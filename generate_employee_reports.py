import os
import pandas as pd
from fpdf import FPDF

# Function to read Excel data
def read_excel(file_path):
    try:
        data = pd.read_excel(file_path, sheet_name=None)
        return data
    except Exception as e:
        print(f"Error reading Excel file: {e}")
        return None

# Create folder if it doesn't exist
def create_folder(folder_name):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

# Function to generate the PDF report
def generate_report(person_data, purchase_data, output_path):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Add company logo and name
    pdf.image("assets/logo.png", x=10, y=8, w=33)  # Adjust the path and size as needed
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="AVINESH MASIH PROJECT ", ln=True, align="C")
    pdf.ln(20)

    pdf.cell(200, 10, txt="Personal Report", ln=True, align="C")
    pdf.ln(10)

    # Add formatted table with employee details
    pdf.set_font("Arial", size=10)
    pdf.set_fill_color(200, 220, 255)
    pdf.cell(40, 10, 'Name', border=1, align='C', fill=True)
    pdf.cell(20, 10, 'Age', border=1, align='C', fill=True)
    pdf.cell(40, 10, 'Department', border=1, align='C', fill=True)
    pdf.cell(60, 10, 'Job Title', border=1, align='C', fill=True)
    pdf.cell(30, 10, 'Salary (INR)', border=1, align='C', fill=True)
    pdf.ln()

    for index, row in person_data.iterrows():
        pdf.cell(40, 10, row['Employee Name'], border=1, align='C')
        pdf.cell(20, 10, str(row['Age']), border=1, align='C')
        pdf.cell(40, 10, row['Department'], border=1, align='C')
        pdf.cell(60, 10, row['Job Title'], border=1, align='C')
        pdf.cell(30, 10, str(row['Salary (INR)']), border=1, align='C')
        pdf.ln()

    pdf.ln(10)
    pdf.cell(200, 10, txt="Item Purchase Details", ln=True, align="C")
    pdf.ln(5)

    # Add formatted table with purchase details
    pdf.set_font("Arial", size=10)
    pdf.set_fill_color(200, 220, 255)
    pdf.cell(60, 10, 'Item Purchased', border=1, align='C', fill=True)
    pdf.cell(40, 10, 'Quantity', border=1, align='C', fill=True)
    pdf.cell(40, 10, 'Price (INR)', border=1, align='C', fill=True)
    pdf.cell(50, 10, 'Total Cost (INR)', border=1, align='C', fill=True)
    pdf.ln()

    for index, row in purchase_data.iterrows():
        pdf.cell(60, 10, row['Item Purchased'], border=1, align='C')
        pdf.cell(40, 10, str(row['Quantity']), border=1, align='C')
        pdf.cell(40, 10, str(row['Price (INR)']), border=1, align='C')
        pdf.cell(50, 10, str(row['Total Cost (INR)']), border=1, align='C')
        pdf.ln()

    # Output the PDF
    pdf.output(output_path)

# Main function
def main():
    excel_file = "assets\employees.xlsx"  # Replace with your file path
    data = read_excel(excel_file)

    if data is None:
        print("Failed to load data.")
        return

    # Extract employee data and item purchase data
    employee_data = data['Employee Data']
    purchase_data = data['Item Purchases']

    # Ensure the column names are correct
    print("Employee Data Columns:", employee_data.columns)
    print("Purchase Data Columns:", purchase_data.columns)

    overwrite_all = False

    # Create a folder for each employee and generate their reports
    for index, row in employee_data.iterrows():
        person_name = row['Employee Name']  # Employee name is used as folder name
        folder_name = f"reports/{person_name}"
        create_folder(folder_name)

        # Generate the PDF report with employee details
        report_path = os.path.join(folder_name, f"{person_name}_report.pdf")
        
        if os.path.exists(report_path) and not overwrite_all:
            overwrite = input(f"The report for {person_name} already exists. Do you want to overwrite it? (yes/no/all): ")
            if overwrite.lower() == 'no':
                print(f"Skipping report generation for {person_name}.")
                continue
            elif overwrite.lower() == 'all':
                overwrite_all = True

        generate_report(employee_data[employee_data['Employee Name'] == person_name], purchase_data, report_path)

        print(f"Report generated for {person_name} at {report_path}")

if __name__ == "__main__":
    main()
