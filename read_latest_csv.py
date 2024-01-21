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

        previous_week = None
        for row in reader:
            # Assume the first column is the date in 'YYYY-MM-DD' format
            current_week = datetime.strptime(row[0], '%Y-%m-%d').isocalendar()[1]
            if previous_week is not None and current_week != previous_week:
                # Insert a visually distinct separator row
                table += "| " + " | ".join(['&nbsp;'] * len(headers)) + " |\n"
            table += "| " + " | ".join(row) + " |\n"
            previous_week = current_week

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
