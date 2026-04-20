from ninja import NinjaAPI, Schema, FilterSchema, Query, ModelSchema
from pydantic import Field
from typing import Optional
from .models import CSV_Object
from django.core.serializers import serialize
import datetime

class CustomerFilterSchema(FilterSchema):
    first_name: Optional[str] = Field(None, q="first_name__icontains")
    last_name: Optional[str] = Field(None, q="last_name__icontains")
    country: Optional[str] = None
    subscription_date: Optional[datetime.date] = None
    subscription_year: Optional[int] = Field(None, q="subscription_date__year")
    subscription_month: Optional[int] = Field(None, q="subscription_date__month")
    subscription_day: Optional[int] = Field(None, q="subscription_date__day")

# class CustomerOut(Schema):
#     index: int
#     customer_id: str
#     first_name: str
#     last_name: str
#     company: str
#     city: str
#     country: str
#     phone_1: str
#     phone_2: str
#     email: str
#     subscription_date: datetime
#     website: str

class CustomerOut(ModelSchema):
    class Meta:
        model = CSV_Object
        # fields = "__all__"
        fields = ['first_name', 'last_name', 'company', 'city', 'country', 'phone_1', 'phone_2', 'email', 'subscription_date', 'website']

api = NinjaAPI()

@api.get("/customers", response=list[CustomerOut])
def get_customers(request, filters: CustomerFilterSchema = Query(...)):
    customers = CSV_Object.objects.all()
    customers = filters.filter(customers)
    return customers
