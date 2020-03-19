#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import xbmc
import xbmcaddon
import xbmcgui,xbmcvfs
import json,urllib2,re,urlparse,os
from difflib import SequenceMatcher
from bs4 import BeautifulSoup
from datetime import datetime    
import urllib
import requests,cookielib
from cookielib import LWPCookieJar
cj = cookielib.CookieJar()
addon = xbmcaddon.Addon()

profile    = xbmc.translatePath( addon.getAddonInfo('profile') ).decode("utf-8")
temp       = xbmc.translatePath( os.path.join( profile, 'temp', '') ).decode("utf-8")
session = requests.session()

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



def gettitle()  :
  title=""
  title=xbmc.getInfoLabel('ListItem.TVShowTitle')
  try:    
    info = sys.listitem.getVideoInfoTag() 
    title=info.getTVShowTitle()
  except:
    pass
  try:
      title=xbmc.getInfoLabel('ListItem.TVShowTitle')
  except:
       pass
  if title=="":
     title = xbmc.getInfoLabel("ListItem.Title").decode('UTF-8')      
  if title=="":
     title=sys.listitem.getLabel()
  debug("TITLE :::: "+title)     
  return title

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def find_in_thread(title):
  debug("-------- findinthread")
  content=geturl(thread)
  htmlPage = BeautifulSoup(content, 'html.parser')    
  liste = htmlPage.find("div",{"class" :"contentNavigation"})     
  debug(liste)
  Seiten=liste.findAll("a")
  seitennr=0
  for Seite in Seiten:
#     debug("-->"+Seite.text)
     try:
        number=int(Seite.text)
        if number > seitennr:
            seitennr=number
     except:
      pass
  dialoga = xbmcgui.DialogProgress()
  dialoga.create("Suche Post für "+title.encode("utf-8").strip(),"")
  for i in range (60,seitennr+1,1):
    dialoga.update(seitennr/100*i,"Suche in Seite "+str(i))
    content2=geturl(thread+"?pageNo="+str(i))
    htmlPage2 = BeautifulSoup(content2, 'html.parser') 
    sec_token=re.compile("SECURITY_TOKEN = '(.+?)'", re.DOTALL).findall(content2)[0]
    liste = htmlPage2.findAll("article")   
    for post in liste:
        try:    
            Text = post.find("div",{"class" :"messageText"}).text.encode("utf-8").strip()     
        except:
            debug("ERR")
            continue            
        textid = post["data-object-id"]  
        try:
            empfehler = post["data-like-user"]       
        except:
             empfehler=""
        debug(Text)
        debug("------")
        if title.encode("utf-8") in Text:
            dialoga.close()
            dialog = xbmcgui.Dialog()
            username=addon.getSetting("username")
            if username in empfehler:
               ok = dialog.ok('Schon Empfohlen', 'Du hast es schon Geliked')
               return 1               
            ret=dialog.yesno("Wurde schon empfohlen Liken?", Text+"\n Liken?")
            if ret==1:
                values = {
                    'actionName': 'like',
                    'className': 'wcf\data\like\LikeAction',
                    'parameters[data][containerID]' : 'wcf24',
                    'parameters[data][objectID]' : textid,
                    'parameters[data][objectType]' : 'com.woltlab.wbb.likeablePost',
      
                }                
                data = urllib.urlencode(values)
                content=geturl("https://www.kodinerds.net/index.php/AJAXProxy/?t="+sec_token,data=data)
                print(content)
                return 1
            else:
                 dialoga = xbmcgui.DialogProgress()
                 dialoga.create("Suche Post für "+title.encode("utf-8").strip(),"")
                 dialoga.update(i*100/seitennr,"Suche in Seite "+str(i))
  dialoga.close()
  return 0
    
addon = xbmcaddon.Addon()    
debug("Hole Parameter")
debug("Argv")
debug(sys.argv)
debug("----")
try:
      params = parameters_string_to_dict(sys.argv[2])
      debug("Parameter Holen geklappt")
except:
      debug("Parameter Holen nicht geklappt")
      mode="" 
debug("Mode ist : "+mode)
if mode=="":  
    username=addon.getSetting("username")
    password=addon.getSetting("password")
    if username=="" or password=="":
      dialog = xbmcgui.Dialog()
      ok = dialog.ok('Username oder Password fehlt', 'Username oder Password fehlt')
      exit    
    title=gettitle()
    url="https://api.themoviedb.org/3/search/tv?api_key=f5bfabe7771bad8072173f7d54f52c35&language=de-DE&query=" + title.replace(" ","+")
    content=geturl(url)
    wert = json.loads(content)  
    wert=wert["results"]    
    debug(wert)
    count=0
    gefunden=0
    wertnr=0
    for serie in wert:
      serienname=serie["name"].encode("utf-8")
      debug(serienname)
      nummer=similar(title,serienname)
      if nummer >wertnr:
        wertnr=nummer
        gefunden=count
      count+=1
    if count>0:      
      idd=str(wert[gefunden]["id"])
      seriesName=wert[gefunden]["name"].encode("utf-8")
      serienstart=wert[gefunden]["first_air_date"].encode("utf-8")
      inhalt=wert[gefunden]["overview"].encode("utf-8")
      if inhalt=="":
        urlx="https://api.themoviedb.org/3/search/tv?api_key=f5bfabe7771bad8072173f7d54f52c35&language=en-US&query=" + title.replace(" ","+")
        content=geturl(urlx)
        wert = json.loads(content)  
        wert=wert["results"] 
        inhalt=wert[gefunden]["overview"]
      Bild="http://image.tmdb.org/t/p/w300/"+wert[gefunden]["poster_path"].encode("utf-8")
      newurl="https://api.themoviedb.org/3/tv/"+idd+"?api_key=f5bfabe7771bad8072173f7d54f52c35&language=de-DE"
      content2=geturl(newurl)
      wert2 = json.loads(content2)
      anzahLstaffeln=wert2["number_of_seasons"]      
      dialog=xbmcgui.Dialog()
      ret=dialog.yesno("Serienname richtig?", "Ist der Serienname "+seriesName +" richtig?")
      if ret==0:
         count=0         
         seriesName=title
    else:
      seriesName=title 
    debug("Gefunden :"+seriesName)
    dialog=xbmcgui.Dialog()      
    ret=dialog.yesno("Serie empfehlen?", "Serienname "+seriesName +" empfehlen?")           
    if ret==0:
       quit()
       exit
    if title=="":
       dialog = xbmcgui.Dialog()
       ok = dialog.ok('Fehler', 'Selektiertes File Hat kein Serie hinterlegt')
       quit()
       exit
    content=geturl("https://www.kodinerds.net/")    
    newurl=re.compile('method="post" action="(.+?)"', re.DOTALL).findall(content)[0]
    sec_token=re.compile("SECURITY_TOKEN = '(.+?)'", re.DOTALL).findall(content)[0]
    content=geturl("https://www.kodinerds.net/index.php/Login/",data="username="+username+"&action=login&password="+password+"&useCookies=1&submitButton=Anmelden&url="+newurl+"&t="+sec_token)
    if "Angaben sind ung" in content or "Anmelden oder registrieren"in content:
      dialog = xbmcgui.Dialog()
      ok = dialog.ok('Username oder Password ungültig', 'Username oder Password ungueltig')
      quit()  
      exit      
    ret=find_in_thread(seriesName)      
    if ret==1:
       quit()
       exit
    content=geturl(thread)

    sec_token=re.compile("SECURITY_TOKEN = '(.+?)'", re.DOTALL).findall(content)[0]
    hash=re.compile('name="tmpHash" value="(.+?)"', re.DOTALL).findall(content)[0]
    timestamp=re.compile('data-timestamp="(.+?)"', re.DOTALL).findall(content)[0]
    text="[url='https://www.kodinerds.net/index.php/Thread/58030-Doofe-ideen/\']Durch Kodi empfohlen:[/url] '"+seriesName+"'"   
    if count>0:    
      text=text+"\n"+"[img]"+Bild+"[/img]\n"
      text=text+"Gestartet am: "+serienstart+"\n"
      text=text+"Anzahl Staffeln: " +str(anzahLstaffeln)+"\n"
      text=text+"Inhalt:\n"
      text=text+inhalt+"\n"      
      try:
        debug("Try German Trailer")
        movidedb="https://api.themoviedb.org/3/tv/"+str(idd)+"/videos?api_key=f5bfabe7771bad8072173f7d54f52c35&language=de-DE"
        content=geturl(movidedb)
        trailers = json.loads(content)        
        if len(trailers["results"])==0:
            debug("Try English Trailer")
            movidedb="https://api.themoviedb.org/3/tv/"+str(idd)+"/videos?api_key=f5bfabe7771bad8072173f7d54f52c35&language=en-US"
            content=geturl(movidedb)
            trailers = json.loads(content)        
        debug(trailers)
        zeige=""
        nr=0
        for trailer in trailers["results"]:
          wertung=0
          key=trailer["key"]
          debug("KEY :"+key)
          site=trailer["site"]
          type=trailer["type"]
          if site=="YouTube":
            if "railer" in type:
                wertung=2
            else:
                wertung=1
          if wertung>nr:
            zeige=key
            nr=wertung
        if not zeige=="":
           debug("----")
           debug(text)
           debug("FOUND :"+zeige)
           text=text+'[url=\'https://www.youtube.com/watch?v='+zeige.encode('ascii')+'\']Trailer[/url]\n'
           debug("-----")
           debug(text)
      except  Exception as e: 
           print str(e)
      text=text+'[url=\'https://www.werstreamt.es/filme-serien?q='+seriesName.replace(" ","+")+'&action_results=suchen\']Wo läuft es[/url]'        
    values = {
      'actionName' : 'quickReply',
      'className' : 'wbb\data\post\PostAction',
      'interfaceName': 'wcf\data\IMessageQuickReplyAction',
      'parameters[objectID]': '11148',
      'parameters[data][message]' : text,
      'parameters[data][tmpHash]' : hash,
      'parameters[lastPostTime]':timestamp,
      'parameters[pageNo]':'1'
    }
    data = urllib.urlencode(values)
    content=geturl("https://www.kodinerds.net/index.php/AJAXProxy/?t="+sec_token,data=data)
    if content == ""  : 
      dialog = xbmcgui.Dialog()
      ok = dialog.ok('Posten hat nicht Geklappt', 'Posten hat nicht Geklappt. Posten nur alle 30 Sek möglich')
      exit    
    debug(content)
    
    

    
