import os
from .ocr_utils import process_image, create_positional_pdf_with_font_size
from .pdf_utils import extract_images_from_pdf

def process_image_to_pdf(input_path, output_pdf_path):
    """
    Process an image or PDF to extract text and generate a PDF with positioned text.

    Parameters:
        input_path (str): Path to the input image or PDF file.
        output_pdf_path (str): Path to save the output PDF.
    """
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Error: File not found at {input_path}")

    temp_dir = "temp_images"
    os.makedirs(temp_dir, exist_ok=True)

    image_paths = []

    if input_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
        image_paths.append(input_path)
    elif input_path.lower().endswith('.pdf'):
        image_paths.extend(extract_images_from_pdf(input_path, temp_dir))
    else:
        raise ValueError("Unsupported file format. Please provide an image or PDF file.")

    for image_path in image_paths:
        try:
            ocr_results, image_width, image_height = process_image(image_path)
            output_path = os.path.splitext(output_pdf_path)[0] + f"_{os.path.basename(image_path)}.pdf"
            create_positional_pdf_with_font_size(ocr_results, output_path, image_width, image_height)
            print(f"OCR results with positions and estimated font sizes saved to {output_path}")
        except Exception as e:
            print(f"Error processing {image_path}: {e}")

    # Clean up temporary images
    for img_path in image_paths:
        if img_path != input_path:  # Don't delete the original input if it's an image
            os.remove(img_path)
    os.rmdir(temp_dir)
