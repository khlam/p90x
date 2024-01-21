import os
import csv
from datetime import datetime

def find_latest_csv():
    csv_files = [f for f in os.listdir('.') if f.endswith('.csv')]
    latest_file = max(csv_files, key=os.path.getmtime)
    return latest_file

def extract_month_and_year_from_filename(filename):
    base = os.path.basename(filename)
    name, ext = os.path.splitext(base)
    try:
        date = datetime.strptime(name, '%Y-%m')
        return date.strftime('%B %Y')  # Format changed to include the year
    except ValueError:
        return "Unknown Date"

def csv_to_markdown_table_and_monthly_earnings(file_name):
    monthly_earnings = {}
    table = ""

    with open(file_name, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        headers = next(reader)
        # Initialize monthly earnings for each client, skipping the first column
        for header in headers[1:]:
            monthly_earnings[header] = 0

        # Markdown table headers
        table += "| " + " | ".join(headers) + " |\n"
        table += "| " + " | ".join(['---'] * len(headers)) + " |\n"

        for row in reader:
            table += "| " + " | ".join(row) + " |\n"
            # Sum earnings for each client, skipping the first column (date)
            for i, earning in enumerate(row[1:], start=1):
                try:
                    monthly_earnings[headers[i]] += float(earning)
                except ValueError:
                    pass  # Ignore if conversion to float fails or field is empty

    return table, monthly_earnings

def update_readme(csv_file, month, table, monthly_earnings):
    with open('README.md', 'w', encoding='utf-8') as readme:
        readme.write(f"## [{month}]({csv_file})\n\n")
        # Print monthly earnings, excluding the "date" column
        for client, earning in monthly_earnings.items():
            readme.write(f"**{client}:** {earning:.2f}\n")
        readme.write("\n")
        readme.write(table)

if __name__ == "__main__":
    latest_csv = find_latest_csv()
    month = extract_month_and_year_from_filename(latest_csv)
    markdown_table, monthly_earnings = csv_to_markdown_table_and_monthly_earnings(latest_csv)
    update_readme(latest_csv, month, markdown_table, monthly_earnings)
