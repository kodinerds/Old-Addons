#!/usr/bin/python
# -*- coding: utf-8 -*-

import feedparser
import re
import HTMLParser
import xbmcgui

#####import urllib
#####import sys
#####import os
#####import datetime
#####import xbmc
#####import xbmcgui
#####import xbmcaddon
#####import xbmcplugin
#####from xml.dom.minidom import parseString
#####
class NewsFeed():
    def __init__(self):
        url=''


##########################################################################################################################
##
##########################################################################################################################
    def feed2container2(self):
        WINDOW = xbmcgui.Window( 10000 )
        listitems = []
    
        for i in range(x,50):
            if WINDOW.getProperty('LatestNews.%s.Title' % i) == '':
                break
            title = WINDOW.getProperty('LatestNews.%s.Title' % i)
            description = WINDOW.getProperty('LatestNews.%s.Desc' % i)
            img = WINDOW.getProperty('LatestNews.%s.Logo' % i)
            pubdate = WINDOW.getProperty('LatestNews.%s.Date' % i)
            headerpic = WINDOW.getProperty('LatestNews.%s.HeaderPic' % i)
    
            json_str = { "Logo": img, "Label": title, "Desc": description, "HeaderPic": headerpic, "Date": pubdate}
            listitems.append( json_str )
    
        return listitems
    

##########################################################################################################################
##
##########################################################################################################################
    def feed2property(self,url,headerpic):
        if headerpic == '':
            headerpic='http://www.kokobeet.at/wp-content/uploads/logo_platzhalter.gif'
        feed = feedparser.parse( url )
        WINDOW = xbmcgui.Window( 10000 )
        x=0
    
        for item in feed[ "items" ]:
            title = item[ "title" ]
    
            try:
                img = item[ "media_content" ][0][ "url" ]
            except:
                try:
                    ce = item[ "content" ][0][ "value" ]
                    imgsrc = re.search('img[^<>\\n]+src=[\'"]([^"\']+(?<!(gif|img)))[\'"]', ce)
                    img = imgsrc.group(1)
                except:
                    imgsrc = re.search('img[^<>\\n]+src=[\'"]([^"\']+(?<!(gif|img)))[\'"]', item[ "summary" ])
                    try:
                        img = imgsrc.group(1)
                    except:
                        if len(item[ 'links' ]) >= 1:
                            piclink = ''
                            for link in item[ 'links' ]:
                                if re.search('.*(png|jpg|jpeg)', link['href']):
                                    piclink = link['href']
                                    break
                        if piclink != '':
                            img = str(piclink)
                        else:
                            img = 'http://dzmlsvv5f118.cloudfront.net/wp-content/uploads/2013/04/newsandblogimage.jpg?cc475f'
    
    
            description = item[ "summary" ]
            description = re.sub('<p[^>\\n]*>','\n\n',description)
            description = re.sub('<br[^>\\n]*>','\n',description)
            description = re.sub('<[^>\\n]+>','',description)
            description = re.sub('\\n\\n+','\n\n',description)
            description = re.sub('(\\w+,?) *\\n(\\w+)','\\1 \\2',description)
            description = HTMLParser.HTMLParser().unescape(description).strip()
    
            pubdate = item[ "published" ]
    
            WINDOW.setProperty( "LatestNews.%s.Title" % (x), title )
            WINDOW.setProperty( "LatestNews.%s.Desc" % (x), description )
            WINDOW.setProperty( "LatestNews.%s.Logo" % (x), img )
            WINDOW.setProperty( "LatestNews.%s.Date" % (x), pubdate )
            WINDOW.setProperty( "LatestNews.%s.HeaderPic" % (x), headerpic )
            x+=1
    
        for i in range(x,50):
            WINDOW.clearProperty('LatestNews.%s.Title' % i)
            WINDOW.clearProperty('LatestNews.%s.Desc' % i)
            WINDOW.clearProperty('LatestNews.%s.Logo' % i)
            WINDOW.clearProperty('LatestNews.%s.Date' % i)
            WINDOW.clearProperty('LatestNews.%s.HeaderPic' % i)
    
    
    
