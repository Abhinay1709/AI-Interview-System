import re
from datetime import datetime

def generate_full_report(
    questions,
    answers,
    evaluation
):

    report = "============================================================\n"
    report += "                 AI INTERVIEW SYSTEM REPORT                 \n"
    report += "============================================================\n"
    report += f"Generated On: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"

    # ── EXTRACT OVERALL SCORES FOR THE TOP OF THE REPORT
    tech_score = "N/A"
    comm_score = "N/A"
    conf_score = "N/A"
    
    if evaluation:
        ts = re.search(r"Technical Score:\s*(.*?/10)", evaluation, re.IGNORECASE)
        cs = re.search(r"Communication Score:\s*(.*?/10)", evaluation, re.IGNORECASE)
        cfs = re.search(r"Confidence Score:\s*(.*?/10)", evaluation, re.IGNORECASE)
        
        if ts: tech_score = ts.group(1)
        if cs: comm_score = cs.group(1)
        if cfs: conf_score = cfs.group(1)

    report += "--- OVERALL SCORES ---\n"
    report += f"Technical Score:     {tech_score}\n"
    report += f"Communication Score: {comm_score}\n"
    report += f"Confidence Score:    {conf_score}\n\n"

    report += "============================================================\n"
    report += "             QUESTIONS, ANSWERS & FEEDBACK                  \n"
    report += "============================================================\n\n"

    # ── CHECK IF QUESTIONS EXIST
    if not questions:
        report += "No questions or answers found for this record.\n"
        report += "(This is likely an older or incomplete database entry).\n\n"
    else:
        # ── LOOP THROUGH EACH QUESTION TO EXTRACT INDIVIDUAL DATA
        for index, question in enumerate(questions, start=1):

            answer = answers.get(question, "*(No answer provided)*")
            
            q_score = "N/A"
            model_answer = "*(Not available for this record)*"
            
            if evaluation:
                # Extract score for this specific question
                sm = re.search(rf"Question {index} Score:\s*(.*?/10)", evaluation, re.IGNORECASE)
                if sm: 
                    q_score = sm.group(1)
                
                # Extract the correct model answer for this specific question
                am = re.search(rf"Question {index} Score:.*?Model Answer:\s*(.*?)(?=\nQuestion \d+ Score|\nTechnical Score|\nCommunication Score|\nQuestions Attempted|\Z)", evaluation, re.DOTALL | re.IGNORECASE)
                if am: 
                    model_answer = am.group(1).strip()

            report += f"QUESTION {index}:\n"
            report += f"{question}\n\n"
            
            report += "YOUR ANSWER:\n"
            report += f"{answer}\n\n"
            
            report += f"SCORE OBTAINED: {q_score}\n\n"
            
            report += "CORRECT / MODEL ANSWER:\n"
            report += f"{model_answer}\n\n"
            
            report += "-" * 60 + "\n\n"

    # ── APPEND THE FULL RAW EVALUATION AT THE BOTTOM
    report += "============================================================\n"
    report += "                 FULL EVALUATION SUMMARY                    \n"
    report += "============================================================\n\n"
    
    report += evaluation if evaluation else "No evaluation available."
    
    report += "\n\n============================================================\n"
    report += "                       END OF REPORT                        \n"
    report += "============================================================\n"

    return report