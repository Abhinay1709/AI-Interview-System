import os
from dotenv import load_dotenv


# ==========================================================
# LOAD ENVIRONMENT VARIABLES
# ==========================================================

load_dotenv()


# ==========================================================
# GEMINI API KEY
# ==========================================================

GEMINI_API_KEY = os.getenv(
    "GEMINI_API_KEY"
)

# If the key is not provided, warn instead of raising so the
# app can start in limited mode (useful for local dev or when
# features that require the key are optional).
if not GEMINI_API_KEY:
    import warnings

    warnings.warn(
        (
            "GEMINI_API_KEY not found. Some features may not work.\n"
            "Create a .env file in project root or set the environment variable:\n\n"
            "GEMINI_API_KEY=your_api_key_here"
        ),
        UserWarning,
    )

    GEMINI_API_KEY = None


# ==========================================================
# APPLICATION CONFIGURATION
# ==========================================================

APP_NAME = (
    "AI Interview Preparation System"
)

APP_VERSION = "5.0"


# ==========================================================
# QUESTION CONFIGURATION
# ==========================================================

TOTAL_QUESTIONS = 10

TECHNICAL_QUESTIONS = 5

HR_QUESTIONS = 3

PROJECT_QUESTIONS = 2


# ==========================================================
# QUESTION CATEGORY LABELS
# ==========================================================

QUESTION_TYPES = {

    "technical": 5,

    "hr": 3,

    "project": 2
}


# ==========================================================
# SKIP ANSWERS
# ==========================================================

SKIP_WORDS = [

    "",

    "-",

    "no",

    "n/a",

    "na",

    "skip",

    "skipped",

    "none"
]


# ==========================================================
# FILE UPLOAD CONFIGURATION
# ==========================================================

ALLOWED_FILE_TYPES = [

    "pdf",

    "docx",

    "txt"
]

MAX_FILE_SIZE_MB = 10


# ==========================================================
# DATABASE CONFIGURATION
# ==========================================================

DATABASE_NAME = (
    "interview_data.db"
)


# ==========================================================
# REPORT CONFIGURATION
# ==========================================================

REPORT_FILE_NAME = (
    "Interview_Report.docx"
)

HISTORY_REPORT_PREFIX = (
    "Interview_Report_"
)

EXPORT_HISTORY_FILE = (
    "Interview_History.xlsx"
)


# ==========================================================
# ANALYTICS CONFIGURATION
# ==========================================================

ENABLE_ANALYTICS = True

SHOW_SCORE_CHARTS = True

SHOW_COMPLETION_STATS = True


# ==========================================================
# SPEECH CONFIGURATION
# ==========================================================

ENABLE_VOICE_INPUT = True

SPEECH_LANGUAGE = (
    "en-US"
)

SPEECH_TIMEOUT = 15

SPEECH_PHRASE_LIMIT = 60


# ==========================================================
# EVALUATION CONFIGURATION
# ==========================================================

MAX_SCORE = 10

ENABLE_QUESTION_ANALYSIS = True

ENABLE_MODEL_ANSWERS = True

ENABLE_FEEDBACK = True

AUTO_SAVE_AFTER_EVALUATION = True


# ==========================================================
# HISTORY CONFIGURATION
# ==========================================================

ENABLE_INTERVIEW_HISTORY = True

ENABLE_DELETE_INTERVIEW = True

ENABLE_DELETE_HISTORY = True

ENABLE_EXPORT_HISTORY = True

ENABLE_OLD_REPORT_DOWNLOAD = True


# ==========================================================
# DASHBOARD CONFIGURATION
# ==========================================================

ENABLE_DASHBOARD = True

ENABLE_ADVANCED_ANALYTICS = True


# ==========================================================
# STATUS LABELS
# ==========================================================

STATUS_NOT_STARTED = (
    "Not Started"
)

STATUS_IN_PROGRESS = (
    "In Progress"
)

STATUS_COMPLETED = (
    "Completed"
)

STATUS_EVALUATED = (
    "Evaluated"
)


# ==========================================================
# UI LABELS
# ==========================================================

RESUME_UPLOAD_TITLE = (
    "📄 Resume Upload"
)

QUESTION_SECTION_TITLE = (
    "🎯 Interview Questions"
)

EVALUATION_SECTION_TITLE = (
    "📊 Interview Evaluation"
)

ANALYTICS_SECTION_TITLE = (
    "📈 Analytics Dashboard"
)

HISTORY_SECTION_TITLE = (
    "📚 Interview History"
)

EXPORT_SECTION_TITLE = (
    "📤 Export History"
)


# ==========================================================
# DEFAULT MESSAGES
# ==========================================================

RESUME_SUCCESS_MESSAGE = (
    "Resume Parsed Successfully"
)

INVALID_RESUME_MESSAGE = (
    "Invalid Resume Uploaded"
)

QUESTION_GENERATED_MESSAGE = (
    "Questions Generated Successfully"
)

INTERVIEW_SAVED_MESSAGE = (
    "Interview Saved Successfully"
)

HISTORY_CLEARED_MESSAGE = (
    "Interview History Deleted Successfully"
)

NO_HISTORY_MESSAGE = (
    "No Interview History Available"
)


# ==========================================================
# FOOTER
# ==========================================================

FOOTER_TEXT = (
    "AI Interview Preparation System"
)

DEVELOPER_NAME = (
    "Abhinay Andhavarapu"
)