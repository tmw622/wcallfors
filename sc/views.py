from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.http import JsonResponse
from .models import Tterm, TSelectCourse

# Create your views here.

def TermList(request):
    termlist=Tterm.objects.all()
    context={"termlist":termlist}
    return render(request,'term.html',context)

def CreateTerm(request):
    if request.session.get('username')==None:
        return HttpResponseRedirect('/users/login')

    if request.method=="POST":
        term = Tterm()
        term.termname=request.POST.get('termname')
        term.save()
    return HttpResponseRedirect('/sc/term')

def GetTerm(request,termid):
    term=Tterm.objects.get(termid=termid)
    context={'term':term}
    return render(request,'termedit.html',context)

def loadcourse(request,termid):
    term=Tterm.objects.get(termid=termid)
    sclist=TSelectCourse.objects.filter(term=term)
    courselist={}
    for sc in sclist:
        courselist[sc.course.courseid]=sc.course.coursename
    print(sclist)
    return  JsonResponse(courselist,safe=False)

def EditTerm(request):
    if request.session.get('username')==None:
        return HttpResponseRedirect('/users/login')

    termid=request.POST.get('termid')
    termname=request.POST.get('termname')
    term=Tterm.objects.get(termid=termid)
    term.termname=termname
    term.save()
    return HttpResponseRedirect('/static/popclose.html')

def DelTerm(request,termid):
    if request.session.get('username')==None:
        return HttpResponseRedirect('/users/login')

    term=Tterm.objects.get(termid=termid)
    term.delete()
    return HttpResponseRedirect('/sc/term')