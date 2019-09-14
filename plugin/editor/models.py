from django.db import models
from django.forms import ModelForm, Textarea
from django import forms
from django.forms import ModelForm


# Create your models here.
class Text(models.Model):
    content = models.TextField()

    def __str__(self):
        return self.content


