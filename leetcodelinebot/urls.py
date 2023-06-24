from django.urls import path
from . import views

app_name = 'leetcodelinebot'

urlpatterns = [
    path('callback/', views.callback, name='callback'),
]