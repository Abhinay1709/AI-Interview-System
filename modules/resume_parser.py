from PyPDF2 import PdfReader


def extract_resume_text(pdf_file):
    """
    Extract text from uploaded PDF resume.
    """

    text = ""

    reader = PdfReader(pdf_file)

    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text