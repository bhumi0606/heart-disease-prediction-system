from django.urls import path
from . import views

app_name = 'doctors'

urlpatterns = [
    path('dashboard/', views.doctor_dashboard, name='doctor-dashboard'),
    path('add-patient/', views.add_patient, name='add-patient'),
    path('add-heart/<int:patient_id>/', views.add_heart_data, name='add-heart'),
    path('patient/<int:patient_id>/', views.patient_detail, name='patient-detail'),
    path('apply/', views.request_doctor, name='apply_doctor'),
    path('generate-plan/<int:prediction_id>/', views.doctor_generate_plan, name='generate_plan'),
    path("workoutplan/download/<int:id>", views.download_plan, name='download-plan'),
    path("current-plan", views.currentWorkoutPlan, name='check-plan'),

]