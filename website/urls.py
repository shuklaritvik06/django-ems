from django.urls import path
from .views import *

urlpatterns = [
    path("", home_page),
    path("add/", add_page),
    path("delete/<int:id>/", delete_page),
    path("update/<slug:slug>/", update_page),
    path("login/", login_form),
    path("register/", register_form),
    path("logout/", logout_user),
    path("mod/add/<int:id>/", make_mod),
    path("mod/remove/<int:id>/", remove_mod),
]
