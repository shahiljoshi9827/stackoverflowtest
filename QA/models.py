from django.db import models


# Create your models here.
class Tags(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Question(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField()
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    pub_date = models.DateTimeField('date published',auto_now_add=True)

    def __str__(self):
        return self.title


class QuestionTag(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tags, on_delete=models.CASCADE)

    def __str__(self):
        return self.tag.name


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.TextField()
    accepted = models.BooleanField(default=False)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    pub_date = models.DateTimeField('date published',auto_now_add=True)

    def __str__(self):
        return self.answer


class QuestionAnswerUserVote(models.Model):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
