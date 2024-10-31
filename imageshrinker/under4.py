from PyPDF2 import PdfReader, PdfWriter
import os
from PIL import Image
import io

def compress_pdf(input_path, output_path, image_quality=20):
    reader = PdfReader(input_path)
    writer = PdfWriter()

    for page in reader.pages:
        # Compress page content streams
        page.compress_content_streams()
        
        # Handle resources and images
        if '/Resources' in page and '/XObject' in page['/Resources']:
            resources = page['/Resources']
            if hasattr(resources['/XObject'], 'get_object'):
                xObject = resources['/XObject'].get_object()
            else:
                xObject = resources['/XObject']
            
            for obj_key in xObject:
                if xObject[obj_key]['/Subtype'] == '/Image':
                    try:
                        img_object = xObject[obj_key]
                        
                        # Skip small images
                        if img_object['/Width'] < 100 or img_object['/Height'] < 100:
                            continue
                            
                        # Process image data
                        img_data = img_object._data
                        
                        # Try to open image data
                        try:
                            img = Image.open(io.BytesIO(img_data))
                        except:
                            continue
                            
                        # Convert RGBA to RGB if necessary
                        if img.mode == 'RGBA':
                            img = img.convert('RGB')
                        elif img.mode != 'RGB':
                            img = img.convert('RGB')
                            
                        # Resize large images
                        max_size = 800  # Maximum width/height
                        if max(img.size) > max_size:
                            ratio = max_size / max(img.size)
                            new_size = tuple(int(dim * ratio) for dim in img.size)
                            img = img.resize(new_size, Image.Resampling.LANCZOS)
                            
                        # Save with compression
                        output = io.BytesIO()
                        img.save(output, format='JPEG', quality=image_quality, optimize=True)
                        img_object._data = output.getvalue()
                            
                    except Exception as e:
                        print(f"Error processing image: {str(e)}")
                        continue
        
        writer.add_page(page)

    # Add metadata and save
    if reader.metadata:
        writer.add_metadata(reader.metadata)
    
    with open(output_path, "wb") as output_file:
        writer.write(output_file)
    
    # Calculate compression ratio
    original_size = os.path.getsize(input_path) / (1024 * 1024)  # MB
    compressed_size = os.path.getsize(output_path) / (1024 * 1024)  # MB
    compression_ratio = (1 - compressed_size / original_size) * 100
    
    return original_size, compressed_size, compression_ratio

def compress_to_target(input_file, output_file, target_size_mb=4):
    compression_levels = [30, 20, 10, 5, 1]  # Added more aggressive compression
    
    for quality in compression_levels:
        print(f"\nTrying compression quality: {quality}%")
        original_size, compressed_size, compression_ratio = compress_pdf(
            input_file, 
            output_file, 
            image_quality=quality
        )
        print(f"Original size: {original_size:.2f}MB")
        print(f"Compressed size: {compressed_size:.2f}MB")
        print(f"Compression ratio: {compression_ratio:.1f}%")
        
        if compressed_size <= target_size_mb:
            print(f"✓ Target size achieved with quality level {quality}%")
            break
        elif quality == compression_levels[-1]:
            print("! Could not reach target size even with maximum compression")

# Usage
input_file = "imageshrinker/input.pdf"
output_file = "compressed_output.pdf"

compress_to_target(input_file, output_file, target_size_mb=4)