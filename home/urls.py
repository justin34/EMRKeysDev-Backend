from django.urls import path
from . import views


#Django looks for this array to find where to go given urls
urlpatterns = [
    path("", views.getMain, name='home'),
    path("appointments/", views.getAppointemnts),
]