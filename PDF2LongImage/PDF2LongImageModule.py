import fitz  # PyMuPDF
from PIL import Image
import io

def convert_pdf_to_long_image(pdf_path, output_path, zoom=2.0):
    """
    Convert a PDF file to a single long JPEG image using PyMuPDF.
    
    Args:
        pdf_path (str): Path to the input PDF file
        output_path (str): Path where the output JPEG will be saved
        zoom (float): Zoom factor for resolution (higher means better quality but larger file)
    """
    # Open the PDF
    print("Opening PDF...")
    pdf_document = fitz.open(pdf_path)
    
    # Get all page images
    print("Converting PDF pages to images...")
    page_images = []
    for page_number in range(pdf_document.page_count):
        page = pdf_document[page_number]
        pix = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom))
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        page_images.append(img)
    
    # Calculate dimensions for final image
    width = page_images[0].width
    total_height = sum(img.height for img in page_images)
    
    # Create the final long image
    print("Creating final image...")
    final_image = Image.new('RGB', (width, total_height), 'white')
    
    # Paste all pages into the final image
    current_height = 0
    for img in page_images:
        final_image.paste(img, (0, current_height))
        current_height += img.height
    
    # Save the final image
    print(f"Saving final image to {output_path}...")
    final_image.save(output_path, 'JPEG', quality=95)
    
    # Close the PDF
    pdf_document.close()
    print("Conversion complete!")

# Example usage
if __name__ == "__main__":
    pdf_file = "PDF2LongImage/input.pdf"  # Replace with your PDF file path
    output_file = "PDF2LongImage/output.jpg"  # Replace with desired output path
    
    convert_pdf_to_long_image(pdf_file, output_file)