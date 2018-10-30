from django.shortcuts import render
from django.http import HttpResponse
from .models import Question
from django.template import loader

def read(i):
    f=open('D:/true/diary/read/hw%s.txt'% i,'r')
    x=f.read()
    return x
  
def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'read/index.html', context)

def detail(request, question_id):
    return HttpResponse(read(question_id))
    #latest_question_list = Question.contain
    #context = {'latest_question_list': latest_question_list}
    #return render(request, 'read/index.html', context)

def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)


# Create your views here.
    

