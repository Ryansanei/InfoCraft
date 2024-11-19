import cv2
from paddleocr import PaddleOCR
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import os

# Initialize PaddleOCR (supports multiple languages, including English and Persian)
ocr = PaddleOCR(use_angle_cls=True, lang='en')  # Change 'en' to 'fa' for Farsi if needed

# Function to calculate font size based on bounding box height
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

# Function to create a PDF with positional text and estimated font sizes
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

        # Skip empty text results
        if not text.strip():
            continue

        # Calculate font size based on bounding box height
        font_size = calculate_font_size(bbox)

        # Draw the detected text in the correct position with the estimated font size
        x, y = bbox[0][0], img_height - bbox[0][1]  # Invert the y-axis for PDF coordinates
        c.setFont("Helvetica", font_size)  # Set the font and size
        c.setFillColorRGB(0, 0, 0)  # Set text color to black
        c.drawString(x, y, text)  # Draw the OCR text at the detected position

    c.save()

def main(image_path, output_pdf_path):
    """
    Main function to perform OCR and generate a PDF.

    Parameters:
        image_path (str): Path to the input image file.
        output_pdf_path (str): Path to save the output PDF.
    """
    # Validate input file
    if not os.path.exists(image_path):
        print(f"Error: File not found at {image_path}")
        return

    # Load the image and convert to grayscale
    image = cv2.imread(image_path)
    if image is None:
        print(f"Error: Unable to load image at {image_path}")
        return

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Perform OCR using PaddleOCR
    ocr_results = ocr.ocr(image_path, cls=True)

    # Get the image dimensions
    image_height, image_width, _ = image.shape

    # Create the PDF
    create_positional_pdf_with_font_size(ocr_results, output_pdf_path, image_width, image_height)

    print(f"OCR results with positions and estimated font sizes saved to {output_pdf_path}")


if __name__ == "__main__":
    # Specify input and output paths
    image_path = r"C:\Users\ryans\Downloads\4958571715424792012.jpg"  # Replace with the path to your input image
    output_pdf_path = r"paddleocr_output.pdf"  # Replace with the desired output PDF path

    # Run the main function
    main(image_path, output_pdf_path)
