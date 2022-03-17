from rest_framework import serializers

from .models import Appointment, Doctor, Especiality, Patient
from authentication.serializers import UserSerializer
from django.contrib.auth.models import User


class EspecialitySerialiazer(serializers.ModelSerializer):
    class Meta:
        model = Especiality
        fields = (
            'pk',
            'name'
        )


class DoctorSerialiazer(serializers.ModelSerializer):
    user = UserSerializer()

    especiality = EspecialitySerialiazer(read_only=True)
    especiality_id = serializers.IntegerField(write_only=True)

    user_rol = serializers.SerializerMethodField()

    class Meta:
        model = Doctor
        fields = (
            'pk',
            'user',
            'especiality',
            'especiality_id',
            'first_name',
            'last_name',
            'phone',
            'user_rol'
        )

    def get_user_rol(self, obj):
        return type(obj).__name__

    def create(self, validated_data):
        user_data = validated_data.pop('user', None)

        if not user_data:
            raise Exception('No user data were provided')

        user = User.objects.create_user(
            **user_data
        )
        doctor = Doctor.objects.create(
            user=user,
            **validated_data
        )

        return doctor


class PatientSerialiazer(serializers.ModelSerializer):
    user = UserSerializer()
    user_rol = serializers.SerializerMethodField()

    class Meta:
        model = Patient
        fields = (
            'pk',
            'user',
            'phone',
            'first_name',
            'last_name',
            'user_rol'
        )

    def get_user_rol(self, obj):
        return type(obj).__name__

    def create(self, validated_data):
        user_data = validated_data.pop('user', None)

        if not user_data:
            raise Exception('No user data were provided')

        user = User.objects.create_user(
            **user_data
        )
        patient = Patient.objects.create(
            user=user,
            **validated_data
        )

        return patient


class AppointmentSerialiazer(serializers.ModelSerializer):
    doctor = DoctorSerialiazer(read_only=True)
    doctor_id = serializers.IntegerField(write_only=True)

    patient = PatientSerialiazer(read_only=True)
    patient_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Appointment
        fields = (
            'pk',
            'motive',
            'doctor',
            'doctor_id',
            'patient',
            'patient_id',
            'state',
            'due_date'
        )
