import os
import fitz  # PyMuPDF

def extract_images_from_pdf(pdf_path, temp_dir):
    """
    Extract images from a PDF file and save them to a temporary directory.

    Parameters:
        pdf_path (str): Path to the input PDF file.
        temp_dir (str): Path to the temporary directory to save images.

    Returns:
        list: List of paths to the extracted images.
    """
    doc = fitz.open(pdf_path)
    image_paths = []

    for i in range(len(doc)):
        for img_index, img in enumerate(doc.get_page_images(i)):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]
            image_path = os.path.join(temp_dir, f"page_{i+1}_img_{img_index+1}.{image_ext}")
            with open(image_path, "wb") as img_file:
                img_file.write(image_bytes)
            image_paths.append(image_path)

    return image_paths
