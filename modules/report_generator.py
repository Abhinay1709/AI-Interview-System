def generate_report(
    question,
    answer,
    evaluation
):

    report = f"""
AI Interview Report

==================================

Question:

{question}

==================================

Answer:

{answer}

==================================

Evaluation:

{evaluation}

==================================
"""

    return report