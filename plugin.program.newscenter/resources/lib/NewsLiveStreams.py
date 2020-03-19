#!/usr/bin/python

import urllib
import requests
from xml.dom.minidom import parseString
import json
import xbmc
import requests

class NewsLiveStreams():

    def __init__(self):
        # do variable init
        url=''

##########################################################################################################################
##
##########################################################################################################################
    def get_livestream_euronews_url(self):
        r = requests.post("http://de.euronews.com/nachrichten/livestream/", data={'action': 'getHexaglobeUrl'})
        r = requests.get(r.text)
        euronews_streams = json.loads(r.text)
        return euronews_streams['primary']['de']['hls']
    

##########################################################################################################################
##
##########################################################################################################################
    def get_livestream_ntv_url(self):
        url = "http://p.live.fra.n-tv.de/hls-live/ntvlive/ntvlive_1500.m3u8"
        return url
    

##########################################################################################################################
##
##########################################################################################################################
    def get_livestream_n24_url(self):
        url = "http://n24-live.hls.adaptive.level3.net/n24/live2cms/live2cms.m3u8"
        return url
    
##########################################################################################################################
##
##########################################################################################################################
    def get_livestream_tagesschau24_url(self):
        url = "http://www.tagesschau.de/api/multimedia/video/ondemand100~_type-video.json"
        response = urllib.urlopen(url)
        data = json.loads(response.read())
        return data['multimedia'][0]['livestreams'][0]['mediadata'][0]['http_tab_high']
    
##########################################################################################################################
##
##########################################################################################################################
    def get_livestream_phoenix_url(self):
        url = "https://www.phoenix.de/php/mediaplayer/data/beitrags_details.php?ak=web&id=livestream247_1"
        response = urllib.urlopen(url)
        content = response.read()
    
        xmldoc = parseString(content)
        itemlist = xmldoc.getElementsByTagName('formitaet')
        for s in itemlist:
            if s.attributes['basetype'].value == "h264_aac_ts_http_m3u8_http":
                if s.getElementsByTagName('quality')[0].firstChild.nodeValue == "high":
                    url = s.getElementsByTagName('url')[0].firstChild.nodeValue
        return url
    
##########################################################################################################################
##
##########################################################################################################################
    def get_livestream_dw_url(self):
        url = "http://dwstream6-lh.akamaihd.net/i/dwstream6_live@123962/master.m3u8"
        return url
    
##########################################################################################################################
##
##########################################################################################################################
   
    def PlayEuronews(self):
        url=self.get_livestream_euronews_url()
        xbmc.executebuiltin('XBMC.PlayMedia('+url+')')
    
##########################################################################################################################
##
##########################################################################################################################
    def PlayNTV(self):
        url=self.get_livestream_ntv_url()
        xbmc.executebuiltin('XBMC.PlayMedia('+url+')')
    
##########################################################################################################################
##
##########################################################################################################################
    def PlayN24(self):
        url=self.get_livestream_n24_url()
        xbmc.executebuiltin('XBMC.PlayMedia('+url+')')
    
##########################################################################################################################
##
##########################################################################################################################
    def PlayTagesschau24(self):
        url=self.get_livestream_tagesschau24_url()
        xbmc.executebuiltin('XBMC.PlayMedia('+url+')')
    
##########################################################################################################################
##
##########################################################################################################################
    def PlayPhoenix(self):
        url=self.get_livestream_phoenix_url()
        xbmc.executebuiltin('XBMC.PlayMedia('+url+')')
    
##########################################################################################################################
##
##########################################################################################################################
    def PlayDW(self):
        url=self.get_livestream_dw_url()
        xbmc.executebuiltin('XBMC.PlayMedia('+url+')')
