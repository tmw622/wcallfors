from django.urls import path
from . import views

app_name='users'

urlpatterns=[
    path('login', views.LoginView),
    path('<int:userid>',views.LoginInfo),
    path('<slug:username>/<slug:userpwd>',views.LoginInfo)

]
