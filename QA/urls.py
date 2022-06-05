from django.urls import path

from QA.views import QuestionView, QuestionDetailView, AnswerView, AnswerDetailView, AcceptAnswerView, QuestionTagView, \
    QuestionUserView

urlpatterns = [
    path('question/', QuestionView.as_view(), name='question'),
    path('question/<int:id>', QuestionDetailView.as_view(), name='question-detail'),
    path('answer/', AnswerView.as_view(), name='answer'),
    path('answer/<int:id>', AnswerDetailView.as_view(), name='answer-detail'),
    path('accept-answer/<int:pk>/<int:question_id>', AcceptAnswerView.as_view(), name='accept-answer'),
    path('question-tag/<str:tag>/', QuestionTagView.as_view(), name='question-tag'),
    path('question-user/', QuestionUserView.as_view(), name='question-user'),
]
