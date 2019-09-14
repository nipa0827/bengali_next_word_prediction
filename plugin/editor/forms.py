# -*- coding: utf-8 -*-

from django import forms


class TextForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea)
