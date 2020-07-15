from django.urls import path
from . import views

app_name='sc'

urlpatterns=[
    path('term', views.TermList),
    path('term/create', views.CreateTerm),
    path('term/<int:termid>',views.GetTerm),
    path('load/<int:termid>',views.loadcourse)
]
