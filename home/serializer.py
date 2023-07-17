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
    userIds = UserSerializer(many=True)

    class Meta:
        model = Patient
        fields = ["name", "DOB", "notes", 'userId_set']

    def create(self, validated_data):
        userId_set = validated_data.pop('userId_set')

        patient = Patient.objects.create(**validated_data)
        for userId in userId_set:
            patient.users.add(User.objects.get(id=userId))