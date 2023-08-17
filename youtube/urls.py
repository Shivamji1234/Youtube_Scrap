from django.urls import path
from .views import home_page,comment

urlpatterns = [
    path('search/',home_page,name="home_page"),
    path("search/comment/",comment,name="comment")
]