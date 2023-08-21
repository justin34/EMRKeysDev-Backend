from rest_framework import serializers
from .models import *
from django import forms
from django.conf import settings

import os
import openai

openai.api_key = settings.OPENAI_KEY


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ['userId', 'title', 'startTime', 'endTime', 'description']

    def create(self, validated_data):
        userId = validated_data.pop('userId')
        user = User.objects.get(id=userId)
        appointment = user.appointment_set.create(**validated_data)
        return appointment


class UserSerializer(serializers.ModelSerializer):
    appointment_set = AppointmentSerializer(many=True)

    class Meta:
        model = User
        fields = ['userName', 'email', 'password', 'appointment_set']

    def create(self, validated_data):
        appointment_data = validated_data.pop('appointment_set')
        user = User.objects.create(**validated_data)
        for appointment in appointment_data:
            Appointment.objects.create(app_user=user, title=appointment['title'], startTime=appointment['startTime'],
                                       endTime=appointment['endTime'], description=appointment['description'])
        return user


class PatientSerializer(serializers.ModelSerializer):
    users = UserSerializer(many=True)

    class Meta:
        model = Patient
        fields = ["name", "DOB", "notes", 'profile_picture']

    def create(self, validated_data):
        user_set = validated_data.pop('users')

        patient = Patient.objects.create(**validated_data)
        for user in user_set:
            patient.users.add(user)


class AINoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = AINote
        fields = ['symptoms', 'patient']

    def create(self, validated_data):
        prompt = "Write a short doctors note summarizing the folowing symptoms do not include the date or the reasons" \
                 " for the symptoms:\n"
        patient = validated_data['patient']
        symptoms = validated_data.pop('symptoms')
        aINote = patient.ainote_set.create()

        for symptom in symptoms:
            prompt = prompt + symptom.symptom + " is " + symptom.severity + '\n'
            aINote.symptoms.add(symptom)

        completion = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=[{'role': 'user', 'content': prompt}],
            temperature=0.2
        )

        aINote.note = completion["choices"][0]["message"]["content"]
        aINote.save()
        print(completion["choices"][0]["message"]["content"])

        return aINote


class PatientUpdate(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['name', 'DOB', 'profile_picture']


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = TempImages
        fields = ["image"]
