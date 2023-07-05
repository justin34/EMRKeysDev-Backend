from rest_framework import serializers
from .models import *


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ['time', 'description']


class UserSerializer(serializers.ModelSerializer):
    appointments = AppointmentSerializer(many=True)

    class Meta:
        model = User
        fields = ['userName', 'email', 'password', 'appointments']

    def create(self, validated_data):
        appointment_data = validated_data.pop('tracks')
        user = User.objects.create(**validated_data)
        for appointment in appointment_data:
            Appointment.objects.create(app_user=user, **appointment)
        return user
