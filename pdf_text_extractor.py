import PyPDF2


def extract_clean_text(pdf_path):
    """
    Extracts and formats text from a PDF file.

    Args:
        pdf_path (str): Path to the PDF file.

    Returns:
        str: Cleaned and formatted text from the PDF.

    Raises:
        RuntimeError: If an error occurs while reading the PDF.
    """
    extracted_text = []
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)

            for page in pdf_reader.pages:
                page_text = page.extract_text()
                if page_text:
                    extracted_text.append(page_text.strip())

        cleaned_text = " ".join(extracted_text)

    except (FileNotFoundError, PyPDF2.errors.PdfReadError) as e:
        raise RuntimeError(f"Error extracting text from PDF '{pdf_path}': {e}")

    return cleaned_text

# This module can now be imported and used in other Python files like:
# from pdf_text_extractor import extract_clean_text
# text = extract_clean_text('path/to/file.pdf')
