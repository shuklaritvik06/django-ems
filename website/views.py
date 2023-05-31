from django.shortcuts import render, redirect
from .models import Employee
from django.http import JsonResponse
from .forms import EmployeeForm, RegisterForm, LoginForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from .signals import create_user_profile, delete_user, s
from django.db.models.signals import post_save, post_delete
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.utils.text import slugify

post_save.connect(create_user_profile, sender=User)
post_delete.connect(delete_user, sender=Employee)
MOD = False


@login_required(login_url="/employee/login/")
def home_page(request):
    employees = Employee.objects.all()
    return render(request, "ems/home.html", {"employees": employees, "value": True, "mod": MOD})


@login_required(login_url="/employee/login/")
@permission_required("website.add_employee", login_url="/employee/login/", raise_exception=True)
def add_page(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST, request.FILES)
        if form.is_valid():
            employee = form.save(commit=False)

            user = User.objects.create_user(username=form.cleaned_data["emp_id"], email=form.cleaned_data["email"],
                                            password=f"ems{form.cleaned_data['emp_id']}{form.cleaned_data['name'].split(' ')[0]}",
                                            first_name=form.cleaned_data["name"].split(" ")[0],
                                            last_name=form.cleaned_data["name"].split(" ")[1])
            employee.user = user
            employee.slug = slugify(employee.name, True)
            employee.save()
            return redirect('/employee/')
    else:
        form = EmployeeForm()
    return render(request, "ems/create.html", {"form": form, "value": True})


@login_required(login_url="/employee/login/")
@permission_required("website.delete_employee", login_url="/employee/login/", raise_exception=True)
def delete_page(request, id):
    employee = Employee.objects.filter(emp_id=id).get()
    user = User.objects.filter(id=employee.user.id)
    employee.delete()
    user.delete()
    return redirect("/employee/")


@login_required(login_url="/employee/login/")
@permission_required("website.delete_employee", login_url="/employee/login/", raise_exception=True)
def update_page(request, slug):
    employee = Employee.objects.filter(slug=slug).get()
    user = User.objects.filter(id=employee.user.id).get()
    if request.method == 'POST':
        try:
            name = request.POST.get("name")
            email = request.POST.get("email")
            phone = request.POST.get("phone")
            address = request.POST.get("address")
            employee.name = name
            user.first_name = name.split(" ")[0]
            user.last_name = name.split(" ")[1]
            employee.email = email
            user.email = email
            employee.phone = phone
            employee.address = address
            employee.user = user
            user.save()
            employee.save()
            return redirect("/employee/")
        except Exception as e:
            return JsonResponse({
                "message": "error",
                "error": e.__str__()
            })
    return render(request, "ems/update.html", {"employee": employee, "value": True})


def login_form(request):
    if request.user.is_authenticated:
        return redirect("/employee/")
    form = LoginForm()
    if "login" in request.GET:
        user = authenticate(request, username=request.GET.get("username"), password=request.GET.get("password1"))
        if user is not None:
            login(request, user)
            return redirect("/employee/")
        else:
            messages.add_message(request, messages.ERROR, 'Invalid form submission.')
            for _, val in dict(form.errors).items():
                messages.add_message(request, messages.ERROR, val)
    return render(request, "accounts/login.html", {"form": form})


def register_form(request):
    if request.user.is_authenticated:
        return redirect("/employee/")
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("/employee/")
        else:
            messages.add_message(request, messages.ERROR, 'Invalid form submission.')
            for _, val in dict(form.errors).items():
                messages.add_message(request, messages.ERROR, val)
    else:
        form = RegisterForm()
    return render(request, "accounts/register.html", {"form": form})


def logout_user(request):
    logout(request)
    return redirect("/employee/login/")


def make_mod(request, id):
    user = User.objects.filter(id=id).first()
    if user and request.user.is_staff:
        try:
            group, ok = Group.objects.get_or_create(name="moderator")
            content_type = ContentType.objects.get(model='Employee')
            permission = Permission.objects.filter(content_type=content_type)
            group.permissions.add(*permission)
            group.user_set.add(user)
            global MOD
            MOD = True
            s.sendmail("ritvikshukla261@gmail.com", user.email,
                       f"Subject: Congratulations on becoming a MODERATOR!\n\nYou are promoted "
                       f"to the organization ABC as a moderator")
        except Exception as e:
            pass
    return redirect("/employee/")


def remove_mod(request, id):
    user = User.objects.filter(id=id).first()
    if user and request.user.is_staff:
        try:
            group, ok = Group.objects.get_or_create(name="moderator")
            group.user_set.remove(user)
            s.sendmail("ritvikshukla261@gmail.com", user.email,
                       f"Subject: Removed from Moderator!\n\nYou are removed "
                       f"from the position of moderator")
            global MOD
            MOD = False
        except Exception as e:
            pass
    return redirect("/employee/")


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
