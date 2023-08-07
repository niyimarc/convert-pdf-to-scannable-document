import fitz
import os
from PIL import Image

def convert_pdf_to_images(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    pdf_files = [file for file in os.listdir(input_folder) if file.lower().endswith('.pdf')]
    
    for pdf_file in pdf_files:
        pdf_path = os.path.join(input_folder, pdf_file)
        doc = fitz.open(pdf_path)
        
        for page_number in range(doc.page_count):
            page = doc.load_page(page_number)
            pix = page.get_pixmap()
            image_path = os.path.join(output_folder, f"{pdf_file}_{page_number + 1}.png")
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            img.save(image_path)

        doc.close()

# Example usage
input_folder = "input"
output_folder = "output"
convert_pdf_to_images(input_folder, output_folder)
