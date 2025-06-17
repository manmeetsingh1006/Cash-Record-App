import unittest
import os
import csv
import sys

# Add project root to sys.path to allow importing data_manager
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import data_manager

class TestDataManager(unittest.TestCase):

    def setUp(self):
        self.test_csv_file = 'test_records.csv'
        # IMPORTANT: Override the RECORDS_FILE in the data_manager module
        data_manager.RECORDS_FILE = self.test_csv_file

        # Ensure a clean slate for each test by creating an empty file with only headers
        with open(self.test_csv_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["date", "description", "type", "amount"])

    def tearDown(self):
        # Clean up the test file after each test
        if os.path.exists(self.test_csv_file):
            os.remove(self.test_csv_file)

    def test_add_record(self):
        data_manager.add_record("2023-10-26", "Test Expense", "expense", "50.00")

        with open(self.test_csv_file, 'r', newline='') as f:
            reader = csv.reader(f)
            lines = list(reader)

        # Expected: Header + 1 record
        self.assertEqual(len(lines), 2, "CSV file should have 2 lines (header + 1 record)")
        self.assertEqual(lines[0], ["date", "description", "type", "amount"], "Header row is incorrect")
        self.assertEqual(lines[1], ["2023-10-26", "Test Expense", "expense", "50.00"], "Added record data is incorrect")

        # Also test via view_records to ensure it's readable by the system
        records = data_manager.view_records()
        self.assertEqual(len(records), 1, "view_records should return 1 record")
        self.assertEqual(records[0]['date'], "2023-10-26")
        self.assertEqual(records[0]['description'], "Test Expense")
        self.assertEqual(records[0]['type'], "expense")
        self.assertEqual(records[0]['amount'], "50.00")


    def test_view_records_empty(self):
        # setUp creates a file with only a header. view_records should return empty list.
        records = data_manager.view_records()
        self.assertEqual(len(records), 0, "view_records should return an empty list for a header-only file")

    def test_view_records_with_data(self):
        data_manager.add_record("2023-01-01", "Coffee", "expense", "3.50")
        data_manager.add_record("2023-01-02", "Salary", "income", "500.00")

        records = data_manager.view_records()
        self.assertEqual(len(records), 2, "view_records should return 2 records")

        self.assertEqual(records[0]['date'], "2023-01-01")
        self.assertEqual(records[0]['description'], "Coffee")
        self.assertEqual(records[0]['type'], "expense")
        self.assertEqual(records[0]['amount'], "3.50")

        self.assertEqual(records[1]['date'], "2023-01-02")
        self.assertEqual(records[1]['description'], "Salary")
        self.assertEqual(records[1]['type'], "income")
        self.assertEqual(records[1]['amount'], "500.00")

    def test_view_records_file_not_found(self):
        # Ensure the file is deleted before calling view_records
        if os.path.exists(self.test_csv_file):
            os.remove(self.test_csv_file)

        records = data_manager.view_records()
        self.assertEqual(len(records), 0, "view_records should return an empty list if the file does not exist")

    def test_add_multiple_records(self):
        data_manager.add_record("2024-01-01", "Groceries", "expense", "75.20")
        data_manager.add_record("2024-01-01", "Freelance Gig", "income", "250.00")
        data_manager.add_record("2024-01-02", "Dinner Out", "expense", "45.50")

        records = data_manager.view_records()
        self.assertEqual(len(records), 3)

        self.assertEqual(records[0]['description'], "Groceries")
        self.assertEqual(records[1]['description'], "Freelance Gig")
        self.assertEqual(records[2]['description'], "Dinner Out")

        with open(self.test_csv_file, 'r', newline='') as f:
            reader = csv.reader(f)
            lines = list(reader)
        self.assertEqual(len(lines), 4, "CSV file should have 4 lines (header + 3 records)")


if __name__ == '__main__':
    unittest.main()
