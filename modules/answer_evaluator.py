import google.generativeai as genai


def evaluate_answer(question, answer):

    try:

        prompt = f"""
You are an expert interviewer.

Interview Question:
{question}

Candidate Answer:
{answer}

Evaluate the answer using the following sections:

Technical Score: X/10
Communication Score: X/10
Confidence Score: X/10

Strengths:
- Item 1
- Item 2

Weaknesses:
- Item 1
- Item 2

Improvement Suggestions:
- Item 1
- Item 2

Keep feedback professional and concise.
"""

        model = genai.GenerativeModel(
            "gemini-2.5-flash"
        )

        response = model.generate_content(
            prompt
        )

        return response.text

    except Exception as e:

        return f"Error: {str(e)}"