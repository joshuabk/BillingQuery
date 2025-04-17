from django.shortcuts import render
from django.shortcuts import render, redirect

from django.contrib.auth import authenticate, login, logout

from django.contrib import messages 

from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from django.contrib.auth.decorators import login_required

from smtplib import SMTPException
from datetime import datetime
from .forms import questionForm, answerForm 
from .models import billingQuestion
from django.db.models import Q

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from io import BytesIO
import os
import textwrap

from django.core import mail
from django.core.mail.backends.smtp import EmailBackend

# Create your views here.


def submitQuestion(request):

    if request.method == "POST":
         form = questionForm(request.POST or None)
         if form.is_valid():
            question = form.save()


         orderBy = request.GET.get('order_by', 'Date')
         questions = billingQuestion.objects.all().order_by(orderBy)
         return render(request, 'showQuestions.html', {'questions':questions})
    else:
        return render(request, 'submitQuestion.html')       

def showQuestions(request):
    orderBy = request.GET.get('order_by', 'Date')
    questions = billingQuestion.objects.all().order_by(orderBy)
    return render(request, 'showQuestions.html', {'questions':questions})

def searchQuestions(request):
    keyword = request.POST.get('keyword')
    print(keyword)
    if keyword != "":
         
         
         orderBy = request.GET.get('order_by', 'Date')
         questions = billingQuestion.objects.all().order_by(orderBy)
         fil_questions = questions.filter(Q(Title__icontains = keyword)|Q(Content__icontains = keyword))

         return render(request, 'showQuestions.html', {'questions':fil_questions})
    else:
        return render(request, 'showQuestions.html', {'questions':questions})

def showUnanswered(request):
    orderBy = request.GET.get('order_by', 'Date')
    questions = billingQuestion.objects.get(Answered ==False).order_by(orderBy)
    
    return render(request, 'showQuestions.html', {'questions':questions})

def deleteQuestion(request, question_id):
    question = billingQuestion.objects.get(pk = question_id)
    question.delete()
    requests = billingQuestion.objects.all()
    return redirect('showQuestions')

def editQuestion(request, question_id):
    if request.method == "POST":
        question = billingQuestion.objects.get(pk = question_id)
        form = editQuestionForm(request.POST or None, instance=question)
        print(form.errors)
        if form.is_valid():
            
            messages.success(request, ('Item has been Edited'))
           
            temReq = form.save()

            requests = list(billingQuestion.objects.all())
            
            return redirect('showQuestions')
        else:
           
            print("Farts")
            messages.error(request, "Error")
            requests = billingQuestion.objects.all()
            return redirect('showQuestions')
           
    else:
        
        question = billingQuestion.objects.get(pk = question_id)
        
        return render(request, 'editQuestion.html', {'question':question})

           
def showQuestion(request, question_id):
    if request.method == "GET":
        question = billingQuestion.objects.get(pk = question_id)
        return render(request, 'showQuestion.html', {'question':question})


def loginUser(request):
    if request.method == 'POST':
        password = request.POST.get("password")
        username = request.POST.get("username")
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            messages.success(request, ('Login Successful'))
            return redirect(showQuestions)
            
        else:
            storage = messages.get_messages(request)
            storage.used = True


            messages.error(request, ('Incorrect login credentials'))
            return render(request, 'login.html')

    else:
        
        return render(request, 'login.html', {})
    
def logoutUser(request):
    logout(request)
    messages.success(request, ('You have Been Logged Out'))
    return redirect('login')

