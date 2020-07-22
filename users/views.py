from django.shortcuts import render,HttpResponseRedirect
from sc.views import Tterm
from users.models import TUser
from .UserForm import UserForm
from sc.models import TSelectCourse,Tcourse
# Create your views here.

def LoginView(request):
    termlist=Tterm.objects.all()
    userform=UserForm()
    context={'termlist':termlist,'userform':userform}
    return render(request,'login.html',context)

def LoginAction(request):
    if request.method == "POST":
        form=UserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            userpwd = form.cleaned_data['userpwd']
            termid = request.POST.get('term')
            courseid = request.POST.get('course')

            user = TUser.objects.filter(username=username,userpwd=userpwd)
            if len(user) > 0 :
                request.session['username'] = user[0].username
                request.session['userid'] = user[0].userid
                request.session['termid'] = termid
                request.session['courseid'] = courseid
                term=Tterm.objects.get(termid=termid)
                course=Tcourse.objects.get(courseid=courseid)
                sc=TSelectCourse.objects.get(term=term,course=course)
                request.session['scid'] = sc.scid
                return render(request, 'index.html')
            else:
                return HttpResponseRedirect('/users/login')
    else:
        return HttpResponseRedirect('/users/login')

def logout(request):
    del request.session['username']
    del request.session['userid']
    del request.session['termid']
    del request.session['courseid']

    return HttpResponseRedirect('/users/login')
