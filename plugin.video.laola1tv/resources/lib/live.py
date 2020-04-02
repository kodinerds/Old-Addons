# -*- coding: utf-8 -*-

from common import *

class Live:

    def __init__(self, i):
        self.item = {}
        self.a = i['@attributes']
        self.live = self.a['islive']
        self.start = self.a['scheduled_start'][:16]
        self.end = self.a['scheduled_end'][:16]
        self.sport = i['sport']
        self.liga = i['liga']
        self.update_item(i)
        
    def title(self, i):
        title = i['titleEN']
        if self.live == 'true':
            return utfenc(unicode('[COLOR red]LIVE[/COLOR]  %s' % (title)))
        else:
            return utfenc(unicode('%s %s' % (self.start,title)))
        
    def description(self):
        return utfenc(unicode('Start: %s\nEnd: %s\nSport: %s\nLiga: %s' % (self.start, self.end, self.sport, self.liga)))
    
    def duration(self):
        now = datetime.datetime.now()
        start = datetime.datetime.fromtimestamp(time.mktime(time.strptime(self.a['scheduled_start'],'%Y-%m-%d %H:%M:%S')))
        end = datetime.datetime.fromtimestamp(time.mktime(time.strptime(self.a['scheduled_end'],'%Y-%m-%d %H:%M:%S')))
        if self.live == 'true':
            return timedelta_total_seconds(end-now)
        else:
            return timedelta_total_seconds(end-start)
        
    def update_item(self, i):
        self.item['mode'] = 'play'
        self.item['params'] = 'true'
        self.item['title'] = self.title(i)
        self.item['id'] = self.a['id']
        self.item['plot'] = self.description()
        self.item['thumb'] = i['image']
        self.item['date'] = self.start[:10]
        self.item['duration'] = self.duration()