from django.urls import path
from . import views
urlpatterns = [
    path('', views.submitQuestion, name='submitQuestion'),
    path('showQuestions/', views.showQuestions, name='showQuestions'),
    path('editQuestion/<question_id>', views.editQuestion, name='editQuestion'),
    path('showQuestion/<question_id>', views.showQuestion, name='showQuestion'),
    path('deleteQuestion/<question_id>', views.deleteQuestion, name='deleteQuestion'),
    path('searchQuestions', views.searchQuestions, name='searchQuestions'),
]