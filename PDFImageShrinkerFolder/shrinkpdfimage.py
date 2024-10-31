import fitz  # PyMuPDF
import io
from PIL import Image
import os

def compress_image_aggressive(image_data, max_dimension=800):
    """Aggressively compress an image"""
    try:
        img = Image.open(io.BytesIO(image_data))
        
        # Convert to RGB
        if img.mode in ['RGBA', 'P', 'PA']:
            bg = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode in ['RGBA', 'PA']:
                bg.paste(img, mask=img.split()[-1])
            else:
                bg.paste(img)
            img = bg
        elif img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Calculate new dimensions
        ratio = min(max_dimension / img.width, max_dimension / img.height)
        if ratio < 1:
            new_width = int(img.width * ratio)
            new_height = int(img.height * ratio)
            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        # Save with high compression
        output = io.BytesIO()
        img.save(output, format='JPEG', quality=95, optimize=True)
        return output.getvalue()
    except Exception as e:
        print(f"Image compression failed: {str(e)}")
        return None

def compress_pdf_images(input_path, output_path, target_size_mb=4):
    try:
        # Open source PDF
        src_pdf = fitz.open(input_path)
        
        # Create new PDF
        new_pdf = fitz.open()
        
        # Process each page
        for page_num in range(src_pdf.page_count):
            src_page = src_pdf[page_num]
            
            # Extract text
            text_blocks = src_page.get_text("blocks")
            
            # Get images
            images = src_page.get_images(full=True)
            
            # Create new page
            new_page = new_pdf.new_page(width=src_page.rect.width,
                                      height=src_page.rect.height)
            
            # Insert compressed images first
            for img_idx, img in enumerate(images):
                try:
                    xref = img[0]
                    base_image = src_pdf.extract_image(xref)
                    
                    if base_image:
                        # Get original image position
                        rects = src_page.get_image_rects(xref)
                        if not rects:
                            continue
                        
                        rect = rects[0]
                        compressed = compress_image_aggressive(base_image["image"])
                        if compressed:
                            new_page.insert_image(rect, stream=compressed)
                except Exception as e:
                    print(f"Warning: Image {img_idx} on page {page_num} failed: {str(e)}")
            
            # Add text blocks
            for block in text_blocks:
                if block[6] == 0:  # Text block
                    rect = fitz.Rect(block[:4])
                    new_page.insert_text(
                        rect.tl,  # top-left point
                        block[4],  # text
                        fontname="helv",  # use standard font
                        fontsize=10,  # approximate size
                        color=(0, 0, 0)  # black
                    )
        
        # Save with maximum compression
        new_pdf.save(
            output_path,
            garbage=4,
            deflate=True,
            clean=True,
            linear=True,
            pretty=False,
            ascii=False
        )
        
        # Clean up
        new_pdf.close()
        src_pdf.close()
        
        # Calculate sizes
        original_size = os.path.getsize(input_path) / (1024 * 1024)
        compressed_size = os.path.getsize(output_path) / (1024 * 1024)
        compression_ratio = (1 - compressed_size / original_size) * 100
        
        return original_size, compressed_size, compression_ratio
    
    except Exception as e:
        raise Exception(f"Compression failed: {str(e)}")

def main():
    output_dir = "PDFImageShrinkerFolder"
    os.makedirs(output_dir, exist_ok=True)
    
    input_file = os.path.join(output_dir, "input.pdf")
    output_file = os.path.join(output_dir, "compressed_output.pdf")
    
    try:
        if not os.path.exists(input_file):
            raise FileNotFoundError(f"Input file not found: {input_file}")
        
        # Remove existing output file if it exists
        if os.path.exists(output_file):
            os.remove(output_file)
        
        original_size, compressed_size, compression_ratio = compress_pdf_images(
            input_file, output_file, target_size_mb=4
        )
        
        print(f"Original size: {original_size:.2f}MB")
        print(f"Compressed size: {compressed_size:.2f}MB")
        print(f"Compression ratio: {compression_ratio:.1f}%")
        print("\nNote: This version rebuilds the PDF from scratch.")
        print("The layout might be slightly different but should be readable.")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()