from django.db import models


# Create your models here.
# used to pull data from the database

class User(models.Model):
    userName = models.CharField(max_length=200, unique=True)
    email = models.CharField(max_length=400, unique=True)
    password = models.CharField(max_length=200)

    def __str__(self):
        string = "User: " + self.userName + "\nEmail: " + self.email + "\nPassword: " + self.password

        return string


class Appointment(models.Model):
    title = models.CharField(max_length=50)
    startTime = models.DateTimeField()
    endTime = models.DateTimeField()
    description = models.CharField(max_length=400)
    app_user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        string = "Time: " + str(self.startTime) + "\nTitle: " + self.title
        return string

class Patient(models.Model):
    users = models.ManyToManyField(User)
    name = models.CharField(max_length=100)
    DOB = models.DateField()
    notes = models.CharField(max_length=5000)
    profile_picture = models.ImageField(upload_to="profilePictures/", default="/media/profilePictures/DefaultProfilePic.png")

