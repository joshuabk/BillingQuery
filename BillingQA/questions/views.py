from django.shortcuts import render
from django.shortcuts import render, redirect

from django.contrib.auth import authenticate, login, logout

from django.contrib import messages 

from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from django.contrib.auth.decorators import login_required

from smtplib import SMTPException
from datetime import datetime
from .forms import questionForm, answerForm, submitPDFForm, editPDFForm, editQuestionForm 
from .models import billingQuestion, billingPDF
from django.db.models import Q
import spacy
import numpy as np
from django.db.models import Case, When

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
#login
#user: billing
#pass: northside1

def submitQuestion(request):

    if request.method == "POST":
         form = questionForm(request.POST or None)
         if form.is_valid():
            question = form.save()


            orderBy = request.GET.get('order_by', 'Date')
            questions = billingQuestion.objects.all().order_by(orderBy)
            return render(request, 'submissionSuccess.html')
         print("there has been an error")
         print(form.errors)
         return render(request, 'submitQuestion.html')
    else:

        return render(request, 'submitQuestion.html')  

def submitPDF(request):

    if request.method == "POST":
         form = submitPDFForm(request.POST, request.FILES)
         if form.is_valid():
            pdfDoc = form.save()


            #orderBy = request.GET.get('order_by', 'Date')
            pdfs = billingPDF.objects.all()
            return render(request, 'submissionSuccessDoc.html')
            print("there has been an error")
            print(form.errors)
            return render(request, 'showPDFs.html')
    else:

        return render(request,'submitPDF.html')  

def showQuestions(request):
    orderBy = request.GET.get('order_by', 'Date')
    questions = billingQuestion.objects.filter(Answered = True).order_by(orderBy)
    type = " "
    return render(request, 'showQuestions.html', {'questions':questions, 'type': type, 'search_phrase': ''})

def showPDFs(request):
    orderBy = request.GET.get('order_by', 'Category')
    docs = billingPDF.objects.filter().order_by(orderBy)
    category = " "
    return render(request, 'showPDFs.html', {'docs':docs, 'category': category})


def searchQuestionsUnanswered(request):
    keyword = request.POST.get('keyword')
    print(keyword)
    orderBy = request.GET.get('order_by', 'Date')
    questions = billingQuestion.objects.filter(Answered = False).order_by(orderBy)
    if keyword != "":
         
         fil_questions = questions.filter(Q(Title__icontains = keyword)|Q(Content__icontains = keyword))

         return render(request, 'showUnanswered.html', {'questions':fil_questions})
    else:
        return redirect('showUnanswered')

def wordEmbedSearch(search_phrase, questions):
    nlp = spacy.load("en_core_web_lg")
    questionsL = list(questions)
    question_ids = [q.id  for q in questionsL]
    questionsC = [q.Content for q in questionsL]
    question_vectors = [nlp(q).vector for q in questionsC]
    search_vector = nlp(search_phrase).vector
    similarities = [np.dot(search_vector, qv) / (np.linalg.norm(search_vector) * np.linalg.norm(qv)) for qv in question_vectors]
    n = 4
    top_indices = np.argsort(similarities)[::-1][:n]
    top_question_ids = [question_ids[i] for i in top_indices if question_ids[i]]
    preserved_order = Case(*[When(id=pk, then=pos) for pos, pk in enumerate(top_question_ids)])
    top_questions = billingQuestion.objects.filter(id__in=top_question_ids).order_by(preserved_order)
    print(top_questions)
    return top_questions



def searchQuestionsAnswered(request, type):
    keyword = request.POST.get('keyword')
    
    print(keyword)
    orderBy = request.GET.get('order_by', 'Date')
    if type != " ":
        questions = billingQuestion.objects.filter(Answered = True, Type = type).order_by(orderBy)
    else:
        questions = billingQuestion.objects.filter(Answered = True,).order_by(orderBy)
    if keyword != "":
         
         fil_questions = questions.filter(Q(Title__icontains = keyword)|Q(Content__icontains = keyword))
         top_questions = wordEmbedSearch(keyword, questions)
         return render(request, 'showQuestions.html', {'questions':top_questions, 'type': type, 'search_phrase': keyword})
    else:
        
        return render(request,'showQuestions.html', {'questions':questions, 'type': type, 'search_phrase': ''})
    

def searchPDFs(request, category):
    keyword = request.POST.get('keyword')
    
    print(keyword)
    orderBy = request.GET.get('order_by', 'Date')
    if category != " ":
        docs = billingPDF.objects.filter(Category = category).order_by(orderBy)
    else:
        docs = billingPDF.objects.filter().order_by(orderBy)
    if keyword != "":
         
         fil_docs = docs.filter(Q(Title__icontains = keyword))

         return render(request, 'showPDFs.html', {'docs':fil_docs, 'category': category})
    else:
        return render(request, 'showPDFs.html', {'docs':docs, 'category': category})

def filterType(request):
    type = request.POST.get('Type')
    print(type)
    orderBy = request.GET.get('order_by', 'Date')
    questions = billingQuestion.objects.filter(Answered = True).order_by(orderBy)
    if type != "":
         
         fil_questions = questions.filter(Type = type).order_by(orderBy)

         return render(request, 'showQuestions.html', {'questions':fil_questions, 'type':type})
    else:
        return redirect('showQuestions')

def filterDocType(request):
    cat = request.POST.get('Category')
    print(cat)
    
    docs = billingPDF.objects.filter()
    if cat != "":
         
         fil_docs = docs.filter(Category = cat)

         return render(request, 'showPDFs.html', {'docs':fil_docs, 'category':cat})
    else:
        return redirect('showPDFs')

def showUnanswered(request):
    orderBy = request.GET.get('order_by', 'Date')
    questions = billingQuestion.objects.filter(Answered =False).order_by(orderBy)
    
    return render(request, 'showUnanswered.html', {'questions':questions})

def deleteQuestion(request, question_id):
    question = billingQuestion.objects.get(pk = question_id)
    question.delete()
    requests = billingQuestion.objects.all()
    return redirect('showQuestions')

def deletePDF(request, doc_id):
    doc = billingPDF.objects.get(pk = doc_id)
    doc.delete()
    #requests = billingPDF.objects.all()
    return redirect('showPDFs')

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

def editPDF(request, doc_id):
    if request.method == "POST":
        doc = billingPDF.objects.get(pk = doc_id)
        form = editPDFForm(request.POST or None, instance=doc)
        print(form.errors)
        if form.is_valid():
            
            messages.success(request, ('Item has been Edited'))
           
            temReq = form.save()

            requests = list(billingPDF.objects.all())
            
            return redirect('showPDFs')
        else:
           
            print("Farts")
            messages.error(request, "Error")
            requests = billingPDF.objects.all()
            return redirect('showPDFs')
           
    else:
        
        doc = billingPDF.objects.get(pk = doc_id)
        
        return render(request, 'editPDF.html', {'doc':doc})

def answerQuestion(request, question_id):
    question = billingQuestion.objects.get(pk = question_id)
    if request.method == "POST":
        
        form = answerForm(request.POST or None, instance=question)
        print(form.errors)
        if form.is_valid():
            
            messages.success(request, ('Question has been Answered'))
           
            answer = form.save(commit = False)
            answer.Answered = True
            answer.save()

            
            
            return redirect('showUnanswered')
        else:
           
            print("Farts")
            messages.error(request, "Error")
            requests = billingQuestion.objects.all()
            return redirect('showQuestions')
    else:

        return render(request, 'answerQuestion.html', {'question':question})
           
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

