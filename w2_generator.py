#!/usr/bin/env python3
"""
W2 PDF Generator - Creates individual W-2 forms from CSV data
Generates realistic-looking W-2 forms for CPA training purposes

Usage:
# Basic usage (creates 'w2_output' directory)
python w2_generator.py synthetic_w2_data.csv

# Specify custom output directory
python w2_generator.py synthetic_w2_data.csv my_training_w2s

"""

import csv
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

def create_w2_pdf(employee_data, output_dir):
    """
    Create a single W-2 PDF for an employee
    
    Args:
        employee_data: Dictionary containing all W-2 fields
        output_dir: Directory to save the PDF
    """
    # Create filename from employee name
    filename = f"{employee_data['last_name']}_{employee_data['first_name']}_W2.pdf"
    filepath = os.path.join(output_dir, filename)
    
    # Create canvas
    c = canvas.Canvas(filepath, pagesize=letter)
    width, height = letter
    
    # Set up fonts
    c.setFont("Helvetica-Bold", 10)
    
    # Title
    c.setFont("Helvetica-Bold", 14)
    c.drawString(0.5*inch, height - 0.5*inch, "Form W-2")
    c.setFont("Helvetica", 8)
    c.drawString(0.5*inch, height - 0.65*inch, "Wage and Tax Statement")
    c.drawString(0.5*inch, height - 0.8*inch, "Copy B—To Be Filed With Employee's FEDERAL Tax Return")
    
    # Year box (top right)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(width - 1.5*inch, height - 0.5*inch, "2024")
    
    # Draw main form outline
    form_top = height - 1*inch
    form_left = 0.5*inch
    form_width = width - 1*inch
    
    # Boxes a-f (Employer/Employee info section)
    c.setFont("Helvetica", 7)
    
    # Box a - Employee's SSN
    box_a_top = form_top
    c.rect(form_left, box_a_top - 0.5*inch, 2.5*inch, 0.5*inch)
    c.drawString(form_left + 0.05*inch, box_a_top - 0.15*inch, "a  Employee's social security number")
    c.setFont("Helvetica-Bold", 9)
    c.drawString(form_left + 0.05*inch, box_a_top - 0.35*inch, employee_data['ssn'])
    
    # Box b - Employer's EIN
    c.setFont("Helvetica", 7)
    c.rect(form_left + 2.5*inch, box_a_top - 0.5*inch, 2.5*inch, 0.5*inch)
    c.drawString(form_left + 2.55*inch, box_a_top - 0.15*inch, "b  Employer identification number (EIN)")
    c.setFont("Helvetica-Bold", 9)
    c.drawString(form_left + 2.55*inch, box_a_top - 0.35*inch, employee_data['employer_ein'])
    
    # Box c - Employer's name and address
    c.setFont("Helvetica", 7)
    c.rect(form_left, box_a_top - 1.5*inch, 2.5*inch, 1*inch)
    c.drawString(form_left + 0.05*inch, box_a_top - 0.65*inch, "c  Employer's name, address, and ZIP code")
    c.setFont("Helvetica", 8)
    c.drawString(form_left + 0.05*inch, box_a_top - 0.85*inch, employee_data['employer_name'])
    c.drawString(form_left + 0.05*inch, box_a_top - 1.0*inch, employee_data['employer_address'])
    c.drawString(form_left + 0.05*inch, box_a_top - 1.15*inch, 
                 f"{employee_data['employer_city']}, {employee_data['employer_state']} {employee_data['employer_zip']}")
    
    # Box d - Control number (optional, leaving blank)
    c.setFont("Helvetica", 7)
    c.rect(form_left + 2.5*inch, box_a_top - 1.5*inch, 2.5*inch, 1*inch)
    c.drawString(form_left + 2.55*inch, box_a_top - 0.65*inch, "d  Control number")
    
    # Box e - Employee's name
    c.rect(form_left, box_a_top - 2.3*inch, 2.5*inch, 0.8*inch)
    c.drawString(form_left + 0.05*inch, box_a_top - 1.65*inch, "e  Employee's first name and initial")
    c.drawString(form_left + 0.25*inch, box_a_top - 1.8*inch, "Last name")
    c.setFont("Helvetica", 8)
    c.drawString(form_left + 0.05*inch, box_a_top - 1.95*inch, 
                 f"{employee_data['first_name']} {employee_data['last_name']}")
    
    # Box f - Employee's address
    c.setFont("Helvetica", 7)
    c.rect(form_left, box_a_top - 3.5*inch, 2.5*inch, 1.2*inch)
    c.drawString(form_left + 0.05*inch, box_a_top - 2.45*inch, "f  Employee's address and ZIP code")
    c.setFont("Helvetica", 8)
    c.drawString(form_left + 0.05*inch, box_a_top - 2.65*inch, employee_data['address'])
    c.drawString(form_left + 0.05*inch, box_a_top - 2.8*inch, 
                 f"{employee_data['city']}, {employee_data['state']} {employee_data['zip']}")
    
    # Wage and tax boxes (right side)
    wage_box_left = form_left + 2.5*inch
    wage_box_width = 2.5*inch
    box_height = 0.5*inch
    
    wage_boxes = [
        ("1", "Wages, tips, other compensation", employee_data['box1_wages']),
        ("2", "Federal income tax withheld", employee_data['box2_federal_tax']),
        ("3", "Social security wages", employee_data['box3_ss_wages']),
        ("4", "Social security tax withheld", employee_data['box4_ss_tax']),
        ("5", "Medicare wages and tips", employee_data['box5_medicare_wages']),
        ("6", "Medicare tax withheld", employee_data['box6_medicare_tax']),
        ("7", "Social security tips", ""),
        ("8", "Allocated tips", ""),
    ]
    
    current_y = box_a_top - 0.5*inch
    c.setFont("Helvetica", 7)
    
    for i, (box_num, label, value) in enumerate(wage_boxes):
        # Alternate between left and right columns
        if i % 2 == 0:
            x = wage_box_left
        else:
            x = wage_box_left + wage_box_width
            
        if i > 0 and i % 2 == 0:
            current_y -= box_height
            
        c.rect(x, current_y, wage_box_width, box_height)
        c.drawString(x + 0.05*inch, current_y + box_height - 0.15*inch, f"{box_num}  {label}")
        c.setFont("Helvetica-Bold", 9)
        if value:
            c.drawRightString(x + wage_box_width - 0.05*inch, current_y + 0.15*inch, f"${value}")
        c.setFont("Helvetica", 7)
    
    # Box 12 - Codes
    current_y -= box_height
    c.rect(wage_box_left, current_y, wage_box_width * 2, box_height)
    c.drawString(wage_box_left + 0.05*inch, current_y + box_height - 0.15*inch, "12a  See instructions for box 12")
    c.setFont("Helvetica", 8)
    if employee_data['box12_codes']:
        c.drawString(wage_box_left + 0.05*inch, current_y + 0.15*inch, employee_data['box12_codes'])
    c.setFont("Helvetica", 7)
    
    # Box 13 - Checkboxes
    current_y -= box_height
    c.rect(wage_box_left, current_y, wage_box_width * 2, box_height)
    c.drawString(wage_box_left + 0.05*inch, current_y + box_height - 0.15*inch, "13")
    
    checkbox_y = current_y + 0.15*inch
    c.drawString(wage_box_left + 0.3*inch, checkbox_y, "Statutory employee")
    c.rect(wage_box_left + 0.2*inch, checkbox_y - 0.05*inch, 0.08*inch, 0.08*inch)
    
    c.drawString(wage_box_left + 1.3*inch, checkbox_y, "Retirement plan")
    c.rect(wage_box_left + 1.2*inch, checkbox_y - 0.05*inch, 0.08*inch, 0.08*inch)
    if employee_data['box13_retirement_plan'] == 'X':
        c.line(wage_box_left + 1.2*inch, checkbox_y - 0.05*inch, 
               wage_box_left + 1.28*inch, checkbox_y + 0.03*inch)
        c.line(wage_box_left + 1.28*inch, checkbox_y - 0.05*inch, 
               wage_box_left + 1.2*inch, checkbox_y + 0.03*inch)
    
    c.drawString(wage_box_left + 2.3*inch, checkbox_y, "Third-party sick pay")
    c.rect(wage_box_left + 2.2*inch, checkbox_y - 0.05*inch, 0.08*inch, 0.08*inch)
    
    # Box 14 - Other
    current_y -= box_height
    c.rect(wage_box_left, current_y, wage_box_width * 2, box_height)
    c.drawString(wage_box_left + 0.05*inch, current_y + box_height - 0.15*inch, "14  Other")
    
    # State/local tax boxes
    current_y -= box_height
    state_boxes = [
        ("15", "State", "Employer's state ID number", employee_data['box15_state'], ""),
        ("16", "State wages, tips, etc.", "", employee_data['box16_state_wages'], ""),
        ("17", "State income tax", "", employee_data['box17_state_tax'], ""),
        ("18", "Local wages, tips, etc.", "", "", ""),
        ("19", "Local income tax", "", "", ""),
        ("20", "Locality name", "", "", ""),
    ]
    
    for box_num, label1, label2, value1, value2 in state_boxes:
        if box_num in ["15", "18"]:
            # Narrower boxes for state/locality codes
            c.rect(wage_box_left, current_y, wage_box_width * 0.6, box_height)
            c.drawString(wage_box_left + 0.05*inch, current_y + box_height - 0.15*inch, f"{box_num}  {label1}")
            if label2:
                c.drawString(wage_box_left + 0.05*inch, current_y + box_height - 0.3*inch, label2)
            c.setFont("Helvetica", 8)
            if value1:
                c.drawString(wage_box_left + 0.05*inch, current_y + 0.15*inch, value1)
            c.setFont("Helvetica", 7)
            
            # Continue with next box on same row
            next_x = wage_box_left + wage_box_width * 0.6
            next_num, next_label, _, next_value, _ = state_boxes[state_boxes.index((box_num, label1, label2, value1, value2)) + 1]
            c.rect(next_x, current_y, wage_box_width * 1.4, box_height)
            c.drawString(next_x + 0.05*inch, current_y + box_height - 0.15*inch, f"{next_num}  {next_label}")
            c.setFont("Helvetica-Bold", 9)
            if next_value:
                c.drawRightString(next_x + wage_box_width * 1.4 - 0.05*inch, current_y + 0.15*inch, f"${next_value}")
            c.setFont("Helvetica", 7)
            current_y -= box_height
    
    # Disclaimer at bottom
    c.setFont("Helvetica-Bold", 12)
    c.setFillColorRGB(0.8, 0, 0)
    c.drawCentredString(width/2, 0.5*inch, "SYNTHETIC DATA: FOR TRAINING PURPOSES ONLY")
    
    # Form information footer
    c.setFillColorRGB(0, 0, 0)
    c.setFont("Helvetica", 6)
    c.drawString(0.5*inch, 0.3*inch, "Form W-2 (2024)")
    
    # Save PDF
    c.save()
    print(f"Generated: {filename}")

def generate_all_w2s(csv_file, output_dir="w2_output"):
    """
    Read CSV and generate W-2 PDFs for all employees
    
    Args:
        csv_file: Path to the CSV file containing W-2 data
        output_dir: Directory to save generated PDFs
    """
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created output directory: {output_dir}")
    
    # Read CSV and generate PDFs
    with open(csv_file, 'r') as f:
        reader = csv.DictReader(f)
        count = 0
        for row in reader:
            create_w2_pdf(row, output_dir)
            count += 1
    
    print(f"\nSuccessfully generated {count} W-2 forms in '{output_dir}' directory")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python w2_generator.py <csv_file> [output_directory]")
        print("Example: python w2_generator.py synthetic_w2_data.csv")
        sys.exit(1)
    
    csv_file = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "w2_output"
    
    if not os.path.exists(csv_file):
        print(f"Error: CSV file '{csv_file}' not found")
        sys.exit(1)
    
    generate_all_w2s(csv_file, output_dir)