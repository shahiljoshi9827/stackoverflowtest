from django.urls import path

from QA.views import QuestionView, QuestionDetailView

urlpatterns = [
    path('question/', QuestionView.as_view(), name='question'),
    path('question/<int:id>', QuestionDetailView.as_view(), name='question-detail'),
]
