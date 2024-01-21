import os
import csv
from datetime import datetime
import subprocess

def find_latest_csv():
    csv_files = [f for f in os.listdir('.') if f.endswith('.csv')]
    latest_file = max(csv_files, key=os.path.getmtime)
    return latest_file

def extract_month_from_filename(filename):
    base = os.path.basename(filename)
    name, ext = os.path.splitext(base)
    try:
        date = datetime.strptime(name, '%Y-%m')
        return date.strftime('%B')
    except ValueError:
        return "Unknown Month"

def csv_to_markdown_table(file_name):
    with open(file_name, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        headers = next(reader)
        table = "| " + " | ".join(headers) + " |\n"
        table += "| " + " | ".join(['---'] * len(headers)) + " |\n"
        for row in reader:
            table += "| " + " | ".join(row) + " |\n"
        return table

def update_readme(csv_file, month, table):
    with open('README.md', 'w', encoding='utf-8') as readme:
        readme.write(f"## [{month}]({csv_file})\n\n")
        readme.write(table)

def git_commit_and_push(filename, commit_message):
    subprocess.run(['git', 'add', filename], check=True)
    subprocess.run(['git', 'commit', '-m', commit_message], check=True)
    subprocess.run(['git', 'push'], check=True)

if __name__ == "__main__":
    latest_csv = find_latest_csv()
    month = extract_month_from_filename(latest_csv)
    markdown_table = csv_to_markdown_table(latest_csv)
    update_readme(latest_csv, month, markdown_table)

    git_commit_and_push('README.md', f'Update README for {month}')