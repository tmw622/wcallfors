from django.urls import path
from . import views

app_name='users'

urlpatterns=[
    path('login', views.LoginView),
    path('LoginAction',views.LoginAction),
    path('logout',views.logout)
]
