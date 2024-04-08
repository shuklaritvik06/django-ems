from django.contrib import admin
from .models import Employee


class EmployeeAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "email",
        "emp_id",
        "phone",
        "designation",
        "full_time",
        "salary",
    )
    list_editable = ("email", "name", "phone", "designation", "full_time")
    list_display_links = ("salary",)
    search_fields = ("name", "email")
    search_help_text = "Enter employee name or email"
    list_per_page = 10
    list_filter = ("full_time",)


admin.site.register(Employee, EmployeeAdmin)
