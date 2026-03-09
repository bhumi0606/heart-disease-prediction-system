import os
from django.contrib import messages

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from HDPM import settings
from doctors.forms import DoctorRequestForm, HeartDataForm, PatientForm
from .models import DoctorRequest, PatientRecord, WorkoutDietPlan
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required,user_passes_test
from .models import PatientRecord, HeartData, PredictionData
import joblib
from .utils import generate_diet_plan, predict_heart, send_email_admin
import pdfkit
from django.template.loader import render_to_string
from django.http import HttpResponse


# Create your views here.

model_path = os.path.join(settings.BASE_DIR, 'Prediction_Model.pkl')
forest_load = joblib.load(model_path)

def is_doctor(user):
    return user.profile.role == 'doctor'

@user_passes_test(is_doctor)
def doctor_dashboard(request):
    patients = PatientRecord.objects.filter(doctor=request.user)

    data = []

    for p in patients:
        heart_records = HeartData.objects.filter(patient=p)
        predictions = PredictionData.objects.filter(patient=p)

        data.append({
            'patient': p,
            'heart_records': heart_records,
            'predictions': predictions
        })

    return render(request, 'core/doctor_dashboard.html', {
        'data': data
    })


# Add Patient
@login_required
def add_patient(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)

        if form.is_valid():
            obj = form.save(commit=False)
            obj.doctor = request.user
            obj.save()

            return redirect('core:dashboard')
    else:
        form = PatientForm()

    return render(request, 'doctors/add_patient.html', {'form': form})

@login_required
def add_heart_data(request, patient_id):
    patient = PatientRecord.objects.get(id=patient_id)

    if request.method == 'POST':
        form = HeartDataForm(request.POST)

        if form.is_valid():
            heart = form.save(commit=False)
            heart.doctor = request.user
            heart.patient = patient
            heart.save()

            result = predict_heart([
                                        heart.age,
                                        heart.sex,
                                        heart.cp,
                                        heart.trestbps,
                                        heart.chol,
                                        heart.fbs,
                                        heart.restecg,
                                        heart.thalach,
                                        heart.exang,
                                        heart.oldpeak,
                                        heart.slope,
                                        heart.ca,
                                        heart.thal
                                    ])
            result = int(result)

            risk = ""
            if result < 40:
                risk = "Low Risk"
            elif result < 70:
                risk = "Medium Risk"
            else:
                risk = "High Risk"
            prediction_record = PredictionData( doctor=request.user,
                patient=patient,
                heartdata=heart,
                heart_disease=result,
                risk=risk)
            prediction_record.save()

            return redirect('core:dashboard')
    else:
        form = HeartDataForm()

    return render(request, 'doctors/add_heart.html', {
        'form': form,
        'patient': patient
    })


@login_required
def patient_detail(request, patient_id):
    patient = PatientRecord.objects.get(id=patient_id, doctor=request.user)

    heart_records = HeartData.objects.filter(patient=patient).order_by('-created_at')
    predictions = PredictionData.objects.filter(patient=patient).order_by('-created_at')

    return render(request, 'doctors/patient_detail.html', {
        'patient': patient,
        'heart_records': heart_records,
        'predictions': predictions
    })

@login_required
def request_doctor(request):

    doctor_request = DoctorRequest.objects.filter(user=request.user).first()
    if request.method == 'POST':
        form = DoctorRequestForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            messages.success(request, "Request submitted successfully!")
            send_email_admin(request.user)
            return render(request, 'doctors/apply_doctor.html', {'form': form,"doctor_request": doctor_request})
        else:
            print("ERROR:", form.errors)
    else:
        form = DoctorRequestForm()

    return render(request, 'doctors/apply_doctor.html', {'form': form,"doctor_request": doctor_request})

@login_required
def doctor_generate_plan(request, prediction_id):

    context = generate_diet_plan(request, prediction_id)

    return render(request, "doctors/plan_result.html", context)


@login_required
def download_plan(request,id):
    context = {
        'plan':WorkoutDietPlan.objects.filter(id=id).first()
    }
    html_string = render_to_string(

        template_name='doctors/workout_plan_download.html',
        context=context,
        request=request
    )

    config = pdfkit.configuration(
        wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
    )
    options = {
    'enable-local-file-access': None,
    }
    pdf_file = pdfkit.from_string(html_string, False,options=options,configuration=config) 
    response = HttpResponse(pdf_file, content_type="application/pdf") 
    response['Content-Disposition'] = 'attachment; filename="workout_diet_plan.pdf"' 
    return response

def currentWorkoutPlan(request):
    current_plan = WorkoutDietPlan.objects.filter(user=request.user).last()
    context = {
        'plan':current_plan
    }
    return render(request,"doctors/plan_result.html",context)