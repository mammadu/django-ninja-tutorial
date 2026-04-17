"""
URL configuration for api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from datetime import date
from typing import List
from django.contrib import admin
from django.urls import path
from django.core.files.storage import FileSystemStorage
from django.shortcuts import get_object_or_404
from ninja import NinjaAPI, Schema, UploadedFile, File
from crud.models import Employee, Department

api = NinjaAPI()
STORAGE = FileSystemStorage()

class EmployeeIn(Schema):
    first_name: str
    last_name: str
    department_id: int = None
    birthdate: date = None

class EmployeeOut(Schema):
    id: int
    first_name: str
    last_name: str
    department_id: int = None
    birthdate: date = None

class DepartmentIn(Schema):
    title: str

class DepartmentOut(Schema):
    id: int
    title: str

@api.post("/departments")
def create_department(request, payload: DepartmentIn):
    payload_dict = payload.dict()
    department = Department(**payload_dict)
    department.save()
    return {"id": department.id}

@api.get("/departments", response=List[DepartmentOut])
def get_departments(request):
    departments = Department.objects.all()
    return departments

@api.put("departments/{department_id}")
def update_department(request, department_id: int, payload: DepartmentIn):
    department = get_object_or_404(Department, id=department_id)
    for attr, value in payload.dict(exclude_unset=True).items():
        setattr(department, attr, value)
    department.save()
    return {"success": True}

@api.delete("departments/{department_id}")
def delete_department(request, department_id: int):
    department = get_object_or_404(Department, id=department_id)
    department.delete()
    return {"success": True}

@api.post("/employees")
def create_employee(request, payload: EmployeeIn, cv: File[UploadedFile]):
    payload_dict = payload.dict()
    employee = Employee(**payload.dict())
    employee.cv.save(cv.name, cv)
    return {"id": employee.id}

@api.get("/employees/{employee_id}", response=EmployeeOut)
def get_employee(request, employee_id: int):
    employee = get_object_or_404(Employee, id=employee_id)
    return employee

@api.get("/employees", response=List[EmployeeOut])
def get_employees(request):
    employees = Employee.objects.all()
    return employees

@api.patch("/employees/{employee_id}")
def update_employee(request, employee_id: int, payload: EmployeeIn):
    employee = get_object_or_404(Employee, id=employee_id)
    for key, value in payload.dict(exclude_unset=True).items():
        setattr(employee, key, value)
    employee.save()
    return {"success": True}

@api.post("/upload")
def create_upload(request, cv: File[UploadedFile]):
    filename = STORAGE.save(cv.name, cv)
    # do stuff

@api.delete("employees/{employee_id}")
def delete_employee(request, employee_id: int):
    employee = get_object_or_404(Employee, id=employee_id)
    employee.delete()
    return {"success": True}


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api.urls),
]
