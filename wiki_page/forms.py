#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms
from django.forms import ModelForm

from wiki_page.models import *

class PageForm(ModelForm):

    class Meta:
        model = Page
        exclude = ('dt', 'parent', 'name', 'page_clean', 'address')
        
    def clean(self, *args, **kwargs):
        cleaned_data = super(PageForm, self).clean(*args, **kwargs)
        if not cleaned_data['caption']:
            raise forms.ValidationError(u"Пустое поле \"Заголовок\".")
        if not cleaned_data['text']:
            raise forms.ValidationError(u"Пустое содержимое.")
        return cleaned_data

class AddPageForm(ModelForm):

    class Meta:
        model = Page
        exclude = ('dt', 'parent', 'page_clean', 'address')
        
    def clean(self, *args, **kwargs):
        cleaned_data = super(AddPageForm, self).clean(*args, **kwargs)
        if not cleaned_data['caption']:
            raise forms.ValidationError(u"Пустое поле \"Заголовок\".")
        if not cleaned_data['text']:
            raise forms.ValidationError(u"Пустое содержимое.")
        if not cleaned_data['name']:
            raise forms.ValidationError(u"Пустое имя.")
        return cleaned_data
