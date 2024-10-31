from PyPDF2 import PdfReader, PdfWriter
import os

def compress_pdf(input_path, output_path):
    reader = PdfReader(input_path)
    writer = PdfWriter()

    # Copy pages and compress
    for page in reader.pages:
        page.compress_content_streams()  # This applies compression to the PDF content
        writer.add_page(page)

    # Use compression while writing
    writer.add_metadata(reader.metadata)
    
    # Save the compressed file
    with open(output_path, "wb") as output_file:
        writer.write(output_file)
    
    # Calculate compression ratio
    original_size = os.path.getsize(input_path) / (1024 * 1024)  # MB
    compressed_size = os.path.getsize(output_path) / (1024 * 1024)  # MB
    compression_ratio = (1 - compressed_size / original_size) * 100
    
    return original_size, compressed_size, compression_ratio

# Usage
input_file = "imageshrinker/input.pdf"
output_file = "imageshrinker/compressed_output.pdf"

original_size, compressed_size, compression_ratio = compress_pdf(input_file, output_file)
print(f"Original size: {original_size:.2f}MB")
print(f"Compressed size: {compressed_size:.2f}MB")
print(f"Compression ratio: {compression_ratio:.1f}%")