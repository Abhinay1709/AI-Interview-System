import google.generativeai as genai


def generate_questions(resume_text):
    """
    Generate interview questions from resume text.

    Parameters:
        resume_text (str): Extracted resume content

    Returns:
        str: Generated interview questions
    """

    try:

        prompt = f"""
You are an experienced technical interviewer.

Analyze the candidate's resume carefully and generate interview questions.

Resume:
{resume_text}

Instructions:
1. Generate 5 Technical Questions.
2. Generate 3 HR Questions.
3. Generate 2 Project-Based Questions.
4. Questions should be relevant to the candidate's skills and projects.
5. Number all questions clearly.
6. Return only the questions.

Format:

Technical Questions:
1.
2.
3.
4.
5.

HR Questions:
6.
7.
8.

Project Questions:
9.
10.
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
            f"Error generating questions: "
            f"{str(e)}"
        )