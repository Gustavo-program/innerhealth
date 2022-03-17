from django.db import models
from authentication.models import InnerHealthAbstractClass, User


class Especiality(InnerHealthAbstractClass):
    class Meta:
        verbose_name = "Especiality"
        verbose_name_plural = "Especialities"

    name = models.CharField(
        max_length=250,
        verbose_name=("Name")
    )

    def __str__(self):
        return self.name


class Patient(InnerHealthAbstractClass):
    class Meta:
        verbose_name = "Patient"
        verbose_name_plural = "Patients"

    user = models.OneToOneField(
        User,
        related_name='user_patient',
        on_delete=models.CASCADE,
        verbose_name=("User")
    )
    first_name = models.CharField(
        max_length=155,
        default='',
        verbose_name="First Name"
    )
    last_name = models.CharField(
        max_length=155,
        default='',
        verbose_name="Last Name"
    )
    phone = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name=("Phone")
    )

    def __str__(self):
        return self.first_name


class Doctor(InnerHealthAbstractClass):
    class Meta:
        verbose_name = "Doctor"
        verbose_name_plural = "Doctors"

    user = models.OneToOneField(
        User,
        related_name='user_doctor',
        on_delete=models.CASCADE,
        verbose_name=("User")
    )
    especiality = models.ForeignKey(
        Especiality,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=("Especiality")
    )
    first_name = models.CharField(
        max_length=155,
        default='',
        verbose_name="First Name"
    )
    last_name = models.CharField(
        max_length=155,
        default='',
        verbose_name="Last Name"
    )
    phone = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name=("Phone")
    )

    def __str__(self):
        return self.first_name


class Appointment(InnerHealthAbstractClass):
    _APPOINTMENT_STATES = (
        ('REQUESTED', 'SOLICITADA'),
        ('REJECTED', 'RECHAZADA'),
        ('ACCEPTED', 'ACEPTADA'),
    )

    class Meta:
        verbose_name = "Appointment"
        verbose_name_plural = "Appointments"

    motive = models.TextField(
        null=True
    )
    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE,
        verbose_name=("Doctor")
    )
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        verbose_name=("Patient")
    )
    state = models.CharField(
        max_length=25,
        choices=_APPOINTMENT_STATES,
        default='REQUESTED',
        verbose_name=("State")
    )
    due_date = models.DateTimeField(
        verbose_name=("Due date")
    )

    def __str__(self):
        return f"Doctor: {self.doctor.first_name} Patient: {self.patient.first_name}"

    def save(self, *args, **kwargs):
        existent_appointment = self.__class__.objects.filter(
            doctor=self.doctor,
            due_date=self.due_date
        ).exclude(id=self.pk)

        if existent_appointment:
            raise Exception(
                "El doctor ya tiene una cita programada para esa fecha")

        super(Appointment, self).save(*args, **kwargs)
