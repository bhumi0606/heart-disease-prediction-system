from django import forms
from .models import DoctorRequest, PatientRecord, HeartData

# Patient Form
class PatientForm(forms.ModelForm):
    class Meta:
        model = PatientRecord
        fields = ['patient_name', 'patient_email']


# Heart Data Form
class HeartDataForm(forms.ModelForm):
    class Meta:
        model = HeartData
        fields = ['age','sex','cp','trestbps','chol','fbs','restecg','thalach','exang','oldpeak','slope','ca','thal']
        widgets = {
            'age': forms.NumberInput(attrs={
                'title': 'age in years'
            }),
            'sex': forms.NumberInput(attrs={
                'title':'1 for Male and 2 for female'
            }),
            'cp': forms.NumberInput(attrs={
                'title':'0 for Typical Angina , 1 for Atypical Angina , 2 for Non-anginal Pain , 3 for Asymptomatic'
            }),
            'trestbps': forms.NumberInput(attrs={
                'title':'Resting blood pressure (mm Hg)'
            }),
            'chol': forms.NumberInput(attrs={
                'title':'serum cholestoral in mg/dl'
            }),
            'fbs': forms.NumberInput(attrs={
                'title':'Fasting blood sugar > 120 mg/dl (1 = True, 0 = False)'
            }),
            'restecg': forms.NumberInput(attrs={
                'title':'resting electrocardiographic results'
            }),
            'thalach': forms.NumberInput(attrs={
                'title':'maximum heart rate achieved'
            }),
            'exang': forms.NumberInput(attrs={
                'title': '1 = yes and 0 = no'
            }),
            'oldpeak':forms.NumberInput(attrs={
                'title': 'ST depression level'
            }),
            'slope': forms.NumberInput(attrs={
                'title':'Slope of peak exercise ST segment'
            }),
            'ca': forms.NumberInput(attrs={
                'title':'Number of major vessels (0–3)'
            }),
            'thal': forms.NumberInput(attrs={
                'title': '0 = normal and 1 = fixed defect and 2 = reversable defect'
            })
        }
        labels={
            'age':'age',
            'sex':'sex:',
            'cp':'chest pain',
            'trestbps':'resting blood pressure',
            'chol':'serum cholestoral',
            'fbs':'fasting blood sugar',
            'restecg':'resting electrocardiographic',
            'thalach':'maximum heart rate achieved',
            'exang':'exercise induced angina',
            'oldpeak':'ST depression induced by exercise relative to rest',
            'slope':'the slope of the peak exercise ST segment',
            'ca':'number of major vessels (0-3) colored by flourosopy',
            'thal':'thal',
            }
        exclude = ['doctor', 'patient', 'created_at']

class DoctorRequestForm(forms.ModelForm):
    class Meta:
        model = DoctorRequest
        fields = ['qualification', 'hospital_name', 'license_number', 'certificate']