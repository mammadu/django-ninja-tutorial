from django.core.management.base import BaseCommand, CommandError
from django.apps import apps
import csv

"""
This module is used to create a command to ingest csv files into the database
expected format of the command is `python manage.py ingest_csv model_name, csv_file`
"""

class Command(BaseCommand):
    help = "Ingests csv_file of type MODEL_NAME into the database"

    def load_csv_to_database(self, app_name: str, model_name: str, csv_path: str) -> None:
        model = apps.get_model(app_name, model_name)
        with open(csv_path, "r") as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                field_names = [field.name for field in model._meta.fields]
                dictionary = {field_names[i]: row[i] for i in range(len(field_names))}
                csv_object = model(**dictionary)
                csv_object.save()

    def add_arguments(self, parser):
        parser.add_argument("-a", "--app", default="checkr_project")
        parser.add_argument("model", help="the model from models.py that has the csv structure")
        parser.add_argument("path_to_csv", help="path to csv file")

    def handle(self, *args, **options):
        try:
            app_name = options["app"]
            model_name = options["model"]
            csv_path = options["path_to_csv"]
            self.load_csv_to_database(app_name, model_name, csv_path)
            self.stdout.write("successfully loaded csv into database")
        except Exception as e:
            self.stdout.write(f"could not load csv into database: {e}")
