import fitz  # PyMuPDF


def is_pdf_text_based(pdf_path, text_threshold=10):
    """
    Check if a PDF contains selectable text by verifying both embedded fonts and actual extracted text.

    Parameters:
        pdf_path (str): Path to the PDF file.
        text_threshold (int): Minimum number of text characters to classify the PDF as text-based.

    Returns:
        bool: True if the PDF contains selectable text, False if it's likely an image-based PDF.
    """
    doc = fitz.open(pdf_path)
    total_text = ""
    has_fonts = False

    for page in doc:
        # Check if the page contains any fonts
        if page.get_fonts():
            has_fonts = True

        # Extract actual text from the page
        total_text += page.get_text("text").strip()

    # Condition 1: If the extracted text length is above the threshold, it's text-based
    if len(total_text) > text_threshold:
        return True

    # Condition 2: If fonts are present but no actual text is extracted, it may still be image-based
    return False  # No meaningful text, likely an image-based PDF


# Example usage
pdf_path = r"C:\Users\ryans\PycharmProjects\paddler_final\ocr_processor\paddleocr_output_page_1_img_1.jpeg.pdf"
if is_pdf_text_based(pdf_path):
    print("The PDF contains selectable text.")
else:
    print("The PDF is likely image-based.")
