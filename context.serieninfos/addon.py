#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import re
import xbmc
import xbmcgui
import xbmcaddon
PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3
if PY2:
	from urllib import quote, unquote, quote_plus, unquote_plus, urlencode  # Python 2.X
	try:
		import StorageServer
	except ImportError:
		from resources.lib import storageserverdummy as StorageServer
elif PY3:
	from urllib.parse import quote, unquote, quote_plus, unquote_plus, urlencode  # Python 3+
import json
import xbmcvfs
import shutil
import socket
import datetime
import time
import requests
try:
	from requests.packages.urllib3.exceptions import InsecureRequestWarning
	requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
except: pass
import pyxbmct
import xml.etree.ElementTree as ET
from difflib import SequenceMatcher


global debuging
addon = xbmcaddon.Addon()
socket.setdefaulttimeout(30)
addonPath = xbmc.translatePath(addon.getAddonInfo('path')).encode('utf-8').decode('utf-8')
dataPath = xbmc.translatePath(addon.getAddonInfo('profile')).encode('utf-8').decode('utf-8')
icon = os.path.join(addonPath, 'icon.png')
if PY2:
	cachePERIOD = 24
	cache = StorageServer.StorageServer(addon.getAddonInfo('id'), cachePERIOD) # (Your plugin name, Cache time in hours)
themovieDB_apiKEY = "f5bfabe7771bad8072173f7d54f52c35"
glotzINFO_apiKEY = "U88E9UV2BLYSSBO3"
##### glotzINFO: NEW-apikey = U88E9UV2BLYSSBO3 #####
##### glotzINFO: OTHER apikey from NET = 0629B785CE550C8D #####

def py2_enc(s, encoding='utf-8'):
	if PY2 and isinstance(s, unicode):
		s = s.encode(encoding)
	return s

def py2_uni(s, encoding='utf-8'):
	if PY2 and isinstance(s, str):
		s = unicode(s, encoding)
	return s

def py3_dec(d, encoding='utf-8'):
	if PY3 and isinstance(d, bytes):
		d = d.decode(encoding)
	return d

def failing(content):
	log(content, xbmc.LOGERROR)

def debug(content):
	log(content, xbmc.LOGDEBUG)

def log(msg, level=xbmc.LOGNOTICE):
	msg = py2_enc(msg)
	xbmc.log("["+addon.getAddonInfo('id')+"-"+addon.getAddonInfo('version')+"]"+msg, level)
  
def makeREQUEST(url):
	if PY2:
		INQUIRE = cache.cacheFunction(getUrl, url)
	elif PY3:
		INQUIRE = getUrl(url)
	return INQUIRE

def getUrl(url, __HEADERS=False, __TIMEOUT=30):
	debug("(getUrl) ##### URL = "+url+" #####")
	ip = addon.getSetting("ip")
	port = addon.getSetting("port")
	response = requests.Session()
	if not __HEADERS:
		__HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:55.0) Gecko/20100101 Firefox/55.0'}
	if ip !="" and port !="":
		px ="http://"+ip+":"+str(port)
		__PROXIES = {'http': px,'https': px}
		content = response.get(url, allow_redirects=True, verify=False, headers=__HEADERS, proxies=__PROXIES, timeout=__TIMEOUT).text
	else:
		content = response.get(url, allow_redirects=True, verify=False, headers=__HEADERS, timeout=__TIMEOUT).text
	return content

class Infowindow(pyxbmct.AddonDialogWindow):
	text =""
	pos = 0
	def __init__(self, title='', text='', image="", lastplayd_title="", lastepisode_name="", fehlen=""):
		super(Infowindow, self).__init__(title)
		self.setGeometry(750, 650, 16, 8)
		self.bild = image
		self.text = text
		self.fehlen = fehlen
		self.lastplayd_title = lastplayd_title
		self.lastepisode_name = lastepisode_name
		self.set_info_controls()
		# Connect a key action (Backspace) to close the window.
		self.connect(pyxbmct.ACTION_NAV_BACK, self.close)

	def set_info_controls(self):
		self.image = pyxbmct.Image(self.bild)
		self.placeControl(self.image, 0, 0, columnspan=8, rowspan=4)
		if fehlen !="":
			self.textbox = pyxbmct.TextBox()
			self.placeControl(self.textbox, 4, 0, columnspan=8, rowspan=10)
			self.textbox.setText(self.text)
			self.textbox.autoScroll(5000, 1500, 2000)
			self.textbox2 = pyxbmct.TextBox()
			self.placeControl(self.textbox2, 14, 0, columnspan=8, rowspan=1)
			self.textbox2.setText("[COLOR FFFF5F00][B]Fehlende Folgen : [/B][/COLOR]"+self.fehlen) # R = 255|G = 95|B = 0
		else:
			self.textbox = pyxbmct.TextBox()
			self.placeControl(self.textbox, 4, 0, columnspan=8, rowspan=11)
			self.textbox.setText(self.text)
			self.textbox.autoScroll(5000, 1500, 2000)
		self.textbox3 = pyxbmct.TextBox()
		self.placeControl(self.textbox3, 15, 0, columnspan=4, rowspan=1)
		self.textbox3.setText("[COLOR FFFFEB00][B]Zuletzt gesehen : [/B][/COLOR]"+self.lastplayd_title) # R = 255|G = 235|B = 0
		self.textbox4 = pyxbmct.TextBox()
		self.placeControl(self.textbox4, 15, 5, columnspan=3 ,rowspan=1)
		self.textbox4.setText("[COLOR FF00F000][B]Vorhanden bis : [/B][/COLOR]"+self.lastepisode_name) # R = 0|G = 240|B = 0

		self.connectEventList(
			[pyxbmct.ACTION_MOVE_UP,
			pyxbmct.ACTION_MOUSE_WHEEL_UP],
			self.hoch)
		self.connectEventList(
			[pyxbmct.ACTION_MOVE_DOWN,
			pyxbmct.ACTION_MOUSE_WHEEL_DOWN],
			self.runter)
		self.setFocus(self.textbox)
	def hoch(self):
		self.pos = self.pos-1
		if self.pos < 0:
			self.pos = 0
		self.textbox.scroll(self.pos)
	def runter(self):
		self.pos = self.pos+1
		self.textbox.scroll(self.pos)
		posnew = self.textbox.getPosition()

def fixtime(date_string, format):
	debug("(fixtime) ##### date_string :"+str(date_string)+" ##### format : "+str(format)+" #####")
	try:
		x=datetime.datetime.strptime(date_string, format)
	except TypeError:
		x=datetime.datetime(*(time.strptime(date_string, format)[0:6])) 
	return x

def similar(a, b):
	return SequenceMatcher(None, a, b).ratio()

def getTitle():
	title =""
	title = xbmc.getInfoLabel('ListItem.TVShowTitle')
	try:
		info = sys.listitem.getVideoInfoTag()
		title = info.getTVShowTitle()
	except: pass
	try: title = xbmc.getInfoLabel('ListItem.TVShowTitle')
	except: pass
	if title =="":
		title = xbmc.getInfoLabel("ListItem.Title").decode('utf-8')
	if title =="":
		title = sys.listitem.getLabel()
	debug("(getTitle) ##### TITLE : "+title+" #####")
	return title

def getEpisodedata(title):
	query = {"jsonrpc": "2.0", "method": "VideoLibrary.GetEpisodes", "params": { "filter": { "field": "tvshow", "operator": "is", "value": "" }, "limits": { "start" : 0 }, "properties": ["playcount", "runtime", "tvshowid","episode","season"], "sort": { "order": "ascending", "method": "label" } }, "id": "libTvShows"}
	query = json.loads(json.dumps(query))
	query['params']['filter']['value'] = title
	response = json.loads(xbmc.executeJSONRPC(json.dumps(query)))
	lastplayd_nr = 0
	lastplayd_title =""
	lastplayd_staffel = 1
	lastepisode_nr = 0
	lastepisode_name ="" 
	lastepisode_staffel = 1
	fehlen =""
	try:
		for episode in response["result"]["episodes"]:
			debug("--------------------------------------------------------------------------------------")
			debug("(getEpisodedata) ##### RESPONSE : "+str(episode)+" #####")
			if episode["playcount"] > 0:
				if lastplayd_nr < episode["episode"] or lastplayd_staffel<episode["season"]:
					lastplayd_nr = episode["episode"]
					lastplayd_staffel = episode["season"]
					lastplayd_title ="S"+str(episode["season"])+"E"+str(episode["episode"])
			if lastepisode_nr < episode["episode"] or lastepisode_staffel < episode["season"]:
				if lastepisode_staffel < episode["season"]:
					lastepisode_nr = 0
				count = episode["episode"]-lastepisode_nr
				if count > 1:
					debug("(getEpisodedata) ##### lastepisode_nr : "+str(lastepisode_nr)+" #####")
					debug("(getEpisodedata) ##### episode : "+str(episode["episode"])+" #####")
					if count == 2:
						fehlen = fehlen+","+"S"+str(episode["season"])+"E"+str(lastepisode_nr+1)
					if count > 2:
						fehlen = fehlen+","+"S"+str(lastepisode_staffel)+"E"+str(lastepisode_nr+1)+" - "+"S"+str(episode["season"])+"E"+str(episode["episode"]-1)
				lastepisode_nr = episode["episode"]
				lastepisode_name ="S"+str(episode["season"])+"E"+str(episode["episode"])
				lastepisode_staffel = episode["season"] 
		if len(fehlen) > 0:
			fehlen = fehlen[1:]
			debug("(getEpisodedata) ##### lastplayd_title : "+lastplayd_title+" #####")
			debug("(getEpisodedata) ##### lastepisode_name : "+lastepisode_name+" #####")
			debug("(getEpisodedata) ##### fehlen : "+fehlen+" #####")
	except: pass
	return lastplayd_title, lastepisode_name, fehlen

def get_all_Episodes(idd):
	url ="https://api.themoviedb.org/3/tv/"+str(idd)+"?api_key="+themovieDB_apiKEY+"&language=en_US"
	debug("(get_all_Episodes) ##### URL : "+url+" #####")
	try:
		content = makeREQUEST(url)
		structure = json.loads(content)
	except:
		content = getUrl(url)
		structure = json.loads(content)
	now = datetime.datetime.now()
	last = fixtime("1900-01-01", "%Y-%m-%d")
	next = fixtime("2200-01-01", "%Y-%m-%d")
	lastdatum =""
	lastepisode =""
	nextepisode =""
	nextdatum =""
	for season in structure["seasons"]:
		nr = season["season_number"]
		if int(nr) == 0:
			continue
		seasonurl ="https://api.themoviedb.org/3/tv/"+str(idd)+"/season/"+str(nr)+"?api_key="+themovieDB_apiKEY+"&language=en_US"
		debug("(get_all_Episodes) ##### seasonurl : "+seasonurl+" #####")
		try:
			content2 = makeREQUEST(seasonurl)
			structure = json.loads(content2)
		except:
			content2 = getUrl(seasonurl)
			structure = json.loads(content2)
		debug("(get_all_Episodes) ##### structure : "+str(structure)+" #####")
		for episode in structure["episodes"]:
			debug("(get_all_Episodes) ##### episode : "+str(episode)+" #####")
			datum = episode["air_date"]
			nummer = episode["episode_number"]
			season = episode["season_number"]
			try:
				date1 = fixtime(datum, "%Y-%m-%d")      
				if date1 > now and date1 < next:
					nextdatum = datum
					nextepisode ="S"+str(season)+"E"+str(nummer)
					next = date1
				if date1 < now and date1 > last:
					lastdatum = datum
					lastepisode ="S"+str(season)+"E"+str(nummer)
					last = date1
				debug("(get_all_Episodes) ##### datum : "+datum+" = S"+str(season)+"E"+str(nummer)+" #####")
			except: pass
	debug("(get_all_Episodes) ##### LASTDATUM : "+lastdatum+" | LASTEPISODE : "+lastepisode+" #####")
	debug("(get_all_Episodes) ##### NEXTDATUM : "+nextdatum+" | NEXTEPISODE : "+nextepisode+" #####")
	return (nextdatum, nextepisode, lastdatum, lastepisode)

def parameters_string_to_dict(parameters):
	paramDict = {}
	if parameters:
		paramPairs = parameters[1:].split("&")
		for paramsPair in paramPairs:
			paramSplits = paramsPair.split('=')
			if (len(paramSplits)) == 2:
				paramDict[paramSplits[0]] = paramSplits[1]
	return paramDict

debug("##### Hole Parameter #####")
debug("##### Argv #####")
debug(str(sys.argv))
debug("---------------------------------------")
try:
	params = parameters_string_to_dict(sys.argv[2])
	mode = unquote_plus(params.get('mode', ''))
	series = unquote_plus(params.get('series', ''))
	season = unquote_plus(params.get('season', ''))
	debug("##### Parameter holen geklappt #####")
except:
	debug("##### Parameter holen NICHT geklappt #####")
	mode ="" 
debug("#### Der aktuelle MODE ist : "+str(mode)+" #####")

if mode =="":
	title = getTitle()
	lastplayd_title, lastepisode_name, fehlen = getEpisodedata(title)
	title = re.sub('\(.+?\)', '', title)
	url ="https://api.themoviedb.org/3/search/tv?api_key="+themovieDB_apiKEY+"&language=de-DE&query=" + title.replace(" ","+")
	debug("(modeEMPTY) ##### Searchurl : "+url+" #####")
	try:
		content = makeREQUEST(url)
		wert = json.loads(content)
	except:
		content = getUrl(url)
		wert = json.loads(content)
	count = 0
	gefunden1 = 0
	gefunden2 = 0
	wertnr1 = 0
	wertnr2 = 0
	x1 = 0
	x2 = 0
	x = 0
	for serie in wert["results"]:
		serienname1 = serie["original_name"].encode("utf-8")
		serienname2 = serie["name"].encode("utf-8")
		debug("(modeEMPTY) ##### serienname2 : "+serienname2+" #####")
		debug("(modeEMPTY) ##### serienname1 : "+serienname1+" #####")
		nummer1 = similar(title,serienname1)
		nummer2 = similar(title,serienname2)  
		if nummer1 > wertnr1:
			wertnr1 = nummer1
			gefunden1 = count
			x1 = 1
		if nummer2 > wertnr2:
			wertnr2 = nummer2
			gefunden2 = count
			x2 = 1
		count += 1
	debug("(modeEMPTY) ##### WertNR-1 : "+str(wertnr1)+" | WertNR-1 : "+str(wertnr2)+" #####")
	if float(wertnr2) > float(wertnr1):
		x = x2
		gefunden = gefunden2
	else:
		x = x1
		gefunden = gefunden1
	debug("(modeEMPTY) ##### X : "+ str(x)+" #####")
	debug("(modeEMPTY) ##### gefunden : "+ str(gefunden)+" #####")
	debug("1. +++ Suche +++"+title)
	if x ==0:
		xbmcgui.Dialog().ok(addon.getAddonInfo('name'), '[COLOR orangered]!!![/COLOR] Serie * [COLOR chartreuse]'+title+'[/COLOR] * leider NICHT gefunden [COLOR orangered]!!![/COLOR]')
	else:
		tvdbid = False
		de_last ="\n"
		de_next =""
		debug("****************************************************") 
		debug("(modeEMPTY) ##### WEITERMACHEN #####")
		idd = wert["results"][gefunden]["id"]
		debug("(modeEMPTY) ##### IDD: "+str(idd)+" #####")
		seriesName = wert["results"][gefunden]["name"]
		serienstart = wert["results"][gefunden]["first_air_date"]
		(nextdatum, nextfolge, lastdatum, lastfolge) = get_all_Episodes(idd)
		leztefolge = lastfolge
		debug("3. +++++ Serie +++++")
		try:
			Bild ="http://image.tmdb.org/t/p/w500"+wert["results"][gefunden]["backdrop_path"].encode("utf-8")
		except: Bild =""
		debug("(modeEMPTY) ##### Bild : "+Bild+" #####")
		serienurl="https://api.themoviedb.org/3/tv/"+str(idd)+"?api_key="+themovieDB_apiKEY+"&language=de-DE"
		debug("(modeEMPTY) ##### serienurl : "+serienurl+" #####")
		try:
			content_serie = makeREQUEST(serienurl) 
			struct_serie = json.loads(content_serie)
		except:
			content_serie = getUrl(serienurl) 
			struct_serie = json.loads(content_serie)
		status = struct_serie["status"].decode("utf-8")
		statustext ="Der Status der Serie ist : "+status
		if status =="Returning Series":
			statustext ="Akt. Status :          Fortsetzung"
		if status =="Canceled":
			statustext ="Akt. Status :          Abgesetzt"
		if status =="Ended":
			statustext ="Akt. Status :          Beendet"
		# Continuing
		try:
			sender = struct_serie["Networks"][0].decode("utf-8")
		except: sender =""
		if sender =="":
			sendertext =""
		else:
			sendertext ="Sender :         "+sender
		titlesuche = struct_serie["name"]
		try:
			nextfolge = nextfolge
		except:
			nextfolge =""
		if nextfolge =="":
			textnext =""
		else:
			textnext ="Nächste Folge :\n     US : "+nextfolge+" ( "+nextdatum+" )"
		eidurl ="https://api.themoviedb.org/3/tv/"+str(idd)+"/external_ids?api_key="+themovieDB_apiKEY+"&language=de-DE"
		debug("(modeEMPTY) ##### eidurl : "+eidurl+" #####")
		try:
			content = makeREQUEST(eidurl)
			wwert = json.loads(content)
		except:
			content = getUrl(eidurl) 
			wwert = json.loads(content)
		tvdbid = str(wwert["tvdb_id"])
		if not tvdbid or tvdbid == "None":
			tvdbid = str(idd)
		debug("(modeEMPTY) ##### tvdbid : "+str(tvdbid)+" #####")
		try:
			getnextde ="https://www.glotz.info/api/"+glotzINFO_apiKEY+"/series/"+tvdbid+"/all/de.xml"
			debug("(modeEMPTY) ##### getnextde : "+getnextde+" #####")
			try:
				content = makeREQUEST(getnextde)
				root = ET.fromstring(content)
			except:
				content = getUrl(getnextde)
				root = ET.fromstring(content)
		except: root = ""
		if root !="":
			now = time.time()
			next = 5000000000
			last = 0
			next_EpisodeNumber =""
			next_SeasonNumber =""
			last_EpisodeNumber =""
			last_SeasonNumber =""
			for serie in root.findall('Series'):
				desender = serie.find('Network').text
				if desender == None:
					desender =""
				debug("(modeEMPTY) ##### NETWORK : "+str(desender)+" #####")
				dezeit = serie.find('Airs_Time').text
				if dezeit == None:
					dezeit = ""
				debug("(modeEMPTY) ##### AIRS_TIME : "+str(dezeit)+" #####")
			for episode in root.findall('Episode'):
				try:
					start = episode.find('FirstAired').text
					debug("(modeEMPTY) ##### FIRST_AIRED : "+start+" #####")
					mit = time.strptime(start, "%Y-%m-%d")
					starttime = time.mktime(mit)
				except:
					starttime=0
				debug("(modeEMPTY) ##### STARTTIME : "+str(starttime)+" #####")
				debug("(modeEMPTY) ##### NOWTIME : "+str(now)+" #####")
				debug("### ---------------------------------------------------------------- ###")
				if starttime > now:
					if starttime < next:
						debug("(modeEMPTY) ##### Gefunden - 1 #####")
						next = starttime
						next_EpisodeNumber = episode.find('EpisodeNumber').text
						debug("(modeEMPTY) ##### Grösser = EpisodeNumber : "+next_EpisodeNumber+" #####")
						next_SeasonNumber = episode.find('SeasonNumber').text
						debug("(modeEMPTY) ##### Grösser = SeasonNumber : "+next_SeasonNumber+" #####")
				if starttime < now:
					if starttime > last:
						debug("(modeEMPTY) ##### Gefunden - 2 #####")
						last = starttime
						last_EpisodeNumber = episode.find('EpisodeNumber').text
						debug("(modeEMPTY) ##### Kleiner = EpisodeNumber : "+last_EpisodeNumber+" #####")
						last_SeasonNumber = episode.find('SeasonNumber').text
						debug("(modeEMPTY) ##### Kleiner = SeasonNumber : "+last_SeasonNumber+" #####")
			if next < 5000000000:
				nextde = datetime.datetime.fromtimestamp(next).strftime("%d/%m/%Y")
				if textnext !="":
					debug("(modeEMPTY) ##### LastTurn - 1 #####")
					de_next ="  Other : "+next_SeasonNumber+"X"+next_EpisodeNumber+". ( "+str(nextde)+" "+ str(dezeit)+" "+str(desender)+" )\n"
				else:
					debug("(modeEMPTY) ##### LastTurn - 2 #####")
					de_next ="Nächste Folge :\n     Other : "+next_SeasonNumber+"X"+next_EpisodeNumber+". ( "+str(nextde)+" "+str(dezeit)+" "+str(desender)+" )\n"
			if last > 0:
				debug("(modeEMPTY) ##### LastTurn - 3 #####")
				lastde = datetime.datetime.fromtimestamp(last).strftime("%d/%m/%Y")
				de_last =" - Other : "+last_SeasonNumber+"X"+last_EpisodeNumber+". ( "+str(lastde)+" "+str(dezeit)+" "+str(desender)+" )\n"
		debug("5. ++++++ SUM ++++++")
		zusatz =""
		anzahLstaffeln = int(struct_serie["number_of_seasons"])
		for season in struct_serie["seasons"]:
			seasonNAME = str(season["name"])
			if "Season" in seasonNAME:
				seasonNAME = seasonNAME.replace('Season', 'Staffel')
			zusatz = zusatz+"\n"+seasonNAME+ " : "+ str(season["episode_count"])+ " Folgen\n"
		Zusammenfassung ="Serien-Name :      "+seriesName+"\nSerien-Start :        "+serienstart +"\nAnzahl Staffeln :   "+str(anzahLstaffeln)+"\n"+statustext+u"\n"+"Letzte Folge :\n     US : "+leztefolge+" ( "+lastdatum+" )"+de_last+textnext+de_next+zusatz
		window = Infowindow(title="[B]SERIEN - INFOS[/B]", text=Zusammenfassung, image=Bild, lastplayd_title=lastplayd_title, lastepisode_name=lastepisode_name, fehlen=fehlen)
		window.doModal()
		del window
