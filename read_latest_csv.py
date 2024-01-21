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
        return date.strftime('%B %Y')
    except ValueError:
        return "Unknown Date"

def csv_to_markdown_table_and_totals(file_name):
    monthly_totals = {}
    table = ""

    with open(file_name, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        headers = next(reader)
        for header in headers[1:]:
            monthly_totals[header] = 0

        # Right-align all columns except the first (Day)
        table += "| " + " | ".join(headers) + " |\n"
        table += "|:---|" + "|---:" * (len(headers) - 1) + "|\n"

        for row in reader:
            date_str = row[0]
            date_obj = datetime.strptime(date_str, '%Y-%m-%d')
            week_number = date_obj.isocalendar()[1]
            day = date_obj.day

            # Right-align for odd weeks, left-align for even weeks
            day_str = f"**{day}**" if week_number % 2 != 0 else str(day)

            # Right-align all other columns
            table += "| " + day_str + " | " + " | ".join([f"{cell:>}" for cell in row[1:]]) + " |\n"
            for i, value in enumerate(row[1:], start=1):
                try:
                    monthly_totals[headers[i]] += float(value)
                except ValueError:
                    pass

    return table, monthly_totals

def update_readme(csv_file, month, data_table, monthly_totals):
    with open('README.md', 'w', encoding='utf-8') as readme:
        readme.write(f"## [{month}]({csv_file})\n\n")

        readme.write("|  | Total |\n")
        readme.write("| --- | ---: |\n")
        for identifier, total in monthly_totals.items():
            readme.write(f"| {identifier} | {total:.2f} |\n")

        readme.write("\n")
        readme.write(data_table)

if __name__ == "__main__":
    latest_csv = find_latest_csv()
    month = extract_month_and_year_from_filename(latest_csv)
    markdown_table, monthly_totals = csv_to_markdown_table_and_totals(latest_csv)
    update_readme(latest_csv, month, markdown_table, monthly_totals)
