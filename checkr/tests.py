import csv
from pathlib import Path
from django.test import TestCase
from .models import Customer


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

    # def test_csv_data_matches_db_data(self, )