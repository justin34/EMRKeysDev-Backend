from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.views import APIView
from . models import *
from .serializer import *
from rest_framework.response import Response

# Create your views here.
# this is the request handler it takes requests and does stuff

def getAppointemnts(request):
    #returns a response as http text
    return HttpResponse('Appointment tommorow at 9am')

def getMain(request):
    return render(request, 'index.html')


class ReactApiView(APIView):
    def get(self, request):
        output = [{'username': user.userName,
                   'email': user.email,
                   'password': user.password,
                   'appointments': [{'time': appointment.time,
                                     'description': appointment.description
                                     }for appointment in user.appointment_set.all()
                                    ]}for user in User.objects.all()]
        return Response(output)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)


