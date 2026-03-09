from django import forms
from .models import Report

# class ReportUploadForm(forms.ModelForm):
#     class Meta:
#         model = Report
#         fields = ['report_file']

class ReportUploadForm(forms.Form):
    file = forms.FileField(required=False)