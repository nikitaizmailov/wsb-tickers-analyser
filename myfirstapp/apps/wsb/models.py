from django.db import models
from django.forms import ModelForm
from django import forms

# python's builtin standard datetime handling lib
import datetime

# django's builtin datetime awareness handling lib
from django.utils import timezone

import random
import string
# Create your models here.


class Subreddit(models.Model):
    subreddit_name = models.CharField('Subreddit Name', max_length=255)

    # This is a Mock Choice to test the database model
    submission_title = models.CharField('Submission Title', max_length=500)
    
    regex_pattern = models.CharField('Regex Pattern', max_length=100)
    number_of_mentions = models.IntegerField(default=0)
    post_date = models.DateTimeField('Date Published', default=timezone.now)

    def __str__(self):
        return self.subreddit_name + " --> " + self.submission_title

class Comment(models.Model):
    subreddit = models.ForeignKey(Subreddit, on_delete=models.CASCADE, related_name='comment_set', default=None)
    author_name = models.CharField('author name', max_length=50)
    comment_text = models.CharField('commentary text', max_length=200)

    def __str__(self):
        return self.author_name


STATES = (
    ('', 'Choose...'),
    ('MG', 'Minas Gerais'),
    ('SP', 'Sao Paulo'),
    ('RJ', 'Rio de Janeiro')
)
# Adding ModelForms to create a Crispy Form on the HTML page.
class SubredditForm(ModelForm):
    state = forms.ChoiceField(choices=STATES, widget=forms.RadioSelect,)

    class Meta:
        model = Subreddit
        fields = ['subreddit_name', 'submission_title', 'regex_pattern']

# class CommentForm(ModelForm):
#     class Meta:
#         model = Comment
#         fields = ['author_name']