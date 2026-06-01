# AI Interview Preparation System

## Overview

AI Interview Preparation System is an AI-powered mock interview platform that helps users prepare for technical and HR interviews.

The system analyzes resumes, generates personalized interview questions, evaluates answers using AI, stores interview history, and generates reports.

---

## Features

* Resume Upload (PDF)
* Resume Text Extraction
* Skill Detection
* AI-Based Question Generation
* Voice-to-Text Answer Capture
* AI Answer Evaluation
* Technical, Communication, and Confidence Scoring
* Interview History Storage
* Analytics Dashboard
* Report Generation
* SQLite Database Integration

---

## Technologies Used

* Python
* Streamlit
* Gemini API
* SQLite
* SpeechRecognition
* PyPDF2

---

## Project Structure

AI-Interview-System/

├── app.py

├── config.py

├── requirements.txt

├── README.md

├── modules/

│ ├── resume_parser.py

│ ├── skill_extractor.py

│ ├── question_generator.py

│ ├── speech_to_text.py

│ ├── answer_evaluator.py

│ ├── score_parser.py

│ ├── database_manager.py

│ ├── report_generator.py

│ ├── analytics.py

│ └── export_history.py

└── uploads/

---

## Installation

Clone the repository:

git clone https://github.com/YOUR_USERNAME/AI-Interview-System.git

Move into the project folder:

cd AI-Interview-System

Install dependencies:

pip install -r requirements.txt

---

## Environment Variables

Create a `.env` file:

GEMINI_API_KEY=YOUR_API_KEY

---

## Run the Project

streamlit run app.py

---

## Future Enhancements

* Video Interview Support
* Multi-Language Support
* Advanced Resume Analysis
* AI Career Recommendations

---

## Author

Abhinay

Final Year AI/ML Project
