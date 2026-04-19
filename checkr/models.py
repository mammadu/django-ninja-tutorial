from django.db import models
import csv

class Customer(models.Model):
    index = models.IntegerField(primary_key=True)
    customer_id = models.CharField(max_length=15)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    city = models.CharField(max_length=200)
    country = models.CharField(max_length=100)
    phone_1 = models.CharField(max_length=50)
    phone_2 = models.CharField(max_length=50)
    email = models.EmailField()
    subscription_date = models.DateField()
    website = models.URLField()

def load_csv_to_database(csv_path: str) -> None:
    with open(csv_path, "r") as file:
        reader = csv.reader(file)
        header = next(reader)
        for row in reader:
            field_names = [field.name for field in Customer._meta.fields]
            dictionary = {field_names[i]: row[i] for i in range(len(field_names))}
            customer = Customer(**dictionary)
            customer.save()