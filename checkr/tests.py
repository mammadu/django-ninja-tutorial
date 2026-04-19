from django.test import TestCase
import csv
from pathlib import Path
from datetime import date
from .models import Customer, load_csv_to_database

from django.forms.models import model_to_dict


CURRENT_DIR: str = Path(__file__).resolve().parent
CSV_PATH: str  = CURRENT_DIR / "customers-100.csv"

class CSVImporterTests(TestCase):
    """
    for testing functions realted to CSV
    """
    def test_csv_and_model_object_have_same_headers(self):
        """
        make sure the headers for the db and the csv match"
        """
        customer_fields = [field.name for field in Customer._meta.fields]

        with open(CSV_PATH, "r") as file:
            reader = csv.reader(file)
            headers = next(reader)

        # convert header to lowercase and change spaces to underscores
        for index, header in enumerate(headers):
            header = header.lower()
            header = "_".join(header.split())
            headers[index] = header

        self.assertEqual(customer_fields, headers)

    def test_csv_data_matches_db_data(self):
        """
        a properly formatted csv should be loaded into the database
        """
        load_csv_to_database(CSV_PATH)
        customers = Customer.objects.values()

        customer_fields = [field.name for field in Customer._meta.fields]
        rows = []
        with open(CSV_PATH, "r") as file:
            reader = csv.DictReader(file, fieldnames=customer_fields)
            headers = next(reader)
            for row in reader:
                row["index"] = int(row["index"])
                split_date = row["subscription_date"].split("-")
                row["subscription_date"] = date(*map(int, split_date))
                rows.append(row)
        for index, customer in enumerate(customers):
            self.assertEqual(customer, rows[index])