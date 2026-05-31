from PyPDF2 import PdfReader


def extract_resume_text(pdf_file):
    """
    Extract text from an uploaded PDF resume.

    Parameters:
        pdf_file: Uploaded PDF file object

    Returns:
        str: Extracted text from all pages
    """

    text = ""

    try:
        reader = PdfReader(pdf_file)

        for page in reader.pages:

            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

        return text.strip()

    except Exception as e:
        return f"Error reading PDF: {str(e)}"