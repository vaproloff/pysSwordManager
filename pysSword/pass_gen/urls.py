from django.urls import path
from .views import password_generator, pass_gen_api

urlpatterns = [
    path('', password_generator, name='generator'),
    path('generate/', pass_gen_api, name='pass_gen_api'),
]