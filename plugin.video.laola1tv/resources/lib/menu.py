# -*- coding: utf-8 -*-

from common import *

class Menu:

    def __init__(self, i, mode):
        self.item = {}
        self.item['mode'] = mode
        self.item['title'] = utfenc(i['title'])
        self.item['id'] = i['page']
        self.item['params'] = i['pagetype']

        if i.get('logo', None):
            self.item['thumb'] = i['logo']
        elif i.get('icon', None):
            self.item['thumb'] = i['icon'].replace('80x80','120x120')

        if i.get('description', None):
            self.item['plot'] = i['description']

    