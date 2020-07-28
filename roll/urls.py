from django.urls import path

from . import views


app_name='roll'
urlpatterns=[
    path('importstu',views.importstu),
    path('uploadstu',views.upload),
    path('getstulist',views.getstulist),
    path('scall',views.precall),
    path('hiscall/<int:calldateid>',views.hiscall),
    path('startcall/<int:calldateid>',views.startcall),
    path('loadsign/<int:calldateid>',views.loadsign),
    path('stusign/<slug:stuno>',views.stusign),
    path('stopcall',views.stopcall)
]

