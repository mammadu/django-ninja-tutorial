from django.db import models


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
