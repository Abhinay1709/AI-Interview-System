import google.generativeai as genai


def generate_questions(resume_text):

    try:

        prompt = f"""
You are an expert technical interviewer.

Analyze the following resume:

{resume_text}

Generate EXACTLY 10 interview questions.

Requirements:

1. Generate:
   - 5 Technical Questions
   - 3 HR Questions
   - 2 Project Questions

2. Questions should be based on:
   - Skills
   - Technologies
   - Projects
   - Experience mentioned in the resume

3. Number every question.

Example format:

1. What is Python?

2. Explain Flask architecture.

3. What is Machine Learning?

...

10. Explain your final year project.

Rules:

- Output only questions.
- Do not provide answers.
- Do not provide headings.
- Do not provide explanations.
- Generate exactly 10 questions.
"""

        model = genai.GenerativeModel(
            "gemini-2.5-flash"
        )

        response = model.generate_content(
            prompt
        )

        return response.text

    except Exception as e:

        return (
            f"Question Generation Error:\n\n"
            f"{str(e)}"
        )