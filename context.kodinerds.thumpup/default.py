#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import xbmc
import xbmcaddon
import xbmcgui,xbmcvfs,xbmcplugin
import json,urllib2,re,urlparse,os
from difflib import SequenceMatcher
from bs4 import BeautifulSoup
from datetime import datetime    
import urllib
import requests,cookielib
import YDStreamExtractor

from cookielib import LWPCookieJar
cj = cookielib.CookieJar()
addon = xbmcaddon.Addon()

profile    = xbmc.translatePath( addon.getAddonInfo('profile') ).decode("utf-8")
temp       = xbmc.translatePath( os.path.join( profile, 'temp', '') ).decode("utf-8")
session = requests.session()
addon_handle = int(sys.argv[1])

thread="https://www.kodinerds.net/index.php/Thread/11148-Was-ist-eure-Lieblingsserie-Serientalk-Empfehlungen/"
if not xbmcvfs.exists(temp):       
       xbmcvfs.mkdirs(temp)
       

def debug(content):
    log(content, xbmc.LOGDEBUG)
    
def notice(content):
    log(content, xbmc.LOGNOTICE)

def log(msg, level=xbmc.LOGNOTICE):
    addon = xbmcaddon.Addon()
    addonID = addon.getAddonInfo('id')
    xbmc.log('%s: %s' % (addonID, msg), level) 

def parameters_string_to_dict(parameters):
	paramDict = {}
	if parameters:
		paramPairs = parameters[1:].split("&")
		for paramsPair in paramPairs:
			paramSplits = paramsPair.split('=')
			if (len(paramSplits)) == 2:
				paramDict[paramSplits[0]] = paramSplits[1]
	return paramDict
    
def addLink(name, url, mode, iconimage, duration="", desc="", genre=''):
  u = sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)
  ok = True
  liz = xbmcgui.ListItem(name, iconImage="", thumbnailImage=iconimage)  
  liz.setInfo(type="Video", infoLabels={"Title": name, "Plot": desc, "Genre": genre})
  liz.setProperty('IsPlayable', 'true')
  liz.addStreamInfo('video', { 'duration' : duration })
  liz.setProperty("fanart_image", iconimage)
  #liz.setProperty("fanart_image", defaultBackground)

  xbmcplugin.setContent(int(sys.argv[1]), 'tvshows')
  ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz)
  return ok
  
def geturl(url,data="x",header=[]):
   global cj
   content=""
   debug("URL :::::: "+url)
   opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
   userAgent = "Coralie/1.7.2-2016081207(SM-G900F; Android; 6.0.1"
   header.append(('User-Agent', userAgent))
   header.append(('Accept', "*/*"))
   header.append(('Content-Type', "application/json;charset=UTF-8"))
   header.append(('Accept-Encoding', "plain"))   
   opener.addheaders = header
   try:
      if data!="x" :
         request=urllib2.Request(url)
         cj.add_cookie_header(request)
         content=opener.open(request,data=data).read()
      else:
         content=opener.open(url).read()
   except urllib2.HTTPError as e:
       debug ( e)
   opener.close()
   return content



    
addon = xbmcaddon.Addon()    
debug("Hole Parameter")
debug("Argv")
debug(sys.argv)
debug("----")

params = parameters_string_to_dict(sys.argv[2])
mode = urllib.unquote_plus(params.get('mode', ''))
url = urllib.unquote_plus(params.get('url', ''))
debug("Mode ist : "+mode)
def menu():
      
    content=geturl(thread)
    htmlPage = BeautifulSoup(content, 'html.parser')    
    liste = htmlPage.find("div",{"class" :"contentNavigation"})     
    debug(liste)
    Seiten=liste.findAll("a")
    seitennr=0
    title_array=[]
    video_array=[]
    desc_array=[]
    user_array=[]
    datum_array=[]
    bild_array=[]
    for Seite in Seiten:
        try:
            number=int(Seite.text)
            if number > seitennr:
                seitennr=number
        except:
                pass
    dialoga = xbmcgui.DialogProgress()
    dialoga.create("Suche Videos","")
    for i in range (67,seitennr+1,1):    
        dialoga.update(seitennr/100*i,"Suche in Seite "+str(i))
        content2=geturl(thread+"?pageNo="+str(i))
        htmlPage2 = BeautifulSoup(content2, 'html.parser')     
        liste = htmlPage2.findAll("article")     
        for post in liste:        
            Textraw = post.find("div",{"class" :"messageText"})
            Text = Textraw.encode("utf-8",).strip()
            if "Durch Kodi empfohlen" in Text:
                try:
                    video=Textraw.find("a",{"class" :"externalURL"})["href"]  
                    if video in video_array:
                      continue                    
                    video_array.append(video)                
                except:
                    continue
                #debug(post)
                #noah1 schrieb:                
                user=post.find("span").text                
                user_array.append(user)                
                datum=post.find("time").text
                datum_array.append(datum)                
                serie=re.compile("Durch Kodi empfohlen:</a> '(.+?)'", re.DOTALL).findall(Text)[0]  
                title_array.append(serie)
                bild=Textraw.find("img")["src"]
                bild_array.append(bild)
                inhalt=re.compile("Inhalt:<br/>([^<]+)", re.DOTALL).findall(Text)[0].strip()             
                desc_array.append(inhalt)
    
    for i in range(len(user_array)-1,0,-1):       
       debug(title_array[i])
       addLink(title_array[i]+" ( von : "+user_array[i]+ " am "+datum_array[i]+" )",video_array[i],"playvideo",bild_array[i],desc=desc_array[i])
    xbmcplugin.endOfDirectory(addon_handle,succeeded=True,updateListing=False,cacheToDisc=True)                    
    
def playvideo(url):    
   debug(url)
   vid = YDStreamExtractor.getVideoInfo(url,quality=2) #quality is 0=SD, 1=720p, 2=1080p and is a maximum
   debug(vid)
   stream_url = vid.streamURL()
   stream_url=stream_url.split("|")[0]
   listitem = xbmcgui.ListItem(path=stream_url)   
   addon_handle = int(sys.argv[1])  
   xbmcplugin.setResolvedUrl(addon_handle, True, listitem)                    
username=addon.getSetting("username")
password=addon.getSetting("password")

if username=="" or password=="":
   dialog = xbmcgui.Dialog()
   ok = dialog.ok('Username oder Password fehlt', 'Username oder Password fehlt')
   exit    
if mode=="":
    menu()  
if mode=="playvideo":
    playvideo(url)
    

    
