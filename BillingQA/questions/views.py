from django.shortcuts import render
from django.shortcuts import render, redirect

from django.contrib.auth import authenticate, login, logout

from django.contrib import messages 

from django.core.mail import send_mail, EmailMessage
from django.conf import settings

from smtplib import SMTPException
from datetime import datetime
from .forms import questionForm 
from .models import billingQuestion

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


    orderBy = request.GET.get('order_by', 'questionDate')
    questions = billingQuestion.objects.all().order_by(orderBy)
    return render(request, 'submitQuestion.html', {'questions':questions})
           

def showQuestions(request):
    orderBy = request.GET.get('order_by', 'questionDate')
    questions = billingQuestion.objects.all().order_by(orderBy)
    return render(request, 'showQuestions.html', {'questions':questions})


def deleteQuestion(request, question_id):
    deleteQuestion = billingQuestion.objects.get(pk = question_id)
    deleteQuesiton.delete()
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
