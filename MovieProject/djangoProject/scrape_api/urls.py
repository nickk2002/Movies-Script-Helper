from django.urls import path

from . import views

urlpatterns = [
    path('id/<str:id>', views.find_id, name="find page"),
    path('find/<str:movie_name>', views.find_name, name="find page"),
]
