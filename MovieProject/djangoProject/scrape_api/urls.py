from django.urls import path

from . import views

urlpatterns = [
    path('find/<int:id>', views.find, name="find page"),
]
