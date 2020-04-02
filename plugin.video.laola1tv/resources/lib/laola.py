# -*- coding: utf-8 -*-

from common import *
from items import Items
from menu import Menu
from videos import Videos
from live_videos import Live_Videos
from live import Live
        
items = Items()

def menu(data):
    items.add({'mode':'live', 'title':getString(30101)})
    sports = data[0]['children']
    for i in sports:
        items.add(Menu(i, 'sports').item)
    items.list()
    
def sports(data, channel):
    channels = data[0]['children']
    for c in channels:
        if channel == utfenc(c['title']):
            for i in c['children']:
                items.add(Menu(i, 'sub_menu').item)
            break
    items.list()
    
def sub_menu(data):
    container = data['container']
    for c in container:
        if c['content']:
            if c.get('page', None):
                items.add(Menu(c, 'videos').item)
            else:
                for i in c['content']:
                    items.add(Videos(i).item)
        elif c['schedule']:
            for s in c['schedule']:
                items.add(Live_Videos(s).item)
    items.list()
    
def live(data):
    videos = data.get('video', [])
    for i in videos:
        items.add(Live(i).item)
    items.list()

def video(data):
    content = data['container'][0]['content']
    for i in content:
        items.add(Videos(i).item)
    items.list()
    
def play(path):
    if path:
        items.play(path)