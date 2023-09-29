from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from django.conf import settings

from .models import *
from .serializer import *
from rest_framework.response import Response

import os
import openai


# openai.organization = "org-M7wl4qY9529vkapHZH1fDelQ"
# openai.api_key = "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"
# openai.Model.list()


# Create your views here.
# this is the request handler it takes requests and does stuff


def getMain(request):
    return render(request, 'index.html')


class UsersApiView(APIView):
    def get(self, request):
        output = [{'username': user.userName,
                   'email': user.email,
                   'password': user.password,
                   'id': user.id} for user in User.objects.all()]
        return Response(output)


class AppointmentsApiView(APIView):
    def get(self, request, userId):
        if not isinstance(userId, int):
            return Response(data=None)
        output = [{
            'id': appointment.id,
            'title': appointment.title,
            'start': appointment.startTime,
            'end': appointment.endTime,
        } for appointment in User.objects.get(id=userId).appointment_set.all()]
        return Response(output)

    def post(self, request, userId):
        user = User.objects.get(id=userId)
        serializer = AppointmentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)


class PatientApiView(APIView):

    def get(self, request, patientId):
        patient = Patient.objects.get(id=patientId)
        output = {
            'id': patient.id,
            'name': patient.name,
            'DOB': patient.DOB,
            'notes': patient.notes,
            'profile_picture': patient.profile_picture.url,
            'users': [{'id': user.id,
                       'username': user.userName
                       } for user in patient.users.all()]
        }
        return Response(output)

    def post(self, request, patientId):
        patient = Patient.objects.get(id=patientId)
        form = PatientUpdate(request.POST, instance=patient)
        form.save()
        return Response(form.data)


class UserPatientApiView(APIView):

    def get(self, request, userId):
        output = [{
            'id': patient.id,
            'name': patient.name,
            'DOB': patient.DOB,
            'notes': patient.notes,
            'profile_picture': patient.profile_picture.url,
        } for patient in User.objects.get(id=userId).patient_set.all()]
        return Response(output)


class ReactApiView(APIView):
    def get(self, request):
        output = [{'username': user.userName,
                   'email': user.email,
                   'password': user.password,
                   'appointments': [{'id': appointment.id,
                                     'title': appointment.title,
                                     'start': appointment.startTime,
                                     'end': appointment.endTime,
                                     } for appointment in user.appointment_set.all()
                                    ]} for user in User.objects.all()]
        return Response(output)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)


class TempImage(ModelViewSet):
    queryset = TempImages.objects.all()
    serializer_class = ImageSerializer


class AINote(APIView):
    def get(self, request, patientId):
        output = [{"note": ainote.note} for ainote in Patient.objects.get(id=patientId).ainote_set.all()]
        return Response(output)

    def post(self, request, patientId):
        data = request.data
        data['patient'] = patientId
        symptomsDict = data['symptoms']
        symptoms = []
        for symptom in symptomsDict:
            symptomObj = None
            try:
                symptomObj = Symptom.objects.get(symptom=symptom["symptom"], severity=symptom["severity"])
            except:
                symptomObj = Symptom.objects.create(symptom=symptom['symptom'], severity=symptom['severity'])
            finally:
                symptoms.append(symptomObj.id)

        data['symptoms'] = symptoms
        serializer = AINoteSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)


class SympyomList(APIView):
    def get(self, request):
        output = [symptom.symptom.lower() for symptom in Symptom.objects.all()]
        output = sorted(set(output))

        return Response(output)
