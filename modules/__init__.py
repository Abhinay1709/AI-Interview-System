"""Modules package for AI Interview System."""

from .answer_manager import (
    save_answer,
    get_answer,
    update_answer,
    delete_answer,
    clear_all_answers,
    get_answered_count,
    get_skipped_count
)

from .question_generator import generate_questions
from .resume_parser import extract_resume_text
from .skill_extractor import extract_skills
from .speech_to_text import listen_and_convert
