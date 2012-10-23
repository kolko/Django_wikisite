#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models
import datetime

class Page(models.Model):
    '''Страница'''
    parent = models.ForeignKey(
        'self',
        db_column = 'parent',
        blank = True, null=True,
        verbose_name = u'Страница-родитель',
    )
    address = models.CharField(#т.к адреса мы не меняем - храним его статически
        db_column = 'address',
        max_length = 2048,
        verbose_name = u'Адрес страницы',
        unique = True,
    )
    name = models.CharField(
        db_column = 'name',
        max_length = 128,
        verbose_name = u'Имя страницы',
    )
    caption = models.CharField(
        db_column = 'caption',
        max_length = 512,
        blank = True, null=True,
        verbose_name = u'Заголовок',
    )
    text = models.TextField(
        db_column = 'text',
        blank = True, null=True,
        verbose_name = u'Содержимое',
    )
    dt = models.DateTimeField(
        db_column = 'dt',
        verbose_name = u'Время последней правки',
    )
    
    @property
    def is_deleted(self):
        '''Проверка на удалённость (чтобы можно было изменить при желании)'''
        if (not self.text) and (not self.caption):
            return True
        return False
        
    def delete_page(self):
        '''Кастомная функция удаления страницы'''
        self.caption = None
        self.text = None
        #удаление детей
        for x in self.page_set.all():
            x.delete_page()
        self.save()
        
    
    class Meta:
        db_table = 'wiki_page'
        verbose_name = u'Страница'
#        unique_together = ("address",)

    def __unicode__(self):
        return u'%s' % (self.name)

    def make_history(self, ip_address):
        '''Кладем изменения в лог'''
        log = PageHistory()
        log.page = self
        log.dt = self.dt
        log.caption = self.caption
        log.text = self.text
        log.ip = ip_address
        log.save()

    def save(self, ip_address, *args, **kwargs):
        #в dt - дата последнего изменения
        if self.name:
            self.name = self.name.lower()
        if not self.address:
            if self.parent:
                self.address = self.parent.address+'/%s'%self.name
            else:
                self.address = self.name
        self.dt = datetime.datetime.now()
        super(Page, self).save(*args, **kwargs)
        self.make_history(ip_address)

class PageHistory(models.Model):
    '''История правок'''
    page = models.ForeignKey(
        'Page',
        db_column = 'page',
        verbose_name = u'Страница',
    )
    dt = models.DateTimeField(
        db_column = 'dt',
        verbose_name = u'Время правки',
    )
    caption = models.CharField(
        db_column = 'caption',
        max_length = 512,
        blank = True, null=True,
        verbose_name = u'Заголовок',
    )
    text = models.TextField(
        db_column = 'text',
        blank = True, null=True,
        verbose_name = u'Содержимое',
    )
    ip = models.CharField(
        db_column = 'ip',
        max_length = 512,
        blank = True, null=True,
        verbose_name = u'ip клиента',
    )
    class Meta:
        db_table = 'wiki_page_log'
        
    @property
    def is_delet(self):
        '''True - если произошло удаление'''
        if (not self.text) and (not self.caption):
            return True
        return False
