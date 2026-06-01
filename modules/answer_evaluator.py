import google.generativeai as genai


def evaluate_answer(question, answer):

    try:

        prompt = f"""
Question:
{question}

Answer:
{answer}

Provide:

Technical Score: X/10
Communication Score: X/10
Confidence Score: X/10

Strengths:
- point

Weaknesses:
- point

Improvement Suggestions:
- point
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
            f"Gemini API Error:\n\n"
            f"{str(e)}"
        )