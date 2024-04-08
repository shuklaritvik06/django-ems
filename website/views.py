from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.mail import send_mail
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required, permission_required
from .forms import LoginForm, RegisterForm, EmployeeForm
from .models import Employee

MOD = False

@login_required(login_url="/employee/login/")
def home_page(request):
    employees = Employee.objects.all()
    return render(
        request, "ems/home.html", {"employees": employees, "value": True, "mod": MOD}
    )


@login_required(login_url="/employee/login/")
@permission_required(
    "website.add_employee", login_url="/employee/login/", raise_exception=True
)
def add_page(request):
    if request.method == "POST":
        form = EmployeeForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                employee = form.save(commit=False)
                user = User.objects.create_user(
                    username=form.cleaned_data["emp_id"],
                    email=form.cleaned_data["email"],
                    password=f"ems{form.cleaned_data['emp_id']}{form.cleaned_data['name'].split(' ')[0]}",
                    first_name=(
                        form.cleaned_data["name"].split(" ")[0]
                        if len(form.cleaned_data["name"].split(" ")) > 2
                        else ""
                    ),
                    last_name=(
                        form.cleaned_data["name"].split(" ")[1:]
                        if len(form.cleaned_data["name"].split(" ")) > 2
                        else ""
                    ),
                )
                employee.user = user
                employee.slug = slugify(employee.name, True)
                employee.save()
                return redirect("/employee/")
            except Exception as e:
                messages.error(request, f"Error occurred: {e}")
    else:
        form = EmployeeForm()
    return render(request, "ems/create.html", {"form": form, "value": True})


@login_required(login_url="/employee/login/")
@permission_required(
    "website.delete_employee", login_url="/employee/login/", raise_exception=True
)
def delete_page(request, id):
    employee = Employee.objects.filter(emp_id=id).first()
    if employee:
        try:
            user = User.objects.filter(id=employee.user.id).first()
            if user:
                employee.delete()
                user.delete()
        except Exception as e:
            messages.error(request, f"Error occurred: {e}")
    return redirect("/employee/")


@login_required(login_url="/employee/login/")
@permission_required(
    "website.delete_employee", login_url="/employee/login/", raise_exception=True
)
def update_page(request, slug):
    employee = Employee.objects.filter(slug=slug).first()
    if employee:
        user = User.objects.filter(id=employee.user.id).first()
        if request.method == "POST":
            try:
                name = request.POST.get("name")
                email = request.POST.get("email")
                phone = request.POST.get("phone")
                address = request.POST.get("address")
                employee.name = name
                user.first_name = name.split(" ")[0]
                user.last_name = name.split(" ")[1:]
                employee.email = email
                user.email = email
                employee.phone = phone
                employee.address = address
                employee.user = user
                user.save()
                employee.save()
                return redirect("/employee/")
            except Exception as e:
                messages.error(request, f"Error occurred: {e}")
    return render(request, "ems/update.html", {"employee": employee, "value": True})


def login_form(request):
    if request.user.is_authenticated:
        return redirect("/employee/")
    form = LoginForm()
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/employee/")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid form submission.")
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    return render(request, "accounts/login.html", {"form": form})


def register_form(request):
    if request.user.is_authenticated:
        return redirect("/employee/")
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                login(request, user)
                return redirect("/employee/")
            except Exception as e:
                messages.error(request, f"Error occurred: {e}")
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
            content_type = ContentType.objects.get(model="Employee")
            # can_update = Permission.objects.get(name='can_update_employee')
            # group.permissions.add(can_update)
            permission = Permission.objects.filter(content_type=content_type)
            group.permissions.add(*permission)
            group.user_set.add(user)
            global MOD
            MOD = True
            send_mail(
                "Congratulations on becoming a MODERATOR!",
                f"You are promoted to the organization ABC as a moderator",
                "ritvikshukla261@gmail.com",
                [user.email],
                fail_silently=False,
            )
        except Exception as e:
            messages.error(request, f"Error occurred: {e}")
    return redirect("/employee/")


def remove_mod(request, id):
    user = User.objects.filter(id=id).first()
    if user and request.user.is_staff:
        try:
            group, ok = Group.objects.get_or_create(name="moderator")
            group.user_set.remove(user)
            send_mail(
                "Removed from Moderator!",
                f"You are removed from the position of moderator",
                "ritvikshukla261@gmail.com",
                [user.email],
                fail_silently=False,
            )
            global MOD
            MOD = False
        except Exception as e:
            messages.error(request, f"Error occurred: {e}")
    return redirect("/employee/")
