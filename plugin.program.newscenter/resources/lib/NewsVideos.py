#!/usr/bin/python

import urllib,urllib2
import json
import xbmc
import feedparser
import re

class NewsVideos():

    def __init__(self):
        # do variable init
        url=''

    


##########################################################################################################################
##
##########################################################################################################################
    def get_ts100_url(self):
        url = "http://www.tagesschau.de/api/multimedia/video/ondemand100~_type-video.json"
    
        response = urllib.urlopen(url)
        data = json.loads(response.read())
        return data['multimedia'][1]['tsInHundredSeconds']['mediadata'][3]['h264xl']
    

##########################################################################################################################
##
##########################################################################################################################
    def get_ts2000_url(self):
        url = "http://www.tagesschau.de/api/multimedia/sendung/letztesendungen100~_type-TS2000.json"
    
        response = urllib.urlopen(url)
        data = json.loads(response.read())
        ts200jsonurl = str(data['latestBroadcastsPerType'][0]['details'])
        response2 = urllib.urlopen(ts200jsonurl)
        data2 = json.loads(response2.read())
        data3 = data2['fullvideo'][0]['mediadata'][5]['h264xl']
        return data3
    

##########################################################################################################################
##
##########################################################################################################################
    def get_mdr_aktuell_130_url(self):
        url="http://www.ardmediathek.de/tv/MDR-aktuell-Eins30/Sendung?documentId=7545100&bcastId=7545100&rss=true"
        feed = feedparser.parse( url )
        weblink=feed[ "items" ][0]['guid']
        videoid=re.findall('documentId=(........)',weblink)
        videoid = videoid[0]
        url="http://www.ardmediathek.de/play/media/%s" % (videoid)
        req = urllib2.urlopen(url)
        content = unicode(req.read(), "utf-8")
        mediathekjson = json.loads(content)
        medias = mediathekjson['_mediaArray'][0]['_mediaStreamArray']
        for media in medias:
            if media['_quality'] == 3:
                stream = media['_stream']
        return stream
    

##########################################################################################################################
##
##########################################################################################################################
    def get_tagesschauwetter_url(self):
        url='http://www.tagesschau.de/api/multimedia/video/ondemand100~_type-video.json'
        response = urllib.urlopen(url)
        data = json.loads(response.read())
    
        for vid in data['videos']:
            if vid['headline'] == "Die Wetteraussichten":
                for md in vid['mediadata']:
                    try:
                        stream=md['h264xl']
                    except:
                        pass
        return stream
    
    

##########################################################################################################################
##
##########################################################################################################################
    def get_wetteronline_url(self):
        headers = { 'User-Agent' : 'Mozilla/5.0' }
        req = urllib2.Request('http://www.wetteronline.de/wetter-videos', None, headers)
        html = urllib2.urlopen(req).read()
        wetterfile = re.findall('20\d\d\d\d\d\d_...mp4',html)
        url = "rtmp://62.113.210.2/wetteronline-vod/"+wetterfile[0]
        return url
    

##########################################################################################################################
##
##########################################################################################################################
    def get_wetterinfo_url(self):
        url = "http://dlc3.t-online.de/mflash/wetterstudio_prem.mp4"
        return url
    

##########################################################################################################################
##
##########################################################################################################################
    def get_wetternet_url(self):
        url="https://www.youtube.com/feeds/videos.xml?playlist_id=PL79960E6A59C3F69C"
        headers = { 'User-Agent' : 'Mozilla/5.0' }
        req = urllib2.Request(url, None, headers)
        html = urllib2.urlopen(req).read()
        videoid = re.findall('www.youtube.com/watch\?v=(.+?)"',html)
        return 'plugin://plugin.video.youtube/play/?video_id=%s' % (videoid[0])


##########################################################################################################################
##
##########################################################################################################################
    def get_kinder_nachrichten_url(self):
        url="https://www.zdf.de/ZDFmediathek/podcast/222528?view=podcast"
        feed = feedparser.parse( url )
        return feed[ "items" ][0]['guid']
    

##########################################################################################################################
##
##########################################################################################################################
    def get_rundschau100_url(self):
        url="http://redirect.br-online.de/br/bayerisches-fernsehen/rundschau/rsku/rundschaukultur_XL.mp4"
        return url
    

##########################################################################################################################
##
##########################################################################################################################
    def get_ndraktuellkompakt_url(self):
        url="http://www.ndr.de/fernsehen/sendungen/ndr_aktuell/NDR-Aktuell-kompakt-,ndraktuellkompakt110.html"
        url="http://www.ndr.de/fernsehen/sendungen/ndr_aktuell/index.html"
        headers = { 'User-Agent' : 'Mozilla/5.0' }
        req = urllib2.Request(url, None, headers)
        html = urllib2.urlopen(req).read()
        media = re.findall('content="(.+?.hq.mp4)"',html)
        if len(media) == 0:
            media = 'plugin://plugin.video.youtube/?action=play_video&videoid=5WFvhp-2qZI'
        else:
            media = media[0]
        return media
    





##########################################################################################################################
##
##########################################################################################################################
    def PlayTagesschau100(self):
        url=self.get_ts100_url()
        xbmc.executebuiltin('XBMC.PlayMedia('+url+')')

    def PlayTagesschau(self):
        url=self.get_ts2000_url()
        xbmc.executebuiltin('XBMC.PlayMedia('+url+')')

    def PlayMDRAktuell130(self):
        url=self.get_mdr_aktuell_130_url()
        xbmc.executebuiltin('XBMC.PlayMedia('+url+')')

    def PlayTagesschauWetter(self):
        url=self.get_tagesschauwetter_url()
        xbmc.executebuiltin('XBMC.PlayMedia('+url+')')

    def PlayWetterOnline(self):
        url=self.get_wetteronline_url()
        xbmc.executebuiltin('XBMC.PlayMedia('+url+')')

    def PlayWetterInfo(self):
        url=self.get_wetterinfo_url()
        xbmc.executebuiltin('XBMC.PlayMedia('+url+')')

    def PlayWetterNet(self):
        url=self.get_wetternet_url()
        xbmc.executebuiltin('XBMC.PlayMedia('+url+')')

    def PlayKinderNachrichten(self):
        url=self.get_kinder_nachrichten_url()
        xbmc.executebuiltin('XBMC.PlayMedia('+url+')')

    def PlayRundschau100(self):
        url=self.get_rundschau100_url()
        xbmc.executebuiltin('XBMC.PlayMedia('+url+')')

    def PlayNDRAktuellKompakt(self):
        url=self.get_ndraktuellkompakt_url()
        xbmc.executebuiltin('XBMC.PlayMedia('+url+')')

       
