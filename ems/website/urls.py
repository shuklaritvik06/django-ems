from django.urls import path
from .views import *

urlpatterns = [
    path("", home_page),
    path("add/", add_page),
    path("delete/<int:id>/", delete_page),
    path("update/<int:id>/", update_page)
]
