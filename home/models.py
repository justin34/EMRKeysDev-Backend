from django.db import models


# Create your models here.
# used to pull data from the database

class User(models.Model):
    userName = models.CharField(max_length=200)
    email = models.CharField(max_length=400)
    password = models.CharField(max_length=200)

    def __str__(self):
        string = "User: " + self.userName + "\nEmail: " + self.email + "\nPassword: " + self.password

        return string


class Appointment(models.Model):
    title = models.CharField(max_length=50)
    startTime = models.CharField(max_length=100)
    endTime = models.CharField(max_length=100)
    description = models.CharField(max_length=400)
    app_user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        string = "Time: " + self.time + "\nDesc: " + self.description
        return string
