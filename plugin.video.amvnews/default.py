#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import requests,urllib,re,os
import xbmcplugin,xbmcgui
import xbmcaddon,xbmc,xbmcvfs
from random import randint

addon = xbmcaddon.Addon(id='plugin.video.amvnews')
home = addon.getAddonInfo('path').decode('utf-8')
image = xbmc.translatePath(os.path.join(home, 'icon.png'))
datapath = xbmc.translatePath('special://profile/addon_data/plugin.video.amvnews/')
if not os.path.isdir(datapath):
  os.mkdir(datapath)

myvideos = os.path.join(datapath,'myvideos.txt')
amvfolder = addon.getSetting('amvfolder').decode('utf-8')

pluginhandle = int(sys.argv[1])

def home():
	addDir('New','http://amvnews.ru/index.php?go=Files&in=newfiles&per=4&lang=en',6,image)
	addDir('Videos','http://amvnews.ru/index.php?go=Files&in=abc&lang=en',1,image)
	addDir('Anime','http://amvnews.ru/index.php?go=Anime&letter=A&lang=en',2,image)
	addDir('Ratings','http://amvnews.ru/index.php?go=Ratings&lang=en',3,image)
	addDir('Categories','http://amvnews.ru/?lang=en',4,image)
	addDir('Competitions','http://amvnews.ru/?lang=en',5,image)
	addDir('Random Top10','http://amvnews.ru/?lang=en',13,image)
	addDir('AMV TV','http://amvnews.ru/index.php?go=Files&in=newfiles&per=4&lang=en',20,image,folder=False)
	addDir('Search','http://amvnews.ru/index.php?go=Search&modname=Files&query=',11,image)
	addDir('My Videos',myvideos,16,image)
	xbmcplugin.endOfDirectory(pluginhandle)

def myVideos():
	if os.path.exists(myvideos):
	  fh = open(myvideos, 'r')
	  content = fh.read()
	  match = re.findall('{"name":"(.*?)","url":"(.*?)","anime":"(.*?)","cover":"(.*?)","music":"(.*?)","author":"(.*?)","aurl":"(.*?)"}', content, re.DOTALL)
	  for name,url,anime,cover,music,author,aurl in match:
	    artist = music.split('-')
	    artist = str(artist[0])
	    plot = music + '\n' + anime
	    search = 'http://amvnews.ru/index.php?go=Search&modname=Files&query=' + artist
	    cm = []
	    u=sys.argv[0]+"?url="+urllib.quote_plus(search)+"&mode="+urllib.quote_plus('14')
	    cm.append( ('More %s' % artist, "Container.Update(%s)" % u) )
	    u=sys.argv[0]+"?url="+urllib.quote_plus(aurl)+"&mode="+urllib.quote_plus('15')
	    cm.append( ('%s' % author, "Container.Update(%s)" % u) )
	    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&name="+urllib.quote_plus(name)+"&mode="+urllib.quote_plus('18')
	    cm.append( ('Remove from My Videos', "XBMC.RunPlugin(%s)" % u) )
	    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&name="+urllib.quote_plus(name)+"&mode="+urllib.quote_plus('19')
	    cm.append( ('Download AMV', "XBMC.RunPlugin(%s)" % u) )
	    addLink(name,url,7,cover,plot,cm=cm)
	    fh.close()

def addVideo(url,name):
	content = getUrl(url)
	match = re.findall('Anime</b>:(.*?)<.*?Music</b>:(.*?)<.*?/images/(.*?)".*?Author:.*?<a href="(.*?)" title="(.*?)">', content)
	for anime,music,thumb,aurl,author in match:
	  thumb = 'http://amvnews.ru/images/' + thumb
	  aurl = 'http://amvnews.ru' + aurl + '&lang=en'
	  amventry = '{"name":"'+name+'","url":"'+url+'","anime":"'+anime+'","cover":"'+thumb+'","music":"'+music+'","author":"'+author+'","aurl":"'+aurl+'"}'
	  if os.path.exists(myvideos):
	    fh = open(myvideos, 'r')
	    content = fh.read()
	    fh.close()
	    if content.find(amventry) == -1:
	      fh = open(myvideos, 'a')
	      fh.write(amventry+"\n")
	      fh.close()
	  else:
	    fh = open(myvideos, 'a')
	    fh.write(amventry+"\n")
	    fh.close()
	  xbmc.executebuiltin('XBMC.Notification(Info: Video Added!,)')

def remVideo(url,name):
	fh = open(myvideos, 'r')
	content = fh.read()
	fh.close()
	match = re.findall(r'\{(.*?)\}', content)
	for amv in match:
	  if name in amv:
	    fh = open(myvideos, 'w')
	    fh.write(content.replace("{"+amv+"}"+"\n", ""))
	    fh.close()
	    xbmc.executebuiltin('XBMC.Notification(Info: Video Removed!,)')

def abc(url):
	content = getUrl(url)
	match = re.findall('<tr><td align="center">(.*?)</td></tr>', content)
	rematch = re.findall('<a href="(.*?)">(.*?)<', match[0])
	for url,name in rematch:
	  url = 'http://amvnews.ru/' + url + '&lang=en'
	  addDir(name,url,6,image)
	xbmcplugin.endOfDirectory(pluginhandle)

def abc2(url):
	content = getUrl(url)
	match = re.findall('<div style="float: left;">(.*?)</div>', content)
	rematch = re.findall('<a href="(.*?)".*?">(.*?)</span></a>', match[0])
	for url,name in rematch:
	  url = 'http://amvnews.ru/' + url + '&lang=en'
	  addDir(name,url,8,image)
	xbmcplugin.endOfDirectory(pluginhandle)

def anime(url):
	content = getUrl(url)
	match = re.findall('<tr class="anime_tablerow.*?"><td><a href="(.*?)">(.*?)</a>', content)
	for url,name in match:
	  url = 'http://amvnews.ru' + url + '&lang=en'
	  addDir(name,url,9,image)
	xbmcplugin.endOfDirectory(pluginhandle)

def animeamv(url):
	content = getUrl(url)
	match = re.findall('<tr class="ratesrow.*?<a href="(.*?)">(.*?)</a>', content)
	for url,name in match:
	  name = name.replace('<span>','').replace('</span>','')
	  url = 'http://amvnews.ru' + url + '&lang=en'
	  if addon.getSetting('info') == 'true':
	    getInfo(url,name)
	  else:
	    cm = []
	    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&name="+urllib.quote_plus(name)+"&mode="+urllib.quote_plus('17')
	    cm.append( ('Add to My Videos', "XBMC.RunPlugin(%s)" % u) )
	    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&name="+urllib.quote_plus(name)+"&mode="+urllib.quote_plus('19')
	    cm.append( ('Download AMV', "XBMC.RunPlugin(%s)" % u) )
	    addLink(name,url,7,'','',cm=cm)
	xbmcplugin.endOfDirectory(pluginhandle)

def ratings(url):
	content = getUrl(url)
	match = re.findall('<center><H3>Videos ratings</H3></center>(.*?)<center><H3>Author ratings</H3>', content)
	rematch = re.findall('<a href="(.*?)">(.*?)<', match[0])
	for url,name in rematch:
	  url = 'http://amvnews.ru/' + url + '&lang=en'
	  addDir(name,url,10,image)
	addDir('Most popular authors','http://amvnews.ru/index.php?go=Ratings&file=byauthor&lang=en',15,image)
	addDir('Most popular AMV-studios','http://amvnews.ru/index.php?go=Ratings&file=bystudio&lang=en',15,image)
	xbmcplugin.endOfDirectory(pluginhandle)

def rateamv(url):
	content = getUrl(url)
	match = re.findall('<tr class="ratesrow.*?<a href=(.*?) class.*?>(.*?)</a>', content)
	for url,name in match:
	  url = 'http://amvnews.ru/' + url + '&lang=en'
	  if addon.getSetting('info') == 'true':
	    getInfo(url,name)
	  else:
	    cm = []
	    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&name="+urllib.quote_plus(name)+"&mode="+urllib.quote_plus('17')
	    cm.append( ('Add to My Videos', "XBMC.RunPlugin(%s)" % u) )
	    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&name="+urllib.quote_plus(name)+"&mode="+urllib.quote_plus('19')
	    cm.append( ('Download AMV', "XBMC.RunPlugin(%s)" % u) )
	    addLink(name,url,7,'','',cm=cm)
	nextmatch = re.findall('<div  class="navigation-right-div"><a href="(.*?)">.*?title="(.*?)">', content)
	for url,name in nextmatch:
	  url = 'http://amvnews.ru/' + url + '&lang=en'
	  addDir(name,url,10,'')
	xbmcplugin.endOfDirectory(pluginhandle)

def rateauthor(url):
	content = getUrl(url)
	match = re.findall('<tr class="ratesrow.*?<a href="(.*?)">(.*?)</a>', content)
	for url,name in match:
	  url = 'http://amvnews.ru/' + url + '&lang=en'
	  if 'go=Files' in url:
	    if addon.getSetting('info') == 'true':
	      getInfo(url,name)
	    else:
	      cm = []
	      u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&name="+urllib.quote_plus(name)+"&mode="+urllib.quote_plus('17')
	      cm.append( ('Add to My Videos', "XBMC.RunPlugin(%s)" % u) )
	      u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&name="+urllib.quote_plus(name)+"&mode="+urllib.quote_plus('19')
	      cm.append( ('Download AMV', "XBMC.RunPlugin(%s)" % u) )
	      addLink(name,url,7,'','',cm=cm)
	  else:
	    addDir(name,url,15,image)
	nextmatch = re.findall('<div  class="navigation-right-div"><a href="(.*?)">.*?title="(.*?)">', content)
	for url,name in nextmatch:
	  url = 'http://amvnews.ru/' + url + '&lang=en'
	  addDir(name,url,15,'')
	xbmcplugin.endOfDirectory(pluginhandle)

def categories(url):
	content = getUrl(url)
	match = re.findall('Categories(.*?)Competitions', content)
	rematch = re.findall('<a href="(index.*?)" title.*?>(.*?)<', match[0])
	for url,name in rematch:
	  url = 'http://amvnews.ru/' + url + '&lang=en'
	  addDir(name,url,6,image)
	xbmcplugin.endOfDirectory(pluginhandle)

def competitions(url):
	content = getUrl(url)
	match = re.findall('AMV News:.*?<a href="(.*?)" title.*?>(.*?)<', content)
	for url,name in match:
	  url = 'http://amvnews.ru/' + url + '&lang=en'
	  addDir(name,url,6,image)
	xbmcplugin.endOfDirectory(pluginhandle)

def random(url):
	content = getUrl(url)
	match = re.findall('Top 10(.*?)</table></div>', content)
	rematch = re.findall(r'<a href=(index.php\?go=Files.*?) class="top10">(.*?)</a>', match[0])
	for url,name in rematch:
	  url = 'http://amvnews.ru/' + url + '&lang=en'
	  if addon.getSetting('info') == 'true':
	    getInfo(url,name)
	  else:
	    cm = []
	    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&name="+urllib.quote_plus(name)+"&mode="+urllib.quote_plus('17')
	    cm.append( ('Add to My Videos', "XBMC.RunPlugin(%s)" % u) )
	    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&name="+urllib.quote_plus(name)+"&mode="+urllib.quote_plus('19')
	    cm.append( ('Download AMV', "XBMC.RunPlugin(%s)" % u) )
	    addLink(name,url,7,'','',cm=cm)
	xbmcplugin.endOfDirectory(pluginhandle)

def amvs(url):
	content = getUrl(url)
	match = re.findall('<a class=newstitle href=(.*?)>(.*?)</a>.*?Аниме</b>:(.*?)<.*?Музыка</b>:(.*?)<.*?/images/(.*?)".*?Rating: (.*?)<', content)
	for url,title,anime,music,thumb,rating in match:
	  url = 'http://amvnews.ru/' + url + '&lang=en'
	  name = title + '  (' + rating + ')'
	  artist = music.split('-')
	  artist = str(artist[0])
	  plot = music + '\n' + anime
	  thumb = 'http://amvnews.ru/images/' + thumb
	  search = 'http://amvnews.ru/index.php?go=Search&modname=Files&query=' + artist
	  cm = []
	  u=sys.argv[0]+"?url="+urllib.quote_plus(search)+"&mode="+urllib.quote_plus('14')
	  cm.append( ('More %s' % artist, "Container.Update(%s)" % u) )
	  u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&name="+urllib.quote_plus(title)+"&mode="+urllib.quote_plus('17')
	  cm.append( ('Add to My Videos', "XBMC.RunPlugin(%s)" % u) )
	  u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&name="+urllib.quote_plus(title)+"&mode="+urllib.quote_plus('19')
	  cm.append( ('Download AMV', "XBMC.RunPlugin(%s)" % u) )
	  addLink(name,url,7,thumb,plot,cm=cm)
	nextmatch = re.findall('<div  class="navigation-right-div"><a href="(.*?)">.*?title="(.*?)">', content)
	for url,name in nextmatch:
	  url = 'http://amvnews.ru/' + url + '&lang=en'
	  addDir(name,url,6,'')
	xbmcplugin.endOfDirectory(pluginhandle)

def play(url):
	method = addon.getSetting('method')
	if method == 'Torrent':
	  url = url.replace("in=view","file=downtorrent")
	  r = requests.get(url)
	  url = r.url
	else:
	  stream = url.replace("in=view","file=down")
	  r = requests.get(stream, stream=True)
	  url = r.url
	if amvfolder:
	  file = amvfolder + url.split('/')[-1]
	  if os.path.exists(file):
	    stream = file
	  else:
	    if method == 'Preview':
	      stream = stream + '&alt=4'
	    elif method == 'Torrent':
	      stream = "plugin://plugin.video.xbmctorrent/play/" + urllib.quote_plus(url)
	elif method == 'Preview':
	  stream = stream + '&alt=4'
	elif method == 'Torrent':
	  stream = "plugin://plugin.video.xbmctorrent/play/" + urllib.quote_plus(url)
	listitem = xbmcgui.ListItem(path = stream)
	return xbmcplugin.setResolvedUrl(pluginhandle, True, listitem)

def playRandom(url):
	content = getUrl(url)
	last = re.findall('<a class=newstitle href=.+?id=(.*?)>', content)
	playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
	playlist.clear()
	a = 1
	while a < 101:
	  a += 1
	  r = randint(1,int(last[0]))
	  url = 'http://amvnews.ru/index.php?go=Files&in=view&id=' + str(r)
	  u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(7)+"&name="+urllib.quote_plus(str(r))
	  item=xbmcgui.ListItem(name)
	  playlist.add(url=u, listitem=item)
	xbmc.Player().play(playlist)

def download(url):
	url = url.replace("in=view","file=down")
	r = requests.get(url, stream=True)
	if r:
	  url = r.url
	  if amvfolder:
	    file = amvfolder + url.split('/')[-1]
	    if os.path.exists(file):
	      xbmc.executebuiltin('XBMC.Notification(Info: Video Already Downloaded!,)')
	    else:
	      xbmc.executebuiltin('XBMC.Notification(Info: Download Started!,)')
	      with open(file, 'wb') as f:
	        for chunk in r.iter_content(chunk_size=1024): 
	          if chunk:
	            f.write(chunk)
	            f.flush()
	      xbmc.executebuiltin('XBMC.Notification(Info: Download Complete!,)')
	  else:
	    addon.openSettings()
	else:
	  xbmc.executebuiltin('XBMC.Notification(Info: Download Not Possible!,)')

def search(url):
	kb = xbmc.Keyboard('', 'AMV Search', False)
	kb.doModal()
	search_entered = kb.getText().replace(' ','+')
	url = url + search_entered
	result(url)
	nexturl = url  + '&lang=en'
	content = getUrl(nexturl)
	if 'Next page' in content:
	  nextmatch = re.findall('<div  class="navigation-right-div"><a href="(.*?)">.*?title="(.*?)">', content)
	  for url,name in nextmatch:
	    url = 'http://amvnews.ru/' + url + '&lang=en'
	    addDir(name,url,12,'')
	xbmcplugin.endOfDirectory(pluginhandle)

def searchArtist(url):
	result(url.replace(" ","%20"))
	nexturl = url + '&lang=en'
	content = getUrl(nexturl)
	if 'Next page' in content:
	  nextmatch = re.findall('<div  class="navigation-right-div"><a href="(.*?)">.*?title="(.*?)">', content)
	  for url,name in nextmatch:
	    url = 'http://amvnews.ru/' + url + '&lang=en'
	    addDir(name,url,12,'')
	xbmcplugin.endOfDirectory(pluginhandle)

def result(url):
	content = getUrl(url)
	match = re.findall('<td width=100% valign=top><b><a href="(.*?)" target="_blank">(.*?)</a>', content)
	for url,name in match:
	  url = 'http://amvnews.ru/' + url + '&lang=en'
	  if addon.getSetting('info') == 'true':
	    getInfo(url,name)
	  else:
	    cm = []
	    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&name="+urllib.quote_plus(name)+"&mode="+urllib.quote_plus('17')
	    cm.append( ('Add to My Videos', "XBMC.RunPlugin(%s)" % u) )
	    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&name="+urllib.quote_plus(name)+"&mode="+urllib.quote_plus('19')
	    cm.append( ('Download AMV', "XBMC.RunPlugin(%s)" % u) )
	    addLink(name,url,7,'','',cm=cm)

def getInfo(url,name):
	content = getUrl(url)
	match = re.findall('Anime</b>:(.*?)<.*?Music</b>:(.*?)<.*?/images/(.*?)".*?Author:.*?<a href="(.*?)" title="(.*?)">.*?itemprop="ratingValue">(.*?)<', content)
	for anime,music,thumb,aurl,author,rating in match:
	  title = name
	  name = name + '  (' + rating + ')'
	  artist = music.split('-')
	  artist = str(artist[0])
	  plot = music + '\n' + anime
	  thumb = 'http://amvnews.ru/images/' + thumb
	  aurl = 'http://amvnews.ru' + aurl + '&lang=en'
	  search = 'http://amvnews.ru/index.php?go=Search&modname=Files&query=' + artist
	  cm = []
	  u=sys.argv[0]+"?url="+urllib.quote_plus(search)+"&mode="+urllib.quote_plus('14')
	  cm.append( ('More %s' % artist, "Container.Update(%s)" % u) )
	  u=sys.argv[0]+"?url="+urllib.quote_plus(aurl)+"&mode="+urllib.quote_plus('15')
	  cm.append( ('%s' % author, "Container.Update(%s)" % u) )
	  u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&name="+urllib.quote_plus(title)+"&mode="+urllib.quote_plus('17')
	  cm.append( ('Add to My Videos', "XBMC.RunPlugin(%s)" % u) )
	  u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&name="+urllib.quote_plus(title)+"&mode="+urllib.quote_plus('19')
	  cm.append( ('Download AMV', "XBMC.RunPlugin(%s)" % u) )
	  addLink(name,url,7,thumb,plot,cm=cm)

def getUrl(url):
	headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:27.0) Gecko/20100101 Firefox/27.0'}
	content = requests.get(url, headers=headers).content
	content = content.decode('windows-1251').encode('utf-8', 'ignore')
	content = content.replace("\n","").replace("\t","").replace("&amp;","&").replace("&ndash;","-").replace("<BR>","").replace("</B>","</b>").replace(' title="Socks5 proxy 50"','')
	return content

def get_params():
	param=[]
	paramstring=sys.argv[2]
	if len(paramstring)>=2:
		params=sys.argv[2]
		cleanedparams=params.replace('?','')
		if (params[len(params)-1]=='/'):
			params=params[0:len(params)-2]
		pairsofparams=cleanedparams.split('&')
		param={}
		for i in range(len(pairsofparams)):
			splitparams={}
			splitparams=pairsofparams[i].split('=')
			if (len(splitparams))==2:
				param[splitparams[0]]=splitparams[1]
				
	return param

def addLink(name,url,mode,iconimage,plot,cm=False):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
	item=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
	item.setInfo( type="Video", infoLabels={ "Title": name, "Plot": plot } )
	item.setProperty('IsPlayable', 'true')
	if cm:
	  item.addContextMenuItems( cm )
	xbmcplugin.addDirectoryItem(pluginhandle,url=u,listitem=item)

def addDir(name,url,mode,iconimage,folder=True):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)
	item=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	item.setInfo( type="Video", infoLabels={ "Title": name } )
	xbmcplugin.addDirectoryItem(pluginhandle,url=u,listitem=item,isFolder=folder)
	      
params=get_params()
url=None
name=None
mode=None

try:
	url=urllib.unquote_plus(params["url"])
except:
	pass
try:
	name=urllib.unquote_plus(params["name"])
except:
	pass
try:
	mode=int(params["mode"])
except:
	pass

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)

if mode==None:
	print ""
	home()      

elif mode==1:
	print ""+url
	abc(url)
	
elif mode==2:
	print ""+url
	abc2(url)

elif mode==3:
	print ""+url
	ratings(url)

elif mode==4:
	print ""+url
	categories(url)

elif mode==5:
	print ""+url
	competitions(url)

elif mode==6:
	print ""
	amvs(url)

elif mode==7:
	print ""+url
	play(url)

elif mode==8:
	print ""+url
	anime(url)

elif mode==9:
	print ""+url
	animeamv(url)

elif mode==10:
	print ""+url
	rateamv(url)

elif mode==11:
	print ""+url
	search(url)

elif mode==12:
	print ""+url
	result(url)

elif mode==13:
	print ""+url
	random(url)

elif mode==14:
	print ""+url
	searchArtist(url)

elif mode==15:
	print ""+url
	rateauthor(url)

elif mode==16:
	print ""+url
	myVideos()

elif mode==17:
	print ""+url
	addVideo(url,name)

elif mode==18:
	print ""+url
	remVideo(url,name)

elif mode==19:
	download(url)

elif mode==20:
	playRandom(url)

xbmcplugin.endOfDirectory(int(sys.argv[1]))