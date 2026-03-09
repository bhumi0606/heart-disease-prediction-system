from django.db import models
from django.contrib.auth.models import User

# Create your models here.


# Doctor Request
class DoctorRequest(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    qualification = models.CharField(max_length=200)
    hospital_name = models.CharField(max_length=200)
    license_number = models.CharField(max_length=100)
    certificate = models.FileField(upload_to='doctor_certificates/')

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        profile = self.user.profile

        if self.status == 'approved':
            profile.role = 'doctor'
        elif self.status == 'rejected':
            profile.role = 'user'

        profile.save()

    def __str__(self):
        return self.user.username

# Patient Model
class PatientRecord(models.Model):
    doctor = models.ForeignKey(User, on_delete=models.CASCADE)

    patient_name = models.CharField(max_length=100)
    patient_email = models.EmailField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.patient_name


# Heart Data Model
class HeartData(models.Model):
    doctor = models.ForeignKey(User, on_delete=models.CASCADE)
    patient = models.ForeignKey(PatientRecord, on_delete=models.CASCADE)

    age = models.IntegerField()
    sex = models.IntegerField()
    cp = models.IntegerField()
    trestbps = models.IntegerField()
    chol = models.IntegerField()
    fbs = models.IntegerField()
    restecg = models.IntegerField()
    thalach = models.IntegerField()
    exang = models.IntegerField()
    oldpeak = models.FloatField()
    slope = models.IntegerField()
    ca = models.IntegerField()
    thal = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)


# Prediction Model
class PredictionData(models.Model):
    doctor = models.ForeignKey(User, on_delete=models.CASCADE)
    patient = models.ForeignKey(PatientRecord, on_delete=models.CASCADE)
    heartdata = models.ForeignKey(HeartData, on_delete=models.CASCADE)

    heart_disease = models.IntegerField()
    risk = models.CharField(max_length=20)

    created_at = models.DateTimeField(auto_now_add=True)


class WorkoutDietPlan(models.Model):
    doctor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True)

    patient = models.ForeignKey(
        PatientRecord,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    heart_result = models.ForeignKey(
        PredictionData,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    plan_text = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)