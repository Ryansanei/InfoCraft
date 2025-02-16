from ocr_processor import process_image_to_pdf

if __name__ == "__main__":
    input_path = r"C:\Users\ryans\Documents\Doc1111.pdf"  # Replace with your input image or PDF path
    output_pdf_path = r"paddleocr_output.pdf"  # Replace with your desired output PDF path
    process_image_to_pdf(input_path, output_pdf_path)
    print(f"OCR processing completed. Results saved to {output_pdf_path}")