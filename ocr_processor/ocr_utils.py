import os
import cv2
from paddleocr import PaddleOCR
from reportlab.pdfgen import canvas

# Initialize PaddleOCR (supports multiple languages)
ocr = PaddleOCR(use_angle_cls=True, lang='en')  # Change 'en' to 'fa' for Farsi if needed

def calculate_font_size(bbox):
    """
    Calculate font size based on the height of the bounding box.

    Parameters:
        bbox (list): Coordinates of the bounding box.

    Returns:
        int: Estimated font size.
    """
    box_height = abs(bbox[3][1] - bbox[0][1])
    return max(8, int(box_height / 1.5))  # Ensure a minimum font size of 8

def create_positional_pdf_with_font_size(ocr_results, output_pdf, img_width, img_height):
    """
    Create a PDF with text positioned according to OCR results.

    Parameters:
        ocr_results (list): OCR results from PaddleOCR.
        output_pdf (str): Path to save the output PDF.
        img_width (int): Width of the source image.
        img_height (int): Height of the source image.
    """
    c = canvas.Canvas(output_pdf, pagesize=(img_width, img_height))

    for result in ocr_results[0]:
        bbox, text = result[0], result[1][0]

        if not text.strip():
            continue

        font_size = calculate_font_size(bbox)
        x, y = bbox[0][0], img_height - bbox[0][1]  # Invert the y-axis for PDF coordinates
        c.setFont("Helvetica", font_size)
        c.setFillColorRGB(0, 0, 0)
        c.drawString(x, y, text)

    c.save()

def process_image(image_path):
    """
    Process a single image with OCR.

    Parameters:
        image_path (str): Path to the image.

    Returns:
        tuple: OCR results, image width, image height.
    """
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Error: Unable to load image at {image_path}")

    ocr_results = ocr.ocr(image_path, cls=True)
    image_height, image_width, _ = image.shape
    return ocr_results, image_width, image_height
