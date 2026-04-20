from django.test import TestCase
import csv
from pathlib import Path
from datetime import date
from .models import load_csv_to_database, CSV_Object


CURRENT_DIR: str = Path(__file__).resolve().parent
CSV_FILE_NAME: str = "customers-100.csv"
CSV_PATH: str  = CURRENT_DIR / CSV_FILE_NAME

class CSVImporterTests(TestCase):
    """
    for testing functions realted to CSV
    """
    def test_csv_and_model_object_have_same_headers(self):
        """
        make sure the headers for the db and the csv match"
        """
        csv_object_fields = [field.name for field in CSV_Object._meta.fields]

        with open(CSV_PATH, "r") as file:
            reader = csv.reader(file)
            headers = next(reader)

        # convert header to lowercase and change spaces to underscores
        for index, header in enumerate(headers):
            header = header.lower()
            header = "_".join(header.split())
            headers[index] = header

        self.assertEqual(csv_object_fields, headers)

    def test_csv_data_matches_db_data(self):
        """
        a properly formatted csv should be loaded into the database
        """
        load_csv_to_database(CSV_PATH)
        csv_objects = CSV_Object.objects.values()

        # read csv file and perform formatting for comparison to database
        csv_object_fields = [field.name for field in CSV_Object._meta.fields]
        rows = []
        with open(CSV_PATH, "r") as file:
            reader = csv.DictReader(file, fieldnames=csv_object_fields)
            next(reader) # skips the header line
            for row in reader: 
                # we must convert yyy-mm-dd to date objects
                row["index"] = int(row["index"])
                split_date = row["subscription_date"].split("-")
                row["subscription_date"] = date(*map(int, split_date))

                rows.append(row)

        for index, csv_object in enumerate(csv_objects):
            self.assertEqual(csv_object, rows[index])