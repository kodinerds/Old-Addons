#!/usr/bin/python

import urllib2
import xbmcgui
import json


##############################################################################################################################
##
##
##
##############################################################################################################################
class DocuCCWidged():
    def __init__(self):
        url=''
    
    ##########################################################################################################################
    ##
    ##########################################################################################################################
    def getUnicodePage(url):
        req = urllib2.urlopen(url)
        content = ""
        if "content-type" in req.headers and "charset=" in req.headers['content-type']:
            encoding=req.headers['content-type'].split('charset=')[-1]
            content = unicode(req.read(), encoding)
        else:
            content = unicode(req.read(), "utf-8")
        return content
    
    ##########################################################################################################################
    ##
    ##########################################################################################################################
    def set_LatestDokus_to_Home(url):
        WINDOW = xbmcgui.Window( 10000 )
        content = str(self.getUnicodePage(url))
        NewDokus = json.loads(content)
        NewDokus = NewDokus['dokus']
        x=0
        for Doku in NewDokus:
            WINDOW.setProperty( "LatestDocu.%s.Title" % (x), Doku['title'] )
            WINDOW.setProperty( "LatestDocu.%s.Thumb" % (x), Doku['cover'] )
            WINDOW.setProperty( "LatestDocu.%s.Path" % (x),  'plugin://plugin.video.youtube/?action=play_video&videoid=%s' % (Doku['youtubeId']) )
            WINDOW.setProperty( "LatestDocu.%s.Tags" % (x),  Doku['dokuSrc'] )
            x+=1
    
    ##########################################################################################################################
    ##
    ##########################################################################################################################
    def clear_LatestDokus_at_Home():
        WINDOW = xbmcgui.Window( 10000 )
        for i in range(1,25):
            WINDOW.clearProperty('LatestDocu.%s.Title' % i)
            WINDOW.clearProperty('LatestDocu.%s.Thumb' % i)
            WINDOW.clearProperty('LatestDocu.%s.Path' % i)
            WINDOW.clearProperty('LatestDocu.%s.Tags' % i)
    
    
