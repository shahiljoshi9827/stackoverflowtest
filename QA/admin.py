from django.contrib import admin
from QA.models import Question, Answer, QuestionTag, QuestionAnswerUserVote, Tags

admin.site.register(Question)
admin.site.register(QuestionAnswerUserVote)
admin.site.register(Answer)
admin.site.register(QuestionTag)
admin.site.register(Tags)
