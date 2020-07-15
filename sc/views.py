from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.http import JsonResponse
from .models import Tterm, TSelectCourse

# Create your views here.

def TermList(request):
    return render(request,'term.html')


def CreateTerm(request):
    if request.method=="POST":
        term = Tterm()
        term.termname=request.POST.get('termname')
        term.save()
    return HttpResponseRedirect('/sc/term')

def GetTerm(request,termid):
    term=Tterm.objects.get(termid=termid)
    return HttpResponse(term.termname,content_type="text/plain")

def loadcourse(request,termid):

    term=Tterm.objects.get(termid=termid)
    sclist=TSelectCourse.objects.filter(term=term)
    courselist={}
    for sc in sclist:
        courselist[sc.course.courseid]=sc.course.coursename
    print(sclist)
    return  JsonResponse(courselist,safe=False)