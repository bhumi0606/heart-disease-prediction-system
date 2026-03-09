# HeartCare AI – Heart Disease Prediction System

## Project Overview

HeartCare AI is a Django-based web application that helps doctors analyze heart health data and predict the risk of heart disease using a Machine Learning model.

The system allows doctors to add patient information and enter heart-related medical parameters. A trained ML model then analyzes the data and generates a prediction result.

The platform also includes AI-based medical report analysis and email notifications.

---

# User Roles

The system contains **two main roles**:

## 1. User (Patient)

A user can perform the following actions:

* Register an account
* Login to the system
* View profile
* Upload medical reports
* View AI-generated report summaries
* Generate workout and diet recommendations
* View previously uploaded reports

---

## 2. Doctor

A doctor performs the main system operations.

Doctor can:

* Login to the system
* Add patient details
* Enter heart health parameters
* Generate prediction using the ML model
* View prediction results
* Generate workout and diet recommendations

The ML model predicts whether the patient has a **risk of heart disease** based on the entered medical parameters.

---


# Machine Learning Model

The system uses a trained machine learning model:

Prediction_Model.pkl

The model analyzes patient health parameters and predicts the **risk of heart disease**.

---

# Technologies Used

Backend

* Python
* Django

Machine Learning

* Scikit-learn

Frontend

* HTML
* CSS
* Bootstrap

Database

* MySQL

Other Tools

* Docker
* Git

---

# Environment Variables

This project uses environment variables for security.

Create a `.env` file in the project root and add the following:

GEMINI_API_KEY=your_gemini_api_key
EMAIL_HOST_USER=your_email_address
EMAIL_HOST_PASSWORD=your_email_app_password

These variables are used for:

* AI medical report generation
* Sending email notifications

---

# How to Run the Project (Normal Setup)

### 1. Run the Project Using Docker


## Requirements

* Docker
* Docker Compose

Make sure Docker Desktop is installed and running.

---

### 1. Clone the repository

git clone https://github.com/bhumi0606/heart-disease-prediction-system.git

### 2. Navigate to the project folder

cd HDPM

### 3. Build and run containers

docker-compose up --build

This command will build the Docker image and start the Django application.

---

### 4. Open the application

http://localhost:8000

---

### Stop the containers

docker-compose down

---

# Admin Panel

Admin panel is available at:

http://127.0.0.1:8000/admin

The admin can manage users, doctors, and patient data.

---


# Author

Bhumi Prajapati
MCA Student
Dharmsinh Desai University
