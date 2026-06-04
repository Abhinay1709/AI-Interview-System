import google.generativeai as genai


def evaluate_full_interview(
    questions,
    answers
):

    try:

        interview_content = ""

        for index, question in enumerate(
            questions,
            start=1
        ):

            answer = answers.get(question, "No")

            interview_content += f"""
Question {index}:
{question}

Answer:
{answer}

=================================
"""

        # Dynamically build the per-question score lines and model answers
        # so the model knows exactly how many to output
        per_question_format = ""
        for i in range(1, len(questions) + 1):
            per_question_format += f"Question {i} Score: X/10\nModel Answer: [Provide a brief, ideal technical answer here]\n\n"

        prompt = f"""
You are an expert technical interviewer.

Evaluate the COMPLETE interview.

Interview Questions and Answers:

{interview_content}

Evaluation Instructions:

1. Consider ALL answers together.

2. If answer is:
"No"
or
"-"
consider that question skipped and give it 0/10.

3. Provide scores out of 10.

4. Use EXACTLY this format (replace every X with the actual number only, and provide the ideal answer):

Per-Question Scores:
{per_question_format}
Technical Score: X/10

Communication Score: X/10

Confidence Score: X/10

Questions Attempted: X/{len(questions)}

Questions Skipped: X/{len(questions)}

Strengths:
- Point 1
- Point 2

Weaknesses:
- Point 1
- Point 2

Suggestions:
- Point 1
- Point 2

5. Be realistic.

6. Do not give perfect scores unless deserved.

7. Evaluate the entire interview as a whole.
"""

        model = genai.GenerativeModel(
            "gemini-2.5-flash"
        )

        response = model.generate_content(prompt)

        return response.text

    except Exception as e:

        return (
            f"Evaluation Error:\n\n"
            f"{str(e)}"
        )