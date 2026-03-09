from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Report(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    report_file = models.FileField(upload_to='reports/')
    result = models.TextField(blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
    

class WorkoutDietPlanUser(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    report_result = models.ForeignKey(
        Report,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    plan_text = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)