from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from ai_reports.models import Report
from doctors.models import HeartData, PatientRecord, PredictionData

# Create your views here.

@login_required
def dashboard(request):
    user = request.user
    role = user.profile.role

    if role == 'doctor':
        # Get all patients of this doctor
        patients = PatientRecord.objects.filter(doctor=user)

        data = []
        for patient in patients:
            heart_records = HeartData.objects.filter(patient=patient)
            predictions = PredictionData.objects.filter(patient=patient)
            data.append({
                'patient': patient,
                'heart_records': heart_records,
                'predictions': predictions
            })

        return render(request, 'core/doctor_dashboard.html', {'data': data})

    else:
        # Normal user: get AI reports
        reports = Report.objects.filter(user=user)
        return render(request, 'core/user_dashboard.html', {'reports': reports})
    
@login_required
def home(request):
    return render(request, 'core/home.html')