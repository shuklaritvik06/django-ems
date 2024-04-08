from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from . import models


# class EmployeeForm(forms.ModelForm):
#     class Meta:
#         model = models.Employee
#         fields = "__all__"

#     def __init__(self, *args, **kwargs):
#         super(EmployeeForm, self).__init__(*args, **kwargs)
#         del self.fields["user"]
#         del self.fields["slug"]
#         for visible in self.visible_fields():
#             visible.field.widget.attrs["class"] = "form-control"


# class RegisterForm(UserCreationForm):
#     email = forms.EmailField(widget=forms.TextInput())

#     def __init__(self, *args, **kwargs):
#         super(RegisterForm, self).__init__(*args, **kwargs)
#         for visible in self.visible_fields():
#             visible.field.widget.attrs["class"] = "form-control"

#     class Meta:
#         model = User
#         fields = [
#             "username",
#             "email",
#             "first_name",
#             "last_name",
#             "password1",
#             "password2",
#         ]


# class LoginForm(UserCreationForm):
#     username = forms.CharField(widget=forms.TextInput(attrs={"name": "username"}))
#     password1 = forms.CharField(max_length=16, widget=forms.PasswordInput())

#     def __init__(self, *args, **kwargs):
#         super(LoginForm, self).__init__(*args, **kwargs)
#         del self.fields["password2"]
#         self.fields["password1"].label = "Password"
#         for visible in self.visible_fields():
#             visible.field.widget.attrs["class"] = "form-control"

#     class Meta:
#         model = User
#         fields = ["username", "password1"]


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = models.Employee
        exclude = ["user", "slug"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "picture": forms.FileInput(attrs={"class": "form-control"}),
            "emp_id": forms.NumberInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "phone": forms.TextInput(attrs={"class": "form-control"}),
            "age": forms.NumberInput(attrs={"class": "form-control"}),
            "address": forms.Textarea(attrs={"class": "form-control"}),
            "full_time": forms.Select(attrs={"class": "form-control"}),
            "designation": forms.TextInput(attrs={"class": "form-control"}),
            "salary": forms.NumberInput(attrs={"class": "form-control"}),
        }


class RegisterForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control"}))
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "type": "password",
                "placeholder": "password",
            }
        ),
    )
    password2 = forms.CharField(
        label="Confirm password",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "type": "password",
                "placeholder": "password",
            }
        ),
    )
    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "password1",
            "password2",
        ]
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
        }


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    password = forms.CharField(
        max_length=16, widget=forms.PasswordInput(attrs={"class": "form-control"})
    )

    class Meta:
        fields = ["username", "password"]
