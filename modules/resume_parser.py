from PyPDF2 import PdfReader
from docx import Document


def extract_resume_text(uploaded_file):

    try:

        file_name = uploaded_file.name.lower()

        extracted_text = ""

        # PDF FILE

        if file_name.endswith(".pdf"):

            reader = PdfReader(
                uploaded_file
            )

            for page in reader.pages:

                page_text = page.extract_text()

                if page_text:

                    extracted_text += (
                        page_text + "\n"
                    )

        # DOCX FILE

        elif file_name.endswith(".docx"):

            document = Document(
                uploaded_file
            )

            for paragraph in document.paragraphs:

                extracted_text += (
                    paragraph.text + "\n"
                )

        else:

            return (
                "Unsupported file format. "
                "Please upload PDF or DOCX."
            )

        extracted_text = (
            extracted_text.strip()
        )

        if not extracted_text:

            return (
                "No text found in the resume."
            )

        return extracted_text

    except Exception as e:

        return (
            f"Error reading resume: "
            f"{str(e)}"
        )