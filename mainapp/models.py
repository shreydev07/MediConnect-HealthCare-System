from django.db import models
from adminapp.models import DoctorRegister

# Create your models here.

class AdminLogin(models.Model):
    userid=models.CharField(max_length=50)
    password=models.CharField(max_length=50)


class Complaints(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=10)
    complaint = models.TextField()
    registered_date=models.DateField()



class Appointment(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    contact = models.CharField(max_length=15)
    symptoms = models.TextField()
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    doctor_speciality = models.CharField(max_length=80)
    doctor = models.ForeignKey(DoctorRegister, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    # status will track the appointment lifecycle. Values:
    # PENDING  - newly created, doctor action required
    # PROCESSING - approved or rescheduled by doctor, awaiting completion
    # COMPLETED - appointment was completed
    # REJECTED - appointment was rejected by doctor
    STATUS_PENDING = 'PENDING'
    STATUS_PROCESSING = 'PROCESSING'
    STATUS_COMPLETED = 'COMPLETED'
    STATUS_REJECTED = 'REJECTED'

    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_PROCESSING, 'Processing'),
        (STATUS_COMPLETED, 'Completed'),
        (STATUS_REJECTED, 'Rejected'),
    ]

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} → {self.doctor.doctor_name}"
    


    

    






