from django.urls import path

from core.models import Patient

from .views import (AppointmentDetailView, AppointmentListView, DoctorDetailView, DoctorListView, EspecialityDetailView,
                    EspecialityListView, PatientDetailView, PatientListView)

urlpatterns = [
    # Especiality
    path("especialities/", EspecialityListView.as_view(), name="especialities"),
    path("especialities/<int:pk>/", EspecialityDetailView.as_view(),
         name="especialities-detail"),

    # doctors
    path("doctors/", DoctorListView.as_view(), name="doctors"),
    path("doctors/<int:pk>/", DoctorDetailView.as_view(),
         name="doctors-detail"),

    # patients
    path("patients/", PatientListView.as_view(), name="patients"),
    path("patients/<int:pk>/", PatientDetailView.as_view(),
         name="patients-detail"),

    # Appointments
    path("appointments/", AppointmentListView.as_view(), name="appointments"),
    path("appointments/<int:pk>/", AppointmentDetailView.as_view(),
         name="appointments-detail"),
]
