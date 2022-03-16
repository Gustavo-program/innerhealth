from django.contrib import admin

from .models import Especiality, Doctor, Patient, Appointment


admin.site.register(Especiality)
admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(Appointment)
