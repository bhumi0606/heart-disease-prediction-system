import os
import re
from ai_reports.models import Report, WorkoutDietPlanUser
from doctors.models import PredictionData
import pdfplumber
from PIL import Image, ImageFilter
import pytesseract
from google import genai
from doctors.utils import diet_plan, workOutPlanPrompt

#gemini api call
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Tesseract configuration
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Extract text from PDF or Image
def extract_text(file_path):
    """
    Reads a PDF or image file and extracts text using OCR for scanned PDFs/images.
    """
    text = ""
    try:
        # PDF files
        if file_path.lower().endswith('.pdf'):
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    # First try normal text extraction
                    page_text = page.extract_text()
                    if page_text and page_text.strip():
                        text += page_text + "\n"
                    else:
                        # If empty, run OCR on page image
                        img = page.to_image(resolution=300).original
                        img = img.convert("L")  # grayscale
                        img = img.filter(ImageFilter.SHARPEN)
                        ocr_text = pytesseract.image_to_string(img, config='--psm 6')
                        text += ocr_text + "\n"

        # Image files
        elif file_path.lower().endswith(('.png', '.jpg', '.jpeg')):
            image = Image.open(file_path)
            image = image.convert("L")
            image = image.filter(ImageFilter.SHARPEN)
            text = pytesseract.image_to_string(image, config='--psm 6')

        else:
            raise ValueError("Unsupported file type. Use PDF or image.")

    except Exception as e:
        return f"Error reading file: {str(e)}"

    return text


# Analyze report using AI
def analyze_report(text):
    prompt = f"""
You are a clinical assistant AI.

Analyze the following medical report text and generate a structured, professional summary.

Instructions:
- Extract: Age, Blood Pressure, Cholesterol, Blood Sugar.
- If a value is missing, write "Not Available".
- Use clear, formal, and concise medical language.
- Do NOT include unnecessary conversational sentences.
-Use simple English for a non-medical user.
-Avoid complex medical terms.
-Explain like you are talking to a normal person.

Clinical Rules:
- Blood Pressure: Normal <120/80, Elevated 120-139/80-89, High >=140/90
- Cholesterol: Normal <200, Borderline 200-239, High >=240
- Blood Sugar: Normal <140, Prediabetes 140-180, High >180

Format STRICTLY as:

----------------------------------------
AI MEDICAL REPORT SUMMARY
----------------------------------------

Patient Details:
- Age: <value>

Clinical Findings:
- Blood Pressure: <value> (<Normal/Elevated/High>)
- Cholesterol: <value> (<Normal/Borderline/High>)
- Blood Sugar: <value> (<Normal/Prediabetes/High>)

Risk Assessment:
- Overall Risk Level: <LOW / MEDIUM / HIGH>

Clinical Interpretation:
<2-3 professional lines explaining condition>

Recommendations:
- <short point>
- <short point>
- <short point>

Disclaimer:
This is an AI-assisted analysis and should not replace professional medical advice.

----------------------------------------

Report Text:
{text}
"""
    try:
        response = client.models.generate_content(
            model="models/gemini-flash-latest",
            contents=prompt
        )
        ai_text = response.text
    except Exception as e:
        return {
            "ai_report": "AI service is currently unavailable. Please try again later.",
            "overall_risk": "UNKNOWN",
            "future_risk_percent": None,
            "error": True
        }
    # Extract overall risk
    risk_match = re.search(r"OVERALL RISK LEVEL:\s*(LOW|MEDIUM|HIGH)", ai_text, re.IGNORECASE)
    overall_risk = risk_match.group(1).upper() if risk_match else "UNKNOWN"

    # Extract future risk %
    future_risk_match = re.search(r"Future Risk:\s*(\d{1,3})\s*%", ai_text, re.IGNORECASE)
    future_risk = int(future_risk_match.group(1)) if future_risk_match else None

    return {
        "ai_report": ai_text,
        "overall_risk": overall_risk,
        "future_risk_percent": future_risk
    }


# Main function
def process_heart_report_file(uploaded_file, temp_dir="temp_reports"):
    print("in side method")
    """
    Saves uploaded file temporarily, extracts text, and analyzes with AI.
    """

    # Ensure temp dir exists
    os.makedirs(temp_dir, exist_ok=True)

    # Save uploaded file temporarily
    temp_path = os.path.join(temp_dir, uploaded_file.name)
    with open(temp_path, 'wb+') as f:
        print("open file")

        for chunk in uploaded_file.chunks():
            f.write(chunk)

    # Extract text
    text = extract_text(temp_path)

    if not text.strip() or "Error reading file" in text:
        # Clean up temp file
        os.remove(temp_path)
        return {"ai_report": "Could not extract text from the report.", "overall_risk": "UNKNOWN", "future_risk_percent": None}

    # Send to AI
    result = analyze_report(text)

    # Clean up temp file
    os.remove(temp_path)

    return result


def generate_diet_plan(request, report_id):

    report = Report.objects.filter(
        id=report_id,
        user=request.user
    ).first()
    
    prompt = f"""
    This is a heart health medical report.

    {report.result}

    Based on this report create a workout plan and simple Indian diet plan.

    Output format:

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

    plan = WorkoutDietPlanUser(user=request.user,report_result=report,plan_text=response_text)
    plan.save()
    context = {
        "plan": plan,
    }
    return context