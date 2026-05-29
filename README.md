# AI Interview Preparation System

A simple Streamlit application for resume-based interview preparation.

## Features

- Upload a PDF resume
- Extract resume text from the uploaded PDF
- Display the extracted resume content
- Count total resume words
- Detect predefined technical skills from the resume text
- Show detected skill count and a summary panel

## Project Structure

- `app.py` — Streamlit web app entrypoint
- `modules/resume_parser.py` — PDF resume text extraction using `PyPDF2`
- `modules/skill_extractor.py` — Detects predefined skills from extracted text
- `requirements.txt` — Python dependencies

## Requirements

- Python 3.10+ recommended
- `streamlit`
- `PyPDF2`
- `pandas`

## Setup

Open PowerShell in the project folder and run:

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

If you want to use a virtual environment:

```powershell
python -m venv venv
.\\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Run the app

```powershell
streamlit run app.py
```

Then open the local URL shown by Streamlit in your browser.

## Usage

1. Open the app in your browser.
2. Upload a resume PDF using the file uploader.
3. View the extracted resume text.
4. See detected skills and resume word count.

## Notes

- The skill extractor uses a fixed list of skills and matches text case-insensitively.
- Uploaded files are saved in the `uploads/` folder.
