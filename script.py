import pandas as pd
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import Color

def create_temp_pdf(name, x, y, output_path):
    """Creates a temporary PDF with the name at specified coordinates."""
    c = canvas.Canvas(output_path, pagesize=letter)
    c.setFont("Helvetica-BoldOblique", 14)
    custom_color = Color(250/255, 128/255, 114/255) # RGB value format, where it takes range from 0 to 1 only.
    c.setFillColor(custom_color)
    c.drawString(x, y, name)  # Set position (x, y) for the name
    c.save()

def add_name_to_pages(template_path, output_path, name, positions):
    """
    Adds the given name to the specified pages of the template PDF.
    positions: A dictionary where keys are page indices (0-based) and values are (x, y) coordinates.
    """
    writer = PdfWriter()
    template_pdf = PdfReader(template_path)

    for i, page in enumerate(template_pdf.pages):
        if i in positions:  # Check if the current page is in the target positions
            x, y = positions[i]
            temp_pdf_path = "temp_page.pdf"
            create_temp_pdf(name, x, y, temp_pdf_path)  # Create temporary PDF for this page
            temp_pdf = PdfReader(temp_pdf_path)
            page.merge_page(temp_pdf.pages[0])  # Merge temporary PDF onto the current page
        writer.add_page(page)  # Add the (modified or unmodified) page to the output

    # Save the customized PDF
    with open(output_path, "wb") as output_file:
        writer.write(output_file)

def process_invites(template_path, excel_path, output_dir):
    """Processes the Excel file and generates PDFs for all names."""
    # Read the Excel file
    df = pd.read_excel(excel_path)

    # Define target pages and positions
    # Format: {page_index: (x, y)}
    positions = {
        0: (200, 350),  # Page 1
        3: (130, 670),  # Page 4
    }

    # Loop through each name in the Excel file
    for index, row in df.iterrows():
        name = row["Name"]  # Adjust the column name as per your Excel
        mobnum = row["Number"]
        output_file = f"{output_dir}/{mobnum}_{name}.pdf"
        add_name_to_pages(template_path, output_file, name, positions)
        print(f"Generated: {output_file}")

# Paths to your files
template_pdf = "template.pdf"
excel_file = "names.xlsx"
output_directory = "output_invites"

# Process the invitations
process_invites(template_pdf, excel_file, output_directory)

# TO DO
# add google fonts, gujarati font style