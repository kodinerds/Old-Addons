# -*- coding: utf-8 -*-

from common import *

class Items:

    def __init__(self):
        self.cache = True
        self.video = False
    
    def list(self):
        if self.video:
            xbmcplugin.setContent(addon_handle, content)
        xbmcplugin.endOfDirectory(addon_handle, cacheToDisc=self.cache)
        
        if force_view:
            xbmc.executebuiltin('Container.SetViewMode(%s)' % view_id)

    def add(self, item):
        data = {
            'mode': item['mode'],
            'title': item['title'],
            'id': item.get('id', ''),
            'params': item.get('params', '')
        }
                    
        art = {
            'thumb': item.get('thumb', icon),
            'poster': item.get('thumb', icon),
            'fanart': fanart
        }

        labels = {
            'title': item['title'],
            'plot': item.get('plot', ''),
            'premiered': item.get('date', ''),
            'episode': item.get('episode', 0)
        }
        
        listitem = xbmcgui.ListItem(item['title'])
        listitem.setArt(art)
        listitem.setInfo(type='Video', infoLabels=labels)
        
        if 'play' in item['mode']:
            self.cache = False
            self.video = True
            folder = False
            listitem.addStreamInfo('video', {'duration':item.get('duration', 0)})
            listitem.setProperty('IsPlayable', 'true')
        else:
            folder = True
            
        xbmcplugin.addDirectoryItem(addon_handle, build_url(data), listitem, folder)
        
    def play(self, path):
        listitem = xbmcgui.ListItem()
        listitem.setContentLookup(False)
        listitem.setMimeType('application/x-mpegURL')
        listitem.setProperty('inputstreamaddon', 'inputstream.adaptive')
        listitem.setProperty('inputstream.adaptive.manifest_type', 'hls')
        listitem.setPath(path)
        xbmcplugin.setResolvedUrl(addon_handle, True, listitem)