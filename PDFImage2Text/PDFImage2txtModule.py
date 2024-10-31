import pypdfium2 as pdfium
import pytesseract
from PIL import Image
import io

# Install dependencies:
# pip install pypdfium2 pytesseract pillow

def extract_text_from_pdf():
    # Fixed paths in PDFImage2Text directory
    input_pdf = "PDFImage2Text/input.pdf"
    output_txt = "PDFImage2Text/output.txt"
    
    print(f"Processing: {input_pdf}")
    
    try:
        # Load PDF and convert to images
        pdf = pdfium.PdfDocument(input_pdf)
        
        # Open output file
        with open(output_txt, 'w', encoding='utf-8') as f:
            # Process each page
            for page_number in range(len(pdf)):
                # Convert page to image
                page = pdf[page_number]
                pil_image = page.render().to_pil()
                
                # Extract text
                text = pytesseract.image_to_string(pil_image)
                
                # Write to file
                f.write(f"\n--- Page {page_number + 1} ---\n")
                f.write(text)
                print(f"Processed page {page_number + 1}/{len(pdf)}")
        
        print(f"Text saved to: {output_txt}")
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    extract_text_from_pdf()
    input("Press Enter to exit...")