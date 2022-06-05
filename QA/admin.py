from django.contrib import admin
from QA.models import Question, Answer, QuestionTag, Tags, QuestionUserUpVote, QuestionUserDownVote, AnswerUserUpVote, \
    AnswerUserDownVote

admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(QuestionTag)
admin.site.register(Tags)
admin.site.register(QuestionUserUpVote)
admin.site.register(QuestionUserDownVote)
admin.site.register(AnswerUserUpVote)
admin.site.register(AnswerUserDownVote)
