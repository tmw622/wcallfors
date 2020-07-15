from django.shortcuts import render
from sc.views import Tterm

# Create your views here.

def LoginView(request):
    termlist=Tterm.objects.all()
    context={'termlist':termlist}
    return render(request,'login.html',context)

def LoginInfo(request,username,userpwd):
    print("username:",username)
    print("userpwd:",userpwd)
    return render(request,'index.html')