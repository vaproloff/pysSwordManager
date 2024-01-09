from django.urls import path
from .views import password_generator

urlpatterns = [
    path('', password_generator, name='generator'),
]