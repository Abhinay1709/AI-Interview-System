import re
import google.generativeai as genai


def clean_evaluation_text(text):
    
    if not text:
        return ""

    # Remove markdown bold
    text = re.sub(r"\*\*", "", text)

    # Remove markdown headings
    text = re.sub(
        r"^#+\s*",
        "",
        text,
        flags=re.MULTILINE
    )

    # Convert markdown bullets to bullet symbol
    text = re.sub(
        r"^\s*[\*\-]\s+",
        "• ",
        text,
        flags=re.MULTILINE
    )

    # Remove code fences
    text = text.replace("```", "")

    # Remove separators
    text = text.replace("---", "")

    # Remove tabs
    text = text.replace("\t", " ")

    # Remove excessive blank lines
    text = re.sub(
        r"\n{3,}",
        "\n\n",
        text
    )

    return text.strip()


# ==========================================================
# SKIP WORDS
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
# CHECK SKIPPED ANSWER
# ==========================================================

def is_skipped_answer(answer):

    if answer is None:
        return True

    answer = str(answer).strip().lower()

    return answer in SKIP_WORDS


# ==========================================================
# ATTEMPTED / SKIPPED COUNTS
# ==========================================================

def get_attempted_and_skipped(
        questions,
        answers
):

    attempted = 0
    skipped = 0

    for question in questions:

        answer = answers.get(
            question,
            ""
        )

        if is_skipped_answer(
                answer
        ):
            skipped += 1
        else:
            attempted += 1

    return attempted, skipped


# ==========================================================
# BUILD INTERVIEW DATA
# ==========================================================

def build_interview_content(
        questions,
        answers
):

    content = ""

    for index, question in enumerate(
            questions,
            start=1
    ):

        answer = answers.get(
            question,
            "No Answer"
        )

        content += f"""

Question {index}
----------------------------------------

Question:
{question}

Candidate Answer:
{answer}

"""

    return content


# ==========================================================
# QUESTION TEMPLATE
# ==========================================================

def build_question_template(
        total_questions
):

    template = ""

    for i in range(
            1,
            total_questions + 1
    ):

        template += f"""

Question {i} Score: X/10

Model Answer:
[Ideal Answer]

Feedback:
[Feedback]

"""

    return template


# ==========================================================
# MAIN EVALUATION
# ==========================================================

def evaluate_full_interview(
        questions,
        answers
):

    try:

        attempted_questions, skipped_questions = (
            get_attempted_and_skipped(
                questions,
                answers
            )
        )

        total_questions = len(
            questions
        )

        interview_content = (
            build_interview_content(
                questions,
                answers
            )
        )

        question_template = (
            build_question_template(
                total_questions
            )
        )

        prompt = f"""
You are a Senior Technical Interviewer.

Evaluate the interview professionally.

================================================

TOTAL QUESTIONS:
{total_questions}

ANSWERED:
{attempted_questions}

SKIPPED:
{skipped_questions}

================================================

INTERVIEW DATA

{interview_content}

================================================

SCORING RULES

If answer is:

-
No
N/A
NA
Skip
Skipped
None
Empty

Then:

Question Score = 0/10

================================================

Evaluate EACH question individually.

For EVERY question provide:

1. Question Score
2. Model Answer
3. Feedback

================================================

OUTPUT FORMAT

{question_template}

Technical Score: X/10

Communication Score: X/10

Confidence Score: X/10

Overall Score: X/10

Questions Attempted: {attempted_questions}/{total_questions}

Questions Skipped: {skipped_questions}/{total_questions}

Strengths:
Point 1
Point 2
Point 3

Weaknesses:
Point 1
Point 2
Point 3

Suggestions:
Point 1
Point 2
Point 3

================================================

IMPORTANT RULES

- Use realistic scores.
- Don't give everyone high scores.
- Evaluate technical accuracy.
- Evaluate communication quality.
- Evaluate confidence level.
- Keep model answers concise.
- Feedback should explain mistakes.
- Follow format exactly.
- DO NOT use * or ** anywhere.
- DO NOT use numbered lists.
- Return plain text only.
- Follow the exact format.

IMPORTANT:

Use this format:

Strengths:
• Point 1
• Point 2
• Point 3

Weaknesses:
• Point 1
• Point 2
• Point 3

Suggestions:
• Point 1
• Point 2
• Point 3

Do not use:
**
#
Markdown formatting

Use only the bullet symbol: •
"""
        model = genai.GenerativeModel(
            "gemini-2.5-flash"
        )
        response = model.generate_content(
            prompt
        )       
        evaluation = response.text
        evaluation = clean_evaluation_text(
            evaluation
        )
        return evaluation

    except Exception as e:

        return f"""
Evaluation Error

{str(e)}
"""


# ==========================================================
# EXTRACT SCORE
# ==========================================================

def extract_score(
        evaluation_text,
        score_name
):

    try:

        pattern = rf"{score_name}:\s*(\d+)"

        match = re.search(
            pattern,
            evaluation_text,
            re.IGNORECASE
        )

        if match:

            return int(
                match.group(1)
            )

    except Exception:
        pass

    return 0


# ==========================================================
# OVERALL SCORE
# ==========================================================

def extract_overall_score(
        evaluation_text
):

    return extract_score(
        evaluation_text,
        "Overall Score"
    )


# ==========================================================
# TECHNICAL SCORE
# ==========================================================

def extract_technical_score(
        evaluation_text
):

    return extract_score(
        evaluation_text,
        "Technical Score"
    )


# ==========================================================
# COMMUNICATION SCORE
# ==========================================================

def extract_communication_score(
        evaluation_text
):

    return extract_score(
        evaluation_text,
        "Communication Score"
    )


# ==========================================================
# CONFIDENCE SCORE
# ==========================================================

def extract_confidence_score(
        evaluation_text
):

    return extract_score(
        evaluation_text,
        "Confidence Score"
    )


# ==========================================================
# STRENGTHS
# ==========================================================

def extract_strengths(
        evaluation_text
):

    try:

        match = re.search(

            r"Strengths:(.*?)Weaknesses:",

            evaluation_text,

            re.IGNORECASE |
            re.DOTALL
        )

        if match:

            return (
                match.group(1)
                .strip()
            )

    except Exception:
        pass

    return ""


# ==========================================================
# WEAKNESSES
# ==========================================================

def extract_weaknesses(
        evaluation_text
):

    try:

        match = re.search(

            r"Weaknesses:(.*?)Suggestions:",

            evaluation_text,

            re.IGNORECASE |
            re.DOTALL
        )

        if match:

            return (
                match.group(1)
                .strip()
            )

    except Exception:
        pass

    return ""


# ==========================================================
# SUGGESTIONS
# ==========================================================

def extract_suggestions(
        evaluation_text
):

    try:

        match = re.search(

            r"Suggestions:(.*)",

            evaluation_text,

            re.IGNORECASE |
            re.DOTALL
        )

        if match:

            return (
                match.group(1)
                .strip()
            )

    except Exception:
        pass

    return ""


# ==========================================================
# QUESTION SCORES
# ==========================================================

def extract_question_scores(
        evaluation_text
):

    scores = {}

    try:

        matches = re.findall(

            r"Question\s+(\d+)\s+Score:\s*(\d+)",

            evaluation_text,

            re.IGNORECASE
        )

        for question_no, score in matches:

            scores[
                f"Question {question_no}"
            ] = int(score)

    except Exception:
        pass

    return scores


# ==========================================================
# ATTEMPTED QUESTIONS
# ==========================================================

def extract_attempted_questions(
        evaluation_text
):

    try:

        match = re.search(

            r"Questions Attempted:\s*(\d+)\/(\d+)",

            evaluation_text,

            re.IGNORECASE
        )

        if match:

            return int(
                match.group(1)
            )

    except Exception:
        pass

    return 0


# ==========================================================
# SKIPPED QUESTIONS
# ==========================================================

def extract_skipped_questions(
        evaluation_text
):

    try:

        match = re.search(

            r"Questions Skipped:\s*(\d+)\/(\d+)",

            evaluation_text,

            re.IGNORECASE
        )

        if match:

            return int(
                match.group(1)
            )

    except Exception:
        pass

    return 0


# ==========================================================
# COMPLETION %
# ==========================================================

def calculate_completion_percentage(
        attempted,
        total_questions
):

    if total_questions <= 0:
        return 0

    return round(

        (
            attempted /
            total_questions
        ) * 100,

        2
    )

