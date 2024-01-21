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

def csv_to_markdown_table_and_summaries(file_name):
    monthly_totals = {}
    weekly_totals = {}
    table = ""

    with open(file_name, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        headers = next(reader)
        for header in headers[1:]:
            monthly_totals[header] = 0
            weekly_totals[header] = [0] * 53  # Assuming max 53 weeks in a year

        table += "| " + " | ".join(headers) + " |\n"
        table += "| " + " | ".join(['---'] * len(headers)) + " |\n"

        for row in reader:
            table += "| " + " | ".join(row) + " |\n"
            date = datetime.strptime(row[0], '%Y-%m-%d')
            week_num = date.isocalendar()[1]
            for i, value in enumerate(row[1:], start=1):
                try:
                    val = float(value)
                    monthly_totals[headers[i]] += val
                    weekly_totals[headers[i]][week_num] += val
                except ValueError:
                    pass

    # Sum weekly totals
    for client in weekly_totals:
        weekly_totals[client] = sum(weekly_totals[client])

    return table, monthly_totals, weekly_totals

def update_readme(csv_file, month, data_table, monthly_totals, weekly_totals):
    with open('README.md', 'w', encoding='utf-8') as readme:
        readme.write(f"## [{month}]({csv_file})\n\n")

        # Monthly Totals Table
        readme.write("### Monthly\n")
        readme.write("| Identifier | Total |\n")
        readme.write("| --- | ---: |\n")
        for identifier, total in monthly_totals.items():
            readme.write(f"| {identifier} | {total:.2f} |\n")

        readme.write("\n")

        # Weekly Totals Table
        readme.write("### Weekly\n")
        readme.write("| Identifier | Total |\n")
        readme.write("| --- | ---: |\n")
        for identifier, total in weekly_totals.items():
            readme.write(f"| {identifier} | {total:.2f} |\n")

        readme.write("\n")
        readme.write(data_table)

if __name__ == "__main__":
    latest_csv = find_latest_csv()
    month = extract_month_and_year_from_filename(latest_csv)
    markdown_table, monthly_totals, weekly_totals = csv_to_markdown_table_and_summaries(latest_csv)
    update_readme(latest_csv, month, markdown_table, monthly_totals, weekly_totals)
