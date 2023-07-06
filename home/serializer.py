from rest_framework import serializers
from .models import *


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ['title', 'startTime', 'endTime', 'description']


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
