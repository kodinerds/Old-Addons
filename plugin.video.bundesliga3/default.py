#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import xbmcgui
import xbmcplugin
import xbmcaddon
import xbmc
import urlparse
import urllib, urllib2, socket, cookielib, re, os, shutil,json
import time
import locale
from datetime import datetime


base_url = sys.argv[0]
addon_handle = int(sys.argv[1])
args = urlparse.parse_qs(sys.argv[2][1:])
addon = xbmcaddon.Addon()
# Lade Sprach Variablen
translation = addon.getLocalizedString

Monate = {
           "Januar":1,
           "Februar":2,
           "März":3,
           "April":4,
           "Mai":5,
           "Juni":6,
           "Juli":7,
           "August":8,
           "September":9,
           "Oktober":10,
           "November":11,
           "Dezember":12
}


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
  
def addLink(name, url, mode,meldung="",spiel=""):
	u = sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&meldung="+ str(meldung)+"&spiel="+ spiel
	liz = xbmcgui.ListItem(name)
	liz.setProperty('IsPlayable', 'true')
	xbmcplugin.setContent(int(sys.argv[1]), 'tvshows')
	ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz)
	return ok
  
  
def geturl(url):
   cj = cookielib.CookieJar()
   opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
   userAgent = "Mozilla/5.0 (Windows NT 6.2; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0"
   opener.addheaders = [('User-Agent', userAgent)]
   req = opener.open(url)
   inhalt = req.read()   
   return inhalt
   
  
def get_spiele():
  URL="http://www.liga3-online.de/live-spiele/"
  content=geturl(URL)
  kurz_inhalt = content[content.find('wp-table-reloaded wp-table-reloaded-id-8')+1:]  
  kurz_inhalt = kurz_inhalt[:kurz_inhalt.find('</tbody>')]
  spl=kurz_inhalt.split('<tr class="row')
  for i in range(2,len(spl)-1,1):
    element=spl[i]
    try:
      debug ("Element :" + element)
      ar_datum=re.compile('<td class="column-2[^>]*>([^<]+)</td>', re.DOTALL).findall(element)    
      ar_zeit=re.compile('<td class="column-3[^>]*>([^<]+)</td>', re.DOTALL).findall(element)    
      ar_spiel=re.compile('<td class="column-4[^>]*>([^<]+)</td>', re.DOTALL).findall(element)
      ar_sender=re.compile('<td class="column-5[^>]*>([^<]+)</td>', re.DOTALL).findall(element)
      if ar_datum:
        datum=ar_datum[0]
        datum_old=datum
      else:
        datum=datum_old
      if ar_zeit :
        zeit=ar_zeit[0]
        zeit_old=zeit
      else:
        zeit=zeit_old
      spiel=ar_spiel[0]
      sender=ar_sender[0]
      lt = time.localtime()
      jahr=time.strftime("%Y", lt)
      debug("datum"+datum)
      datum_reg=re.compile('.+, ([0-9]+)\. (.+)', re.DOTALL).findall(datum)
      month=datum_reg[0][1]
      day=datum_reg[0][0]
      monat=Monate[month]
      jahr_now= time.strftime("%Y", lt)
      tag_now= time.strftime("%d", lt)
      monat_now= time.strftime("%m", lt)
      debug("------"+ str(jahr_now) +"=="+ str(jahr) +": "+ str(day) +"=="+ str(tag_now) +":"+ str(monat_now) +"=="+ str(monat))
      if int(monat_now) > int(monat):
        jahr=str(int(jahr)+1)
      zeitstring=day+"."+str(monat) +"."+jahr + " " + zeit.strip()
      debug("zeitstring :"+zeitstring +"XXX")
      zeitobjekt=time.strptime(zeitstring , "%d.%m.%Y %H:%M Uhr")   
      if time.mktime(zeitobjekt) <= time.mktime(lt):
        neuzeit=time.strftime("[COLOR red]Läuft seit "+ zeit +"[/COLOR]",zeitobjekt)         
      elif str(jahr_now)==str(jahr) and str(day)==str(tag_now) and str(monat_now)==str(monat):
        neuzeit="[COLOR yellow]Heute [/COLOR]"+ zeit
      else:
        neuzeit=time.strftime("%d. %B %H:%M",zeitobjekt)   

      if time.mktime(zeitobjekt) > time.mktime(lt) :
        meldung="Läuft noch nicht"       
      else:
        meldung=""     
      txtneu=neuzeit +" : "+ spiel
      if "*" in sender and not "/" in sender : 
         txtneu= txtneu + " (Konferenz)"
      addLink(name=txtneu, url=sender , mode="Watch",meldung=meldung,spiel=spiel)
    except:
       pass    
  xbmcplugin.endOfDirectory(addon_handle,succeeded=True,updateListing=False,cacheToDisc=True)
def getUrl(url):
        
        debug("TV4User: Get Url")
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:23.0) Gecko/20100101 Firefox/23.0')
        response = urllib2.urlopen(req)
        content=response.read()
        response.close()
        return content
def maschaftfinden(manschaft,spiel):
        found=0
        sp1 = manschaft.split(' ') 
        for i in range(1, len(sp1), 1):                  
          entry=sp1[i]
          if len(entry)>3:
            if entry in spiel:
              debug("maschaftfinden Entry :"+entry)
              debug("spiel :")
              debug (spiel)
              found=1
        return found 

def folge(url):
    inhalt = geturl(url)
    inhalt=inhalt.replace("'",'"')         
    kurz_inhalt = inhalt[inhalt.find('<div class="clearFix">')+1:]
    kurz_inhalt = kurz_inhalt[:kurz_inhalt.find('<span class="playBtn ir">Video starten</span>')]   
    match=re.compile('dataURL:"([^"]+)"', re.DOTALL).findall(kurz_inhalt)
    xmlfile="http://www.br.de/"+match[0]
    xbmc.log("BR xmlfile: "+ xmlfile )
    inhalt = geturl(xmlfile) 
    inhalt=ersetze(inhalt)    
    inhalt = inhalt[:inhalt.find('<asset type="HDS')]  
    spl=inhalt.split('<asset ')
    debug("split")
    if "Live HLS" in inhalt:
       debug("LIVE")
       was=spl[3]
       debug ("Live: "+ was)         
    debug("XXX was"+ was)          
    match=re.compile('<downloadUrl\>([^<]+)</downloadUrl>', re.DOTALL).findall(was)
    if match :
      video=match[0]
    else :
       match=re.compile('<url>([^<]+)</url', re.DOTALL).findall(was)
       video=match[0]
    debug("XXX video url:"+ video)    
    return video

def live():
      url="http://www.br.de/mediathek/video/livestreams-100.html"
      inhalt = geturl(url)
      match=re.compile('data-filter_entire_broadcasts_url="([^"]+)"', re.DOTALL).findall(inhalt)
      json_url=match[0]
      debug("Jsonurl="+json_url)
      urlnew=jsonurl("http://www.br.de/"+json_url) 
      urlnew=folge(urlnew)
      return urlnew
      
def ersetze(inhalt):
   inhalt=inhalt.replace('&#39;','\'')  
   inhalt=inhalt.replace('&quot;','"')    
   inhalt=inhalt.replace('&gt;','>')      
   inhalt=inhalt.replace('&amp;','&') 
   return inhalt
   
def jsonurl(url) :   
    newurl=""
    debug("Json Url "+ url)
    inhalt = geturl(url)
    inhalt=ersetze(inhalt)
    spl=inhalt.split('<article ')
    for i in range(1,len(spl),1):
      entry=spl[i].replace('\\"','"') 
      entry=entry.replace('\\/','/') 
      
      match=re.compile('<a href="([^"]+)"', re.DOTALL).findall(entry)      
      url="http://www.br.de/"+match[0]     
      
      match=re.compile('<span class="episode">([^<]+)</span>', re.DOTALL).findall(entry)      
      title=match[0]       
      
      debug("URL : " + url)       
      debug("Spiel: " + spiel)
      debug("Title: " + title)
      debug("----------------")
      match = re.compile('([^-]+) - ([^-]+)', re.DOTALL).findall(spiel)
      name1=match[0][0]
      name2=match[0][1]            
      if maschaftfinden(name1, title) ==1 or maschaftfinden(name2, title)==1  :   
         newurl=url     
    return newurl   

    
def watchlive(url,meldung="",spiel=""):
   debug("watchlive")
   debug(url)
   debug(meldung)
   debug(spiel)
   debug("----------")
   urlnew=""
   euro=0
   if "/" in url:
      sender=url.replace("*"," (Konferenz)")
      spl = sender.split('/')
      dialog = xbmcgui.Dialog()
      nr=dialog.select("Stream:", spl)     
      url=spl[nr].replace(" (Konferenz)","").strip()
      debug("URL IST: #"+ url +"###")
   if not meldung == "" :
        dialog = xbmcgui.Dialog()
        nr=dialog.yesno("Läuft nicht", "Dieses Spielt läuft noch nicht trotzdem versuchen?")        
        if not nr:
          listitem = xbmcgui.ListItem(path=url) 
          xbmcplugin.setResolvedUrl(addon_handle,False, listitem) 
          get_spiele()
          return
   if "mdr.de" in url:       
       match = re.compile('([^-]+) - ([^-]+)', re.DOTALL).findall(spiel)
       name1=match[0][0]
       name2=match[0][1]
       urlstart="http://www.mdr.de/mediathek/livestreams/mdr-plus/index.html"
       content=getUrl(urlstart)                        
       match = re.compile('href="([^"]+?)" class="moreBtn" title=(.+?) - (.+?)\"', re.DOTALL).findall(content)
       for urln,spieler1,spieler2 in match:
           debug("- Spieler1 :"+spieler1)
           debug("- Spieler2 :"+spieler2)
           debug("- name1 :"+name1)
           debug("- name1 :"+name2)
           if maschaftfinden(spieler1, name1) ==1 or maschaftfinden(spieler2, name1)==1:   
                debug("Gefunden")
                url= urln
                break
           debug("--------------------------")
       debug("urln :"+ urln)
       debug("--------------------------")
       content=getUrl("http://www.mdr.de/"+urln)
       match = re.compile("'playerXml':'(.+?)'", re.DOTALL).findall(content)       
       xmlurl= match[0].replace("\/","/")
       content=getUrl("http://www.mdr.de"+xmlurl)
       match = re.compile("<adaptiveHttpStreamingRedirectorUrl>(.+?)</adaptiveHttpStreamingRedirectorUrl>", re.DOTALL).findall(content)  
       urlnew=match[0]
       debug("XMLURL :"+ xmlurl)
   elif "ndr.de" in url:
      debug("spiel" +spiel)    
      match = re.compile('([^-]+) - ([^-]+)', re.DOTALL).findall(spiel)
      name1=match[0][0]
      name2=match[0][1]
      debug("name2"+ name2)
      debug("name1"+ name1)
      url="https://www.ndr.de/sport/live/livecenter104.html"
      content=getUrl(url)   
      kurz_inhalt = content[content.find('<div class="container w100">')+1:]
      kurz_inhalt = kurz_inhalt[:kurz_inhalt.find('<iframe')]      
      spl = kurz_inhalt.split('<div class="videolinks">')    
      urlnew=""      
      for i in range(1, len(spl), 1):
        entry=spl[i]   
        debug("ENTRY + "+ entry)
        match = re.compile('span class="icon icon_video"></span>([^<]+)<', re.DOTALL).findall(entry)        
        debug("+++ match[0] :" + match[0])        
        if maschaftfinden(name1, match[0]) ==1 or maschaftfinden(name2, match[0])==1  :   
           match = re.compile('data-streamurl="([^"]+)"', re.DOTALL).findall(entry)        
           urlreg=match[0]           
           #/sport/fussball/eventlivestream2272-player_image-fc9e58f1-26f4-441e-ac26-2c356f85bff4_theme-ndr.html
           urlreg=urlreg.replace('player_image','ppjson_image') 
           urlreg=urlreg.replace('_theme-ndr.html','.json')             
           urljson="https://www.ndr.de"+urlreg           
           debug("urljson:" +urljson)
           content=getUrl(urljson)   
           #debug("content : " + content)
           match = re.compile('"([^"]+)\.m3u8', re.DOTALL).findall(content)   
           urlnew=match[0]+".m3u8"
           debug("urlnew :------- "+ urlnew)
           break           
   elif "NDR" in url:
      urlnew="http://ndr_fs-lh.akamaihd.net/i/ndrfs_nds@119224/master.m3u8"                    
   elif "MDR" in url:
      urlnew="http://livetvsachsen.mdr.de/i/livetvmdrsachsen_de@106902/master.m3u8"                  
   elif "RBB" in url:
      urlnew="http://rbb_live-lh.akamaihd.net/i/rbb_berlin@108248/master.m3u8?bkup=off"      
   elif "SWR" in url:
      urlnew="http://swrbw-lh.akamaihd.net/i/swrbw_live@196738/master.m3u8"
   elif "WDR" in url:
      urlnew="http://wdr_fs_geo-lh.akamaihd.net/i/wdrfs_geogeblockt@112044/master.m3u8"             
   if url=="rbb-online.de":
      urlnew="http://rbb_event-lh.akamaihd.net/i/rbbevent_nongeo@107643/index_1728_av-p.m3u8?sd=10&rebase=on"
   if url=="Eurosport":
      dialog = xbmcgui.Dialog()
      nr=dialog.ok("Eurosport", "Eurosport hat kein Internet Stream")
      euro=1
   if url=="hessenschau.de":
      urlN="http://hessenschau.de/sport/index.html"
      match = re.compile('([^-]+) - ([^-]+)', re.DOTALL).findall(spiel)
      name1=match[0][0]
      name2=match[0][1]
      content=getUrl(urlN) 
      kurz_inhalt = content[content.find('<span class="teaser__topline text__topline">3. Liga </span>')+1:]
      kurz_inhalt = kurz_inhalt[:kurz_inhalt.find('</article>')]
      match = re.compile('span class="teaser__headline text__headline">([^<]+)</span>', re.DOTALL).findall(kurz_inhalt)
      title= match[0]
      match = re.compile('<a href="([^"]+)"', re.DOTALL).findall(kurz_inhalt)
      urlM=match[0]
      if maschaftfinden(name1, title) ==1 or maschaftfinden(name2, title)==1  :
            urlpage=urlM
            content=getUrl(urlM) 
            match = re.compile('"streamUrl": "([^"]+)"', re.DOTALL).findall(content)
            urlnew=match[0]   
            debug("URL hessen: " + urlnew)            
   if url=="swr.de":
      url="http://swrmediathek.de/assets/pages/fussball.html"
      content=getUrl(url)      
      match = re.compile('http://swrmediathek.de/player.htm\?show=(.+?)"', re.DOTALL).findall(content)   
      urlpart=match[0]        
      urla="http://swrmediathek.de/AjaxEntry?callback=js&ekey="+urlpart+"&rand=Sat"    
      debug("URLA : "+urla)          
      content=getUrl(urla) 
      debug ("content:"+ content)
      if "m3u8" in content:
            match = re.compile('"([^"]+)\.m3u8"', re.DOTALL).findall(content)   
            urlnew=match[0]+".m3u8"                               
      else:
            urlnew=""  
   if url=="sportschau.de":
       debug("spiel" +spiel)          
       match = re.compile('([^-]+) - ([^-]+)', re.DOTALL).findall(spiel)
       name1=match[0][0]
       name2=match[0][1]
       url="http://www.sportschau.de/fussball/bundesliga3/dritteligalivestreams100.html"
       content=getUrl(url)   
       kurz_inhalt = content[content.find('<h1 class="siteHeadline hidden"')+1:]
       kurz_inhalt = kurz_inhalt[kurz_inhalt.find('<div class="teaser">')+1:]             
       kurz_inhalt = kurz_inhalt[kurz_inhalt.find('<div class="teaser">')+1:]
       kurz_inhalt = kurz_inhalt[:kurz_inhalt.find('<div class="section sectionA" >')]
       debug("------------+----")
       debug (kurz_inhalt)
       match = re.compile('href="(.+?)" title="3. Liga: (.+?)">', re.DOTALL).findall(kurz_inhalt)
       url=match[0][0]
       spiel=match[0][1]   
       debug("URL: "+ url)
       debug("totle: "+ name)
       if maschaftfinden(name1, spiel) ==1 or maschaftfinden(name2, spiel)==1  : 
           debug("Gefunden")          
           urljson="http://www.sportschau.de/"+url                     
           content=getUrl(urljson)   
           #debug("content : " + content)
           match = re.compile("'mediaObj': { 'url': '(.+?)'", re.DOTALL).findall(content)   
           url3=match[0]
           content=getUrl(url3) 
           match = re.compile('"([^"]+)\.m3u8', re.DOTALL).findall(content)   
           urlnew=match[0]+".m3u8"
           debug ("urlnew :"+ urlnew)
   if "br.de" in url :
       urlnew=live()           
   if urlnew :         
      listitem = xbmcgui.ListItem(path=urlnew) 
      xbmcplugin.setResolvedUrl(addon_handle,True, listitem)
   else :
      if euro==0:
          dialog = xbmcgui.Dialog()
          nr=dialog.ok("Sender nicht bekannt", "Zu Diesem sender fehlt der stream")          
      listitem = xbmcgui.ListItem(path=url) 
      xbmcplugin.setResolvedUrl(addon_handle,False, listitem) 

    
params = parameters_string_to_dict(sys.argv[2])
mode = urllib.unquote_plus(params.get('mode', ''))
url = urllib.unquote_plus(params.get('url', ''))
name = urllib.unquote_plus(params.get('name', ''))
meldung = urllib.unquote_plus(params.get('meldung', ''))
spiel = urllib.unquote_plus(params.get('spiel', ''))
  
  
if mode is '':
    get_spiele()
if mode == 'Watch':
    watchlive(url=url,meldung=meldung,spiel=spiel)
  
  

