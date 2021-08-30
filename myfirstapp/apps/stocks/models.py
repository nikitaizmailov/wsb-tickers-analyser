from django.db import models

# python's builtin standard datetime handling lib
import datetime

# django's builtin datetime awareness handling lib
from django.utils import timezone

# Create your models here.

class Question(models.Model):
    question_text = models.CharField('Question Text', max_length=500)
    pub_date = models.DateTimeField('Date Published')

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        condition = self.pub_date >= timezone.now() - datetime.timedelta(days=1)
        return condition

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text