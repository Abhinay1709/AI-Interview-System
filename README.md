# AI Interview Preparation System

## Overview

AI Interview Preparation System is an AI-powered mock interview platform that helps students and job seekers prepare for technical and HR interviews.

The system analyzes resumes, generates personalized interview questions, collects answers one by one, evaluates the complete interview using AI, stores interview history, generates reports, and provides analytics.

---

## Features

### Resume Analysis

* Upload PDF resumes
* Upload DOCX resumes
* Extract resume text
* Detect technical skills

### AI Question Generation

* Generates 10 interview questions
* 5 Technical Questions
* 3 HR Questions
* 2 Project-Based Questions

### Interview Mode

* One question at a time
* Save & Next navigation
* Previous button
* Edit answers anytime
* Voice-to-text support
* Progress tracking

### AI Evaluation

* Single evaluation for the complete interview
* Technical Score
* Communication Score
* Confidence Score
* Strengths Analysis
* Weakness Analysis
* Suggestions for Improvement

### History Management

* Auto-save completed interviews
* View previous interviews
* Download previous reports
* Delete individual interviews
* Delete complete history

### Analytics Dashboard

* Total Interviews
* Average Technical Score
* Average Communication Score
* Average Confidence Score
* Best Score
* Worst Score

---

## Technologies Used

* Python
* Streamlit
* Google Gemini API
* SQLite
* PyPDF2
* python-docx
* SpeechRecognition

---

## Project Structure

AI-Interview-System/

├── app.py

├── config.py

├── requirements.txt

├── README.md

├── .env

├── modules/

│ ├── resume_parser.py

│ ├── skill_extractor.py

│ ├── question_generator.py

│ ├── speech_to_text.py

│ ├── answer_evaluator.py

│ ├── answer_manager.py

│ ├── database_manager.py

│ ├── report_generator.py

│ ├── analytics.py

│ ├── export_history.py

│ └── score_parser.py

└── interview_data.db

---

## Installation

Clone the repository:

git clone https://github.com/YOUR_USERNAME/AI-Interview-System.git

Move to project folder:

cd AI-Interview-System

Install dependencies:

pip install -r requirements.txt

---

## Environment Setup

Create a .env file:

GEMINI_API_KEY=YOUR_API_KEY

---

## Run Application

streamlit run app.py

---

## Workflow

Upload Resume

↓

Generate Questions

↓

Answer Questions

↓

Finish Interview

↓

AI Evaluation

↓

Auto Save

↓

Analytics Dashboard

↓

History & Reports

---

## Future Enhancements

* Video Interview Support
* Emotion Detection
* Multi-language Interviews
* AI Career Guidance
* Resume Scoring

---

## Author

Abhinay Andhavarapu

AI Interview Preparation System

Final Year Mini Project
