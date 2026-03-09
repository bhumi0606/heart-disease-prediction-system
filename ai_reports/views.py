import os

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from google import genai

from ai_reports.utils import generate_diet_plan, process_heart_report_file
from .forms import ReportUploadForm
from .models import Report, WorkoutDietPlanUser
import pdfkit
from django.template.loader import render_to_string
from django.http import HttpResponse



@login_required
def generate_ai_result(request):
    if request.method == "POST":
        form = ReportUploadForm(request.POST, request.FILES)

        if form.is_valid():
            files = request.FILES.getlist("file")

            if len(files) > 5:
                return render(request, "ai_reports/uploads.html", {
                    "form": form,
                    "error": "Max 5 files allowed."
                })

            results = []

            for f in files:
                report = Report.objects.create(
                    user=request.user,
                    report_file=f
                )

                result = process_heart_report_file(f)

                ai_text = result.get("ai_report")
                risk = result.get("overall_risk")

                report.result = ai_text
                report.save()

                results.append({
                    "file_name": f.name,
                    "result": ai_text,
                    "risk": risk
                })

            return render(request, "ai_reports/aiResult.html", {
                "results": results
            })

    else:
        form = ReportUploadForm()

    return render(request, "ai_reports/uploads.html", {"form": form})

@login_required
def my_reports(request):
    reports = Report.objects.filter(user=request.user).order_by('-uploaded_at')

    return render(request, 'ai_reports/my_reports.html', {
        'reports': reports
    })

@login_required
def user_generate_plan(request, report_id):

    context = generate_diet_plan(request, report_id)

    return render(request, "ai_reports/plan_result.html", context)

@login_required
def download_plan(request,id):
    context = {
        'plan':WorkoutDietPlanUser.objects.filter(id=id).first()
    }
    html_string = render_to_string(

        template_name='ai_reports/workout_plan_download.html',
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
    current_plan = WorkoutDietPlanUser.objects.filter(user=request.user).last()
    context = {
        'plan':current_plan
    }
    return render(request,"ai_reports/plan_result.html",context)