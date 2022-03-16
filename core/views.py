
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.generics import (CreateAPIView, ListAPIView,
                                     ListCreateAPIView, RetrieveAPIView,
                                     RetrieveDestroyAPIView,
                                     RetrieveUpdateDestroyAPIView)
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly, AllowAny)
from rest_framework.response import Response
from rest_framework.status import (HTTP_200_OK, HTTP_201_CREATED,
                                   HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST)
from rest_framework.views import APIView

from .models import Appointment, Doctor, Especiality, Patient
from .serializers import (AppointmentSerialiazer, DoctorSerialiazer,
                          EspecialitySerialiazer, PatientSerialiazer)


class EspecialityListView(ListCreateAPIView):
    permission_classes = (IsAuthenticated, )
    queryset = Especiality.objects.filter(is_active=True)
    serializer_class = EspecialitySerialiazer
    filter_backends = (
        DjangoFilterBackend,
        SearchFilter
    )
    filterset_fields = {
        "name": ['exact'],
    }
    search_fields = [
        '$name',
    ]


class EspecialityDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, )
    queryset = Especiality.objects.filter(is_active=True)
    serializer_class = EspecialitySerialiazer


class DoctorListView(ListCreateAPIView):
    permission_classes = (AllowAny, )
    queryset = Doctor.objects.filter(is_active=True)
    serializer_class = DoctorSerialiazer
    filter_backends = (
        DjangoFilterBackend,
        SearchFilter
    )
    filterset_fields = {
        "user": ['exact'],
        "user__email": ['exact'],
        "user__first_name": ['exact'],
        "user__last_name": ['exact'],
        "especiality": ['exact'],
        "especiality__name": ['exact'],
    }
    search_fields = [
        "$user__first_name",
        "$user__last_name",
        "$especiality__name",
    ]


class DoctorDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, )
    queryset = Doctor.objects.filter(is_active=True)
    serializer_class = DoctorSerialiazer


class PatientListView(ListCreateAPIView):
    permission_classes = (AllowAny, )
    queryset = Patient.objects.filter(is_active=True)
    serializer_class = PatientSerialiazer
    filter_backends = (
        DjangoFilterBackend,
        SearchFilter
    )
    filterset_fields = {
        "user": ['exact'],
        "user__email": ['exact'],
        "user__first_name": ['exact'],
        "user__last_name": ['exact'],
    }
    search_fields = [
        "$user__first_name",
        "$user__last_name",
    ]


class PatientDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, )
    queryset = Patient.objects.filter(is_active=True)
    serializer_class = PatientSerialiazer


class AppointmentListView(ListCreateAPIView):
    permission_classes = (IsAuthenticated, )
    queryset = Appointment.objects.filter(is_active=True)
    serializer_class = AppointmentSerialiazer
    filter_backends = (
        DjangoFilterBackend,
        SearchFilter
    )
    filterset_fields = {
        "user__email": ['exact'],
        "user__first_name": ['exact'],
        "user__last_name": ['exact'],
        "state": ['exact'],
        "due_date": ['exact', 'gt', 'lt', 'gte', 'lte'],
    }
    search_fields = [
        "$motive",
        "$doctor__user__first_name",
        "$doctor__user__last_name",
        "$patient__user__first_name",
        "$patient__user__last_name",
    ]

    def post(self, request, *args, **kwargs):
        try:
            response = super(AppointmentListView, self).post(request)
            return Response(data=response.data, status=HTTP_201_CREATED)
        except Exception as e:
            return Response(data={"detail": str(e)}, status=HTTP_400_BAD_REQUEST)


class AppointmentDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, )
    queryset = Appointment.objects.filter(is_active=True)
    serializer_class = AppointmentSerialiazer

    def put(self, request, pk):
        try:
            response = super(AppointmentDetailView, self).put(request)
            return Response(data=response.data, status=HTTP_201_CREATED)
        except Exception as e:
            return Response(data={"detail": str(e)}, status=HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        try:
            response = super(AppointmentDetailView, self).patch(request)
            return Response(data=response.data, status=HTTP_201_CREATED)
        except Exception as e:
            return Response(data={"detail": str(e)}, status=HTTP_400_BAD_REQUEST)
