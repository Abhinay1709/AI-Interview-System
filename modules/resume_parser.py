from PyPDF2 import PdfReader
from docx import Document


def extract_resume_text(uploaded_file):

    text = ""

    file_name = uploaded_file.name.lower()

    try:

        # PDF

        if file_name.endswith(".pdf"):

            reader = PdfReader(uploaded_file)

            for page in reader.pages:

                page_text = page.extract_text()

                if page_text:
                    text += page_text + "\n"

        # DOCX

        elif file_name.endswith(".docx"):

            document = Document(uploaded_file)

            for paragraph in document.paragraphs:

                text += paragraph.text + "\n"

        else:

            return "Unsupported file format."

        return text.strip()

    except Exception as e:

        return f"Error reading file: {str(e)}"