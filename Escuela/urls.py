from django.urls import path
from . import views

urlpatterns = [
    path('profesor/', views.profesor_dashboard, name='profesor_dashboard'),
]
