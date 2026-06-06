"""
AI Interview Preparation System
Modules Package
Version 5.0
"""

# ==========================================================
# ANSWER MANAGER
# ==========================================================

from .answer_manager import (

    save_answer,
    get_answer,
    update_answer,
    delete_answer,

    clear_all_answers,
    clear_answers,

    get_answered_count,
    get_skipped_count,

    get_attempted_questions,
    get_skipped_questions,

    get_interview_statistics,

    validate_answers
)

# ==========================================================
# RESUME PARSER
# ==========================================================

from .resume_parser import (

    extract_resume_text,

    extract_resume_details,

    extract_email,
    extract_phone,
    extract_name,

    extract_projects,
    extract_skills_from_resume,

    generate_resume_summary,

    validate_resume
)

# ==========================================================
# SKILL EXTRACTOR
# ==========================================================

from .skill_extractor import (

    extract_skills,

    extract_skills_by_category,

    generate_skill_summary,

    get_total_skills,

    get_top_skills
)

# ==========================================================
# QUESTION GENERATOR
# ==========================================================

from .question_generator import (

    generate_questions,

    generate_question_groups,

    validate_question_count,

    get_question_distribution,

    get_question_category,

    extract_projects,

    get_project_summary
)

# ==========================================================
# SPEECH TO TEXT
# ==========================================================

from .speech_to_text import (

    listen_and_convert,

    listen_long_answer,

    clean_speech_text,

    is_valid_speech,

    is_skipped_speech
)

# ==========================================================
# ANSWER EVALUATOR
# ==========================================================

from .answer_evaluator import (

    evaluate_full_interview,

    extract_overall_score,

    extract_technical_score,

    extract_communication_score,

    extract_confidence_score,

    extract_strengths,

    extract_weaknesses,

    extract_suggestions,

    extract_question_scores,

    extract_attempted_questions,

    extract_skipped_questions,

    calculate_completion_percentage
)

# ==========================================================
# DATABASE MANAGER
# ==========================================================

from .database_manager import (

    create_table,

    save_interview,

    get_all_interviews,

    get_interview_by_id,

    delete_interview,

    clear_database,

    get_total_interviews,

    get_latest_interview,

    get_interview_count,

    normalize_interview_record,

    get_normalized_interviews,

    get_all_scores
)

# ==========================================================
# REPORT GENERATOR
# ==========================================================

from .report_generator import (

    generate_full_report,

    extract_question_score,

    extract_model_answer,

    extract_feedback
)

# ==========================================================
# ANALYTICS
# ==========================================================

from .analytics import (

    calculate_statistics,

    get_dashboard_metrics,

    get_advanced_statistics,

    get_interview_summary,

    get_score_trend
)

# ==========================================================
# EXPORT HISTORY
# ==========================================================

from .export_history import (

    export_history_to_excel
)

# ==========================================================
# SCORE PARSER
# ==========================================================

from .score_parser import (

    extract_scores,

    get_question_score,

    get_model_answer,

    get_feedback,

    get_question_analysis,

    get_all_question_analysis
)

# ==========================================================
# PACKAGE VERSION
# ==========================================================

__version__ = "5.0.0"

# ==========================================================
# PUBLIC EXPORTS
# ==========================================================

__all__ = [

    # Resume

    "extract_resume_text",
    "extract_resume_details",
    "extract_email",
    "extract_phone",
    "extract_name",
    "extract_projects",
    "extract_skills_from_resume",
    "generate_resume_summary",
    "validate_resume",

    # Skills

    "extract_skills",
    "extract_skills_by_category",
    "generate_skill_summary",
    "get_total_skills",
    "get_top_skills",

    # Questions

    "generate_questions",
    "generate_question_groups",
    "validate_question_count",
    "get_question_distribution",
    "get_question_category",
    "get_project_summary",

    # Answers

    "save_answer",
    "get_answer",
    "update_answer",
    "delete_answer",
    "clear_all_answers",
    "clear_answers",
    "get_answered_count",
    "get_skipped_count",
    "get_attempted_questions",
    "get_skipped_questions",
    "get_interview_statistics",
    "validate_answers",

    # Evaluation

    "evaluate_full_interview",
    "extract_overall_score",
    "extract_technical_score",
    "extract_communication_score",
    "extract_confidence_score",
    "extract_strengths",
    "extract_weaknesses",
    "extract_suggestions",
    "extract_question_scores",
    "extract_attempted_questions",
    "extract_skipped_questions",
    "calculate_completion_percentage",

    # Database

    "create_table",
    "save_interview",
    "get_all_interviews",
    "get_interview_by_id",
    "delete_interview",
    "clear_database",
    "get_total_interviews",
    "get_latest_interview",
    "get_interview_count",
    "normalize_interview_record",
    "get_normalized_interviews",
    "get_all_scores",

    # Reports

    "generate_full_report",
    "extract_question_score",
    "extract_model_answer",
    "extract_feedback",

    # Analytics

    "calculate_statistics",
    "get_dashboard_metrics",
    "get_advanced_statistics",
    "get_interview_summary",
    "get_score_trend",

    # Export

    "export_history_to_excel",

    # Score Parser

    "extract_scores",
    "get_question_score",
    "get_model_answer",
    "get_feedback",
    "get_question_analysis",
    "get_all_question_analysis"
]