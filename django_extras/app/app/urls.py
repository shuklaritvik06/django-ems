"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("project.urls")),
    path("user/", include("user.urls")),
    path('password_reset/', PasswordResetView.as_view(template_name="reset.html"), name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(template_name="done.html"), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name="confirm.html"), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(template_name="complete.html"), name='password_reset_complete'),
]
