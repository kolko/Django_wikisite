#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils import simplejson
from decimal import Decimal as D

from django.template import RequestContext
from django.shortcuts import render_to_response
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.db import connection

from django.utils import simplejson
import datetime

from wiki_page.models import *
from wiki_page.forms import *
from wiki_page.utils import get_page_by_address, get_page_name_from_address, make_parent_list, check_parent_exist, get_client_ip


def page(request, page_addr):
    '''Отображение wiki-страницы'''
    parent_error = check_parent_exist(page_addr)
    page = get_page_by_address(page_addr)
    page_parents = make_parent_list(page_addr)
    childs = None
    if page:
        childs = page.page_set.filter(caption__isnull=False, text__isnull=False)
    return render(request, 'page.html', {"page": page, "page_addr": page_addr, "childs": childs, "parent_error": parent_error, "page_parents": page_parents})
    
def page_edit(request, page_addr):
    '''Редактирование wiki-страницы'''
    parent_error = check_parent_exist(page_addr)
    page = get_page_by_address(page_addr)
    page_parents = make_parent_list(page_addr)
    childs = None
    if page:
        childs = page.page_set.filter(caption__isnull=False, text__isnull=False)
    form = PageForm(request.POST or None, instance=page)
    if not parent_error:
        if form.is_valid():
            db = form.save(commit=False)
            db.name = get_page_name_from_address(page_addr)
            if page_parents:
                db.parent = page_parents[-1]
            db.save(get_client_ip(request))
            return HttpResponseRedirect(reverse('wiki_page.views.page', args=[page_addr,]))
    return render(request, 'page_edit.html', {"page": page, "page_addr": page_addr, "childs": childs, "parent_error": parent_error, "page_parents": page_parents, "form": form})

def page_delete(request, page_addr):
    '''Удаление страницы'''
    page = get_page_by_address(page_addr)
    page.delete_page()
    return HttpResponseRedirect(reverse('wiki_page.views.page', args=['main']))

def page_add(request, page_addr=None):
    '''Добавление wiki-страницы'''
    parent = None
    if page_addr:
        parent_error = check_parent_exist(page_addr+'/blah')
        parent = get_page_by_address(page_addr)
        page_parents = make_parent_list(page_addr+'/blah')
    form = AddPageForm(request.POST or None)
    if form.is_valid():
        db = form.save(commit=False)
        if parent:
            db.parent = parent
        db.save(get_client_ip(request), force_insert=True)
        return HttpResponseRedirect(reverse('wiki_page.views.page', args=[db.address,]))
    return render(request, 'page_edit.html', {"page": page, "form": form,  "parent_error": parent_error, "page_parents": page_parents})

def page_history(request, page_addr):
    '''История правок'''
    parent_error = check_parent_exist(page_addr)
    page = get_page_by_address(page_addr)
    page_parents = make_parent_list(page_addr)
    childs = None
    page_history = None
    if page:
        childs = page.page_set.filter(caption__isnull=False, text__isnull=False)
        page_history = page.pagehistory_set.all().order_by('-dt')
    return render(request, 'page_history.html', {"page": page, "page_addr": page_addr, "childs": childs, "parent_error": parent_error, "page_parents": page_parents, "page_history": page_history, })
