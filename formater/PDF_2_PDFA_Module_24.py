import fitz  # PyMuPDF

def convert_to_pdfa(input_pdf, output_pdfa):
    # Open the existing PDF
    pdf_document = fitz.open(input_pdf)
    
    # Save the PDF in PDF/A format
    pdf_document.save(output_pdfa, deflate=True, garbage=4, clean=True)
    pdf_document.close()

    print(f"PDF successfully converted to PDF/A: {output_pdfa}")

# Example usage
input_pdf = "formater\input.pdf"
output_pdfa = "formater\output_pdfa.pdf"

convert_to_pdfa(input_pdf, output_pdfa)
