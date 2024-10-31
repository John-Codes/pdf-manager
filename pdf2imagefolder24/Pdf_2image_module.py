import fitz  # PyMuPDF
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import os

# Step 1: Specify the path to your PDF file
pdf_path = 'pdf2imagefolder24/input.pdf'  # Replace with your PDF file path
output_pdf_path = 'pdf2imagefolder24/output.pdf'  # The final PDF file path

# Step 2: Create a new PDF
c = canvas.Canvas(output_pdf_path, pagesize=letter)

# Step 3: Convert PDF to images and add to the new PDF
pdf_document = fitz.open(pdf_path)

for page_num in range(len(pdf_document)):
    # Get a specific page
    page = pdf_document.load_page(page_num)  
    # Render the page to an image (pixmap)
    pix = page.get_pixmap()

    # Save the image as a JPEG
    temp_img_path = "temp_image.jpg"
    pix.save(temp_img_path, "JPEG")

    # Draw the image onto the PDF
    c.drawImage(temp_img_path, 0, 0, width=letter[0], height=letter[1])  # Adjust the size as needed
    c.showPage()  # Create a new page for each image

    # Optionally, remove the temporary image after using it
    os.remove(temp_img_path)

# Step 4: Finalize the PDF
c.save()

print("Final PDF created:", output_pdf_path)
