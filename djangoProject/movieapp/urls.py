from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name="home page"),
    path('movie/<int:id>', views.movie, name="movie view"),
    path("advanced/", views.advanced_search, name="advanced search")
]
