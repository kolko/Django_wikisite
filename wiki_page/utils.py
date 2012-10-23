#!/usr/bin/env python
# -*- coding: utf-8 -*-

from wiki_page.models import *
from wiki_page.forms import *

def get_page_by_address(address):
    '''Селектим страницу'''
    addr = '/'.join(filter(lambda x: bool(x), address.split('/')))
    try:
        return Page.objects.get(address=addr)
    except Page.DoesNotExist:
        return None

def get_page_name_from_address(address):
    '''Извлекаем имя страницы из адреса'''
    return filter(lambda x: bool(x), address.split('/'))[-1]
    
def check_parent_exist(address):
    '''Проверяет наличие родителя
    Возвращает None если страница первого уровня, либо родитель существует
    Иначе возвращает адрес несуществующего родителя самого маленького уровня
    '''
    addr = filter(lambda x: bool(x), address.split('/'))
    if len(addr) < 2:
        return None
    check = addr[:-1]
    error = None
    while check:
        page = get_page_by_address('/'.join(check))
        if (not page) or (page.is_deleted):
            error = '/'.join(check)
            check = check[:-1]
        else:
            return error
            
def make_parent_list(address):
    '''Возвращает список родительских страниц'''
    addr = filter(lambda x: bool(x), address.split('/'))
    if len(addr) < 2:
        return []
    address = ''
    parents = []
    for x in addr[:-1]:
        address += x+'/'
        page = get_page_by_address(address)
        if page:
            parents.append(page)
        else:
            break
    return parents
    
def get_client_ip(request):#взято со stack overflow
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
