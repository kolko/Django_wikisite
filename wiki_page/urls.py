#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *
from wiki_page.views import *

urlpatterns = patterns('',
    url(r'^$', page, {'page_addr': 'main'}),

    url(r'^add/?$', page_add),
    
    url(r'^(?P<page_addr>[a-z0-9_/]+)/add/?$', page_add),

    url(r'^(?P<page_addr>[a-z0-9_/]+)/edit/?$', page_edit),
    
    url(r'^(?P<page_addr>[a-z0-9_/]+)/delete/?$', page_delete),
    
    url(r'^(?P<page_addr>[a-z0-9_/]+)/history/?$', page_history),
    
    url(r'^(?P<page_addr>[a-z0-9_/]+)/?$', page),
    
    
)
