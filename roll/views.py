from django.shortcuts import render
from django.shortcuts import render,HttpResponseRedirect, HttpResponse
from django.http import JsonResponse
import pandas as pd
from sc.models import TSelectCourse, Tterm,Tcourse
from .models import Tstudent, Tcallrec,Tcalldate

# Create your views here.

def getext(filename):
    strlist=filename.split('.')
    return strlist[len(strlist)-1]

def upload(request):
    return render(request,'batimport.html')


def importstu(request):
    if request.method == "POST":
        file = request.FILES.get('stulist')
        print(file.name)
        type_excel = getext(file.name)
        print(type_excel)
        if 'xlsx' == type_excel or 'xls'==type_excel:
            stulist=pd.read_excel(file)
            rows=len(stulist)
            termid=request.session.get('termid')
            courseid=request.session.get('courseid')
            term = Tterm.objects.get(termid=termid)
            course = Tcourse.objects.get(courseid=courseid)
            sc=TSelectCourse.objects.filter(term=term,course=course)
            for i in range(rows):
                scid=sc[0].scid
                stuname=stulist['studentname'][i]
                stuno=stulist['studentid'][i]
                student = Tstudent()
                student.stuno=stuno
                student.stuname=stuname
                student.selectcourse=sc[0]
                student.save()
            return HttpResponseRedirect('/static/popclose.html')


def getstulist(request):
    termid = request.session.get('termid')
    courseid = request.session.get('courseid')
    term=Tterm.objects.get(termid=termid)
    course=Tcourse.objects.get(courseid=courseid)

    sc = TSelectCourse.objects.filter(term=term, course=course)
    scid=sc[0].scid
    stulist=Tstudent.objects.filter(selectcourse=sc[0])

    return render(request,'call.html',{'stulist':stulist,'scid':scid})

def precall(request):
    scid= request.session.get('scid')
    context=Tcallrec.InitialSign(scid)
    return render(request,'scall.html',context)

def hiscall(request,calldateid):
    scid=request.session.get('scid')
    context=Tcallrec.callhis(scid,calldateid)

    maxid=context.get('calldateid')
    statistic=Tcallrec.statics(maxid)
    context=dict(context,**statistic)
    return render(request,'hiscall.html',context)






