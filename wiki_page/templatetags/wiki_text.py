#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

from django.template import Library
from django.utils.html import escape

from wiki_page.utils import check_parent_exist, get_page_by_address

register = Library()

@register.filter
def wiki_text(text):
    def repl(m):
        if (not check_parent_exist(m.group(1))) and (get_page_by_address(m.group(1))): 
            return "<a href=\"/wiki/%s\">%s</a>" % (m.group(1), m.group(2))
        else:
            return "<a href=\"/wiki/%s/edit\" style=\"color: red;\">%s</a>" % (m.group(1), m.group(2))
    
    text = escape(text)
    text = re.sub(r"\*\*(.+?)\*\*", lambda m: "<b>%s</b>" % m.group(1), text)
    text = re.sub(r"//(.+?)//", lambda m: "<i>%s</i>" % m.group(1), text)
    text = re.sub(r"__(.+?)__", lambda m: "<u>%s</u>" % m.group(1), text)
    
    text = re.sub(r"(?<!\[)\[(?!\[)([^ ]+?) (.+?)\]\]", repl, text)
    text = re.sub(r"\[\[(.+?)(?<!\])\](?!\])", lambda m: "<a href=\"%s\">%s</a>" % (m.group(1), m.group(1)), text)
    text = re.sub(r"\[\[([^ ]+?) (.+?)\]\]", lambda m: "<a href=\"%s\">%s</a>" % (m.group(1), m.group(2)), text)
    
    return text

        
    
