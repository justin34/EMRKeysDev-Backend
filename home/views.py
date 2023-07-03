from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
# this is the request handler it takes requests and does stuff

def getAppointemnts(request):
    #returns a response as http text
    return HttpResponse('Appointment tommorow at 9am')

def getMain(request):
    return HttpResponse('Home Page')