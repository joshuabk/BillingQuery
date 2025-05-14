from django.urls import path
from . import views
urlpatterns = [
    path('', views.submitQuestion, name='submitQuestion'),
    path('submitPDF/', views.submitPDF, name='submitPDF'),
    path('login/',  views.loginUser, name = 'login' ),
    path('logout/',  views.logoutUser, name = 'logout' ),
    path('showQuestions/', views.showQuestions, name='showQuestions'),
    path('showUnanswered/', views.showUnanswered, name='showUnanswered'),
    path('showPDFs/', views.showPDFs, name='showPDFs'),
    path('editQuestion/<question_id>', views.editQuestion, name='editQuestion'),
    path('showQuestion/<question_id>', views.showQuestion, name='showQuestion'),
    path('deleteQuestion/<question_id>', views.deleteQuestion, name='deleteQuestion'),
    path('deletePDF/<doc_id>', views.deletePDF, name='deletePDF'),
    path('answerQuestion/<question_id>', views.answerQuestion, name='answerQuestion'),
    path('searchQuestionsAnswered/<str:type>', views.searchQuestionsAnswered, name='searchQuestionsAnswered'),
    path('searchPDFs/<str:category>', views.searchPDFs, name='searchPDFs'),
    path('searchQuestionsUnanswered', views.searchQuestionsUnanswered, name='searchQuestionsUnanswered'),
    path('filterType', views.filterType, name='filterType'),
    path('filterDocType', views.filterDocType, name='filterDocType'),
]