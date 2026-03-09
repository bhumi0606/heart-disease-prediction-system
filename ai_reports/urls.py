from django.urls import path
from . import views

app_name = 'ai_reports'

urlpatterns = [
    path('upload/', views.generate_ai_result, name='upload_report'),
    path('my-reports/', views.my_reports, name='my_reports'),
    path('generate-plan/<int:report_id>/', views.user_generate_plan, name='generate_plan'),
    path("workoutplan/download/<int:id>", views.download_plan, name='download-plan'),
    path("current-plan", views.currentWorkoutPlan, name='check-plan'),
    
]   