from rest_framework import serializers
from .models import *


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
    #users = UserSerializer(many=True)

    class Meta:
        model = Patient
        fields = ["name", "DOB", "notes", 'profile_picture']

    def create(self, validated_data):
        user_set = validated_data.pop('users')

        patient = Patient.objects.create(**validated_data)
        for user in user_set:
            patient.users.add(user)