import fitz
import os
from PIL import Image

def merge_images(images):
    widths, heights = zip(*(i.size for i in images))
    total_width = max(widths)
    total_height = sum(heights)
    new_image = Image.new("RGB", (total_width, total_height))
    y_offset = 0
    for img in images:
        new_image.paste(img, (0, y_offset))
        y_offset += img.size[1]
    return new_image

def convert_pdf_to_images(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    pdf_files = [file for file in os.listdir(input_folder) if file.lower().endswith('.pdf')]

    for pdf_file in pdf_files:
        pdf_path = os.path.join(input_folder, pdf_file)
        doc = fitz.open(pdf_path)

        images_to_merge = []
        for page_number in range(doc.page_count):
            page = doc.load_page(page_number)
            pix = page.get_pixmap()
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            images_to_merge.append(img)

        doc.close()

        if len(images_to_merge) > 1:
            merged_image = merge_images(images_to_merge)
            pdf_output_path = os.path.join(output_folder, f"{pdf_file}.pdf")
            merged_image.save(pdf_output_path, "PDF", resolution=100.0)
        else:
            pdf_output_path = os.path.join(output_folder, f"{pdf_file}.pdf")
            images_to_merge[0].save(pdf_output_path, "PDF", resolution=100.0)

# Example usage
input_folder = "input"
output_folder = "output"
convert_pdf_to_images(input_folder, output_folder)
