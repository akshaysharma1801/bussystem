from django.urls import path, include
from .views import (LoginView, RegisterView)


app_name = "account"
urlpatterns = [

    path('login', LoginView.as_view()),
    path('register/', RegisterView.as_view()),

]

