# !/usr/bin/env python
"""
process_bridge.py

This script processes a PDF file by checking whether it contains selectable (text-based)
content or is image-based.

- For a text-based PDF, it directly extracts and cleans the text using pdf_text_extractor.py.
- For an image-based PDF, it converts each page to an image, calls Paddle_OCR.py to perform OCR
  (which outputs a PDF with OCR results), then extracts the text from the OCR PDF.

Finally, the extracted text is cleaned (trimming whitespace) and the lines are sorted alphabetically before printing.
"""

import os
import sys
import tempfile
import shutil
import fitz  # PyMuPDF

# Import helper modules
from check_readable_PDFs import is_pdf_text_based
from pdf_text_extractor import extract_clean_text
import Paddle_OCR  # Ensure this module is in your PYTHONPATH


def process_pdf(pdf_path):
    """
    Process the PDF based on its content.

    If the PDF is text-based, extract text directly.
    If it is image-based, convert each page to an image, run OCR on it,
    and then extract the OCR’d text.

    Args:
        pdf_path (str): Path to the input PDF.

    Returns:
        str: Combined extracted text.
    """
    if not os.path.exists(pdf_path):
        print(f"Error: File not found at {pdf_path}")
        sys.exit(1)

    print(f"Checking PDF type for: {pdf_path}")
    # Check if PDF contains selectable text
    if is_pdf_text_based(pdf_path):
        print("Detected text-based PDF. Extracting text directly...")
        return extract_clean_text(pdf_path)
    else:
        print("Detected image-based PDF. Processing OCR on each page...")
        extracted_pages = []
        # Open the PDF with PyMuPDF
        doc = fitz.open(pdf_path)
        # Create a temporary directory to store image and OCR outputs
        temp_dir = tempfile.mkdtemp(prefix="ocr_process_")

        try:
            for page_num in range(len(doc)):
                print(f"\n--- Processing page {page_num + 1} of {len(doc)} ---")
                page = doc.load_page(page_num)
                # Increase resolution for better OCR (adjust zoom factor if needed)
                zoom = 2
                mat = fitz.Matrix(zoom, zoom)
                pix = page.get_pixmap(matrix=mat)
                image_path = os.path.join(temp_dir, f"page_{page_num}.png")
                pix.save(image_path)
                print(f"Saved page image: {image_path}")

                # Define a temporary output path for the OCR'd PDF page.
                ocr_pdf_path = os.path.join(temp_dir, f"ocr_page_{page_num}.pdf")

                # Run OCR using Paddle_OCR.py; it will create an OCR'd PDF.
                print(f"Running OCR on page {page_num + 1}...")
                Paddle_OCR.main(image_path, ocr_pdf_path)

                # Extract text from the OCR PDF.
                print(f"Extracting text from OCR output: {ocr_pdf_path}")
                page_text = extract_clean_text(ocr_pdf_path)
                if page_text:
                    extracted_pages.append(page_text)
                else:
                    print(f"No text found on page {page_num + 1}.")
        finally:
            # Remove temporary files
            shutil.rmtree(temp_dir)
            print(f"\nCleaned up temporary files in {temp_dir}")

        return "\n".join(extracted_pages)


def clean_and_sort_text(text):
    """
    Clean and sort the extracted text.

    Splits the text into lines, removes extra whitespace,
    sorts the lines alphabetically, and rejoins them.

    Args:
        text (str): The raw extracted text.

    Returns:
        str: Cleaned and alphabetically sorted text.
    """
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    lines.sort()
    return "\n".join(lines)


def main():
    # If a PDF path is provided as an argument, use it; otherwise prompt the user.
    if len(sys.argv) < 2:
        pdf_path = input("Enter the full path to your PDF file: ").strip()
    else:
        pdf_path = sys.argv[1]

    if not pdf_path:
        print("No PDF path provided. Exiting.")
        sys.exit(1)

    print(f"\nStarting processing for PDF: {pdf_path}\n")
    extracted_text = process_pdf(pdf_path)

    if extracted_text:
        cleaned_sorted_text = clean_and_sort_text(extracted_text)
        print("\n--- Extracted, Cleaned & Sorted Text ---\n")
        print(cleaned_sorted_text)
    else:
        print("No text could be extracted from the PDF.")

if __name__ == "__main__":
    main()
