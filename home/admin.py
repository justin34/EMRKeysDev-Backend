from django.contrib import admin
from .models import *

# Register your models here.
# how the admin moduals for this app looks

admin.site.register(User)
admin.site.register(Appointment)
admin.site.register(Patient)
admin.site.register(AINote)
admin.site.register(Symptom)
