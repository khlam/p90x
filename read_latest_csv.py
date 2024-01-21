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

def csv_to_markdown_table(file_name):
    with open(file_name, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        headers = next(reader)
        table = "| " + " | ".join(headers) + " |\n"
        table += "| " + " | ".join(['---'] * len(headers)) + " |\n"
        for row in reader:
            try:
                # Parse and reformat the date in the first column
                date = datetime.strptime(row[0], '%Y-%m-%d')
                row[0] = date.strftime('%B %d')
            except ValueError:
                # If parsing fails, leave the date as is
                pass
            table += "| " + " | ".join(row) + " |\n"
        return table

def update_readme(csv_file, month, table):
    with open('README.md', 'w', encoding='utf-8') as readme:
        readme.write(f"## [{month}]({csv_file})\n\n")
        readme.write(table)

if __name__ == "__main__":
    latest_csv = find_latest_csv()
    month_year = extract_month_and_year_from_filename(latest_csv)  # Updated function call
    markdown_table = csv_to_markdown_table(latest_csv)
    update_readme(latest_csv, month_year, markdown_table)
