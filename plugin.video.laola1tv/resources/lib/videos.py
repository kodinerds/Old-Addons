# -*- coding: utf-8 -*-

from common import *

class Videos:

    def __init__(self, i):
        self.item = {}
        self.item['mode'] = 'play'
        self.item['title'] = utfenc(i['title'])
        self.item['id'] = i['page']
        self.item['params'] = 'false'

        if i.get('image', None):
            self.item['thumb'] = i['image'].replace('%d','800x450')

        if i.get('description', None):
            self.item['plot'] = i['description']
            
        if i.get('duration', None):
            self.item['duration'] = i['duration']