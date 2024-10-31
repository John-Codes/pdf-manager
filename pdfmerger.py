import PyPDF2

# Open the PDF files you want to merge
pdf1_file = open('file1.pdf', 'rb')
pdf2_file = open('file2.pdf', 'rb')

# Create PDF reader objects
pdf1_reader = PyPDF2.PdfReader(pdf1_file)
pdf2_reader = PyPDF2.PdfReader(pdf2_file)

# Create a PDF writer object
pdf_writer = PyPDF2.PdfWriter()

# Add all pages from the first PDF
for page in range(len(pdf1_reader.pages)):
    pdf_writer.add_page(pdf1_reader.pages[page])

# Add all pages from the second PDF
for page in range(len(pdf2_reader.pages)):
    pdf_writer.add_page(pdf2_reader.pages[page])

# Write the merged PDF to a new file
with open('merged.pdf', 'wb') as output_file:
    pdf_writer.write(output_file)

# Close the PDF files
pdf1_file.close()
pdf2_file.close()
