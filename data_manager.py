import csv
import os

RECORDS_FILE = 'records.csv'

def add_record(date, description, type, amount):
    """Appends a new record to the CSV file."""
    try:
        with open(RECORDS_FILE, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([date, description, type, amount])
    except Exception as e:
        print(f"Error adding record: {e}")

def view_records():
    """Reads all records from the CSV file and returns them as a list of dictionaries."""
    records = []
    try:
        if not os.path.exists(RECORDS_FILE) or os.path.getsize(RECORDS_FILE) == 0:
            print("No records found or record file is empty.")
            return records

        with open(RECORDS_FILE, 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            # Check if the file only contains the header
            if not reader.fieldnames:
                 print("Record file is empty/corrupted.")
                 return records
            for row in reader:
                records.append(row)

            # Handle case where file has header but no data
            if not records and reader.line_num <=1:
                 print("No records found.")

    except FileNotFoundError:
        print(f"Record file not found: {RECORDS_FILE}")
    except Exception as e:
        print(f"Error viewing records: {e}")
    return records
