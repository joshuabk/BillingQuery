from django.urls import path
from . import views
urlpatterns = [
    path('', views.submitQuestion, name='submitQuestion'),
    path('login/',  views.loginUser, name = 'login' ),
    path('logout/',  views.logoutUser, name = 'logout' ),
    path('showQuestions/', views.showQuestions, name='showQuestions'),
    path('showUnanswered/', views.showUnanswered, name='showUnanswered'),
    path('editQuestion/<question_id>', views.editQuestion, name='editQuestion'),
    path('showQuestion/<question_id>', views.showQuestion, name='showQuestion'),
    path('deleteQuestion/<question_id>', views.deleteQuestion, name='deleteQuestion'),
    path('answerQuestion/<question_id>', views.answerQuestion, name='answerQuestion'),
    path('searchQuestionsAnswered/<str:type>', views.searchQuestionsAnswered, name='searchQuestionsAnswered'),
    path('searchQuestionsUnanswered', views.searchQuestionsUnanswered, name='searchQuestionsUnanswered'),
    path('filterType', views.filterType, name='filterType'),
]