from django.shortcuts import render, redirect
from .models import Employee
from django.http import JsonResponse
from .forms import EmployeeForm


def home_page(request):
    employees = Employee.objects.all()
    return render(request, "ems/home.html", {"employees": employees})


def add_page(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect('/employee/')
    else:
        form = EmployeeForm()
    return render(request, "ems/create.html", {"form": form})


def delete_page(request, id):
    employee = Employee.objects.filter(emp_id=id)
    employee.delete()
    return redirect("/employee/")


def update_page(request, id):
    employee = Employee.objects.filter(emp_id=id).get()
    if request.method == 'POST':
        try:
            name = request.POST.get("name")
            emp_id = request.POST.get("emp_id")
            email = request.POST.get("email")
            phone = request.POST.get("phone")
            age = int(request.POST.get("age"))
            address = request.POST.get("address")
            full_time = request.POST.get("full_time")
            designation = request.POST.get("designation")
            salary = int(request.POST.get("salary"))
            employee.name = name
            employee.email = email
            employee.emp_id = emp_id
            employee.phone = phone
            employee.age = age
            employee.address = address
            employee.full_time = full_time
            employee.designation = designation
            employee.salary = salary
            employee.save()
            return redirect("/employee/")
        except Exception as e:
            return JsonResponse({
                "message": "error",
                "error": e.__str__()
            })
    return render(request, "ems/update.html", {"employee": employee})


# try:
#     name = request.POST.get("name")
#     emp_id = request.POST.get("emp_id")
#     email = request.POST.get("email")
#     phone = request.POST.get("phone")
#     age = int(request.POST.get("age"))
#     address = request.POST.get("address")
#     if request.POST.get("full_time") == "Yes":
#         full_time = True
#     else:
#         full_time = False
#     designation = request.POST.get("designation")
#     salary = int(request.POST.get("salary"))
#     employee = Employee(name=name, emp_id=emp_id, email=email, phone=phone, age=age, address=address,
#                         full_time=full_time, designation=designation, salary=salary)
#     employee.save()
#     return redirect("/employee/")
# except Exception as e:
#     return JsonResponse({
#         "message": "error",
#         "error": e.__str__()
#     })
