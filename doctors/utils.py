import os
from doctors.models import PredictionData, WorkoutDietPlan
import joblib
from django.conf import settings
from google import genai
from dotenv import load_dotenv
from django.core.mail import send_mail

load_dotenv()
#gemini api call
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
# client = genai.Client(api_key='AIzaSyCRbaCQKSVnOuzswZJZo7ZW5EiztlOPE3Q')
# client = genai.Client()



model_path = os.path.join(settings.BASE_DIR, 'Prediction_Model.pkl')
model = joblib.load(model_path)

def predict_heart(data):
    prediction = model.predict_proba([data])[0][1] * 100
    return prediction


def diet_plan(prompt):

    prompt = prompt

    response = client.models.generate_content(
        model="models/gemini-flash-latest",
        contents=prompt
    )
    return response.text



def workOutPlanPrompt():
    prompt = """
        Workout Plan
        
        Monday:
        - Exercise:
        - Duration:
        - Diet:
            Breakfast:
                Option 1:
                - Item
                - Item
                Option 2:
                - Item
                - Item
                Option 3:
                - Item
                - Item

                Lunch:
                Option 1:
                - Item
                - Item
                Option 2:
                - Item
                - Item
                Option 3:
                - Item
                - Item

                Snacks:
                Option 1:
                - Item
                - Item
                Option 2:
                - Item
                - Item

                Dinner:
                Option 1:
                - Item
                - Item
                Option 2:
                - Item
                - Item
                Option 3:
                - Item
                - Item
            
        Same as all week days 

        Rules:
        - Simple English
        - Short lines
        - No paragraph
        - No explanation
        - No extra text
        """
    
    return prompt

def generate_diet_plan(request,result_id):
    record = PredictionData.objects.filter(id=result_id).first()
    risk_level = record.risk
    patient = record.patient

    prompt = """
        Write a workout plan and simple Indian diet plan for {risk_level} heart disease risk.
        The workout plan is generate doctor so no prcautions like consult doctor and all
        Give output in this EXACT format:
    """
    prompt += workOutPlanPrompt()
        
    prompt += """
    Precautions:
        1.
        2.
        3.
        4.
        5.

        Rules:
        - Use simple English
        - Use Indian food
        - No long paragraphs
        - Proper line breaks
        - Give healthy options only
    """
    response_text = diet_plan(prompt)
    response_text = response_text.replace("\n", "<br>")
    plan = WorkoutDietPlan(patient=patient,heart_result=record,plan_text=response_text)
    plan.save()
    context = {
        'plan': plan
    }
    return context

def send_email_admin(user):
    subject = "New Doctor Request"
    message = f"""
A user has requested to become a doctor.

User Details:
Username: {user.username}
Email: {user.email}

Please review the request in the admin panel.
"""

    send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [settings.ADMIN_EMAIL],
            fail_silently=False,
        )
    

def send_doctor_approved_email(user):

    subject = "Doctor Request Approved"

    message = f"""
Hello {user.username},

Your request to become a doctor has been approved.

You can now log in and access the doctor dashboard.

Thank you.
"""

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
    )