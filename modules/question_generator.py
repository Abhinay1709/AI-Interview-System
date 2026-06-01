import google.generativeai as genai


def generate_questions(resume_text):

    try:

        prompt = f"""
Generate:

5 Technical Questions
3 HR Questions
2 Project Questions

Based on:

{resume_text}
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
            f"⚠ Gemini API Error\n\n"
            f"{str(e)}\n\n"
            f"Wait 30 seconds and try again."
        )