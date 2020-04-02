# -*- coding: utf-8 -*-

from common import *

class Live_Videos:

    def __init__(self, i):
        self.item = {}
        self.live = i['live']
        self.start = i['scheduled'][:22]
        self.item['mode'] = 'play'
        self.item['title'] = self.title(i)
        self.item['id'] = i['page']
        self.item['params'] = 'true'

        if i.get('image', None):
            self.item['thumb'] = i['image'].replace('%d','800x450')

        if i.get('description', None):
            self.item['plot'] = i['description']
            
        if i.get('duration', None):
            self.item['duration'] = i['duration']
            
    def title(self, i):
        title = i['title']
        if self.live:
            return utfenc(unicode('[COLOR red]LIVE[/COLOR]  %s' % (title)))
        else:
            return utfenc(unicode('%s %s' % (self.start,title)))