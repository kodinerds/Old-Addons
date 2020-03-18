#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import xbmc
import xbmcgui
import xbmcaddon
PY2 = sys.version_info[0] == 2
if PY2:
	reload(sys)
	sys.setdefaultencoding('utf8')
import xbmcvfs
import shutil
import time
from datetime import datetime

displayADDON   = xbmcaddon.Addon()
displayA_Name  = displayADDON.getAddonInfo('name')
displayA_Path    = xbmc.translatePath(displayADDON.getAddonInfo('path')).encode('utf-8').decode('utf-8')
displayA_Profile = xbmc.translatePath(displayADDON.getAddonInfo('profile')).encode('utf-8').decode('utf-8')
displayA_Temp   = xbmc.translatePath(os.path.join(displayA_Profile, 'temp', '')).encode('utf-8').decode('utf-8')
background = os.path.join(displayA_Path, "bg.png")

#wid = xbmcgui.getCurrentWindowId()
#window=xbmcgui.Window(wid)
#window.show()

wait_time = 160  # 180 seconds = 3 minutes - wait at KODI start
#loop_time = 60  # 60 seconds = 1 minute - time when the process started again

if not xbmcvfs.exists(displayA_Temp):
	xbmcvfs.mkdirs(displayA_Temp)

def py2_enc(s, encoding='utf-8'):
	if PY2 and isinstance(s, unicode):
		s = s.encode(encoding)
	return s

def py2_uni(s, encoding='utf-8'):
	if PY2 and isinstance(s, str):
		s = unicode(s, encoding)
	return s

def translation(id):
	LANGUAGE = displayADDON.getLocalizedString(id)
	LANGUAGE = py2_enc(LANGUAGE)
	return LANGUAGE

def special(msg, level=xbmc.LOGNOTICE):
	xbmc.log(msg, level)

def debug(content):
	log(content, xbmc.LOGDEBUG)

def failing(content):
	log(content, xbmc.LOGERROR)

def log(msg, level=xbmc.LOGNOTICE):
	msg = py2_enc(msg)
	xbmc.log("["+displayADDON.getAddonInfo('id')+"-"+displayADDON.getAddonInfo('version')+"]"+msg, level)

def showMESSAGE(Message,image1="",image2="",greyout="true",lesezeit=10,xmessage=110,ymessage=5,breitemessage=1170,hoehemessage=100,startxbild1=-1,startybild1=-1,breitebild1=100,hoehebild1=100,startxbild2=-1,startybild2=-1,breitebild2=100,hoehebild2=100,fontname="font14",fontcolor="FFFFFFFF"):
	global background
	global window
	debug("(showMESSAGE) ##### Image1 : {0} #####".format(image1))
	debug("(showMESSAGE) ##### Image2 : {0} #####".format(image2))
	if int(startxbild1)==-1:
		startxbild1=int(xmessage)
	if int(startybild1)==-1:
		startybild1=int(ymessage)
	if int(startxbild2)==-1:
		startxbild2=int(breitemessage)-int(breitebild2)
	if int(startybild2)==-1:
		startybild2=int(ymessage)
	Message=Message.replace("&amp;", "&")
	fontcolor='0x'+fontcolor
	debug("(showMESSAGE) Gestartet")
	wid = xbmcgui.getCurrentWindowId()
	window=xbmcgui.Window(wid)
	res=window.getResolution()
	if greyout=="true":
		bg=xbmcgui.ControlImage(0,int(ymessage),10000,int(hoehemessage),"")
		bg.setImage(background)
		window.addControl(bg)
	debug("(showMESSAGE) ##### X : {0} #####".format(str(xmessage)))
	debug("(showMESSAGE) ##### Y : {0} #####".format(str(ymessage)))
	debug("(showMESSAGE) ##### Breite : {0} #####".format(str(breitemessage)))
	debug("(showMESSAGE) ##### Höhe : {0} #####".format(str(hoehemessage)))
	debug("(showMESSAGE) ##### Breite Bild1 : {0} #####".format(str(breitebild1)))
	debug("(showMESSAGE) ##### Höhe Bild1 : {0} #####".format(str(hoehebild1)))
	debug("(showMESSAGE) ##### Breite Bild2 : {0} #####".format(str(breitebild2)))
	debug("(showMESSAGE) ##### Höhe Bild2 : {0} #####".format(str(hoehebild2)))
	debug("(showMESSAGE) ##### Message : {0} #####".format(Message))
	debug("(showMESSAGE) ##### Schriftart : {0} #####".format(fontname))### int(xmessage)+int(breitebild1)+10 =+10 damit die Message sich nicht mit dem Bild LINKS berührt ############
	debug("(showMESSAGE) ##### Schriftfarbe : {0} #####".format(fontcolor))###################################### (int(xmessage)+int(breitebild1)+int(breitebild2)+20) =+20 damit die Message sich nicht mit dem Bild RECHTS berührt ############
	report1=xbmcgui.ControlTextBox(int(xmessage)+int(breitebild1)+10, int(ymessage)+5, int(breitemessage) - (int(xmessage)+int(breitebild1)+int(breitebild2)+20), int(hoehemessage), font=fontname, textColor=fontcolor)
	window.addControl(report1)
	report1.setText(Message)
	avatar1=xbmcgui.ControlImage(int(startxbild1), int(startybild1), int(breitebild1), int(hoehebild1), "")
	avatar1.setImage(image1)
	avatar2=xbmcgui.ControlImage(int(startxbild2), int(startybild2), int(breitebild2), int(hoehebild2), "")
	avatar2.setImage(image2)
	window.addControl(avatar1)
	window.addControl(avatar2)
	debug("(showMESSAGE) ##### Lesezeit : {0} #####".format(str(lesezeit)))
	time.sleep(int(lesezeit))
	window.removeControl(report1)
	window.removeControl(avatar1)
	window.removeControl(avatar2)
	if greyout=="true":
		window.removeControl(bg)

if __name__ == '__main__':
	time.sleep(20)
	special("##########################################################################################")
	special("########## RUNNING: "+displayADDON.getAddonInfo('id')+" PLUGIN VERSION "+displayADDON.getAddonInfo('version')+" / ON PLATFORM: "+sys.platform+" #############")
	special("################## Start the Service in 3 minutes - wait for other Instances to close ###################")
	special("##########################################################################################")
	time.sleep(wait_time)
	log("########## START DISPLAY-WINDOWS ##########")
	MAX_ERRORS = 30
	errors = 0
	monitor = xbmc.Monitor()
	while not monitor.abortRequested():
		#log("########## START LOOP ... ##########")
		try:
			starting=datetime.now()
			text=[]
			image=[]
			greyout=[]
			fileliste=[]
			datumliste=[]
			dirs, files = xbmcvfs.listdir(displayA_Temp)
			delete=0
			deletefile=""
			module=""
			for name in files:  
				pf=os.path.join(displayA_Temp, name)
				zeit=os.path.getctime(pf)
				fileliste.append(name)
				if "DELETE" in name:
					delete=1
					deletefile=name
					teile=deletefile.split("_")
					module=teile[1]
				datumliste.append(zeit)
			if len(datumliste) > 0:
				datumliste,fileliste = (list(x) for x in zip(*sorted(zip(datumliste,fileliste))))
				if delete==1:
					ende=0
					x=0
					for file in fileliste:
						if module in file  and ende==0:
							fileliste.pop(x)
							datumliste.pop(x)
							xbmcvfs.delete(os.path.join(displayA_Temp, file))
							debug("(MAIN) ##### Delete File {0} #####".format(file))
							if "DELETE" in file:
								ende=1
								debug("(MAIN) Delete END")
							x +=1
				count=0
				for name in fileliste:
					if count > 4:
						break
					count +=1
					debug("(MAIN) ##### File: {0} #####".format(name))
					debug("(MAIN) Hole Umgebung-1")
					with open(os.path.join(displayA_Temp, name), 'r') as output:
						infos = output.readlines()
					for line in infos:
						message,image1,grey,lesezeit,xmessage,ymessage,breitemessage,hoehemessage,startxbild1,startybild1,breitebild1,hoehebild1,image2,startxbild2,startybild2,breitebild2,hoehebild2,fontname,fontcolor=line.split("###")    
						message=message.replace("#n#", "\n")
						showMESSAGE(message,image1=image1,image2=image2,greyout=grey,lesezeit=lesezeit,xmessage=xmessage,ymessage=ymessage,breitemessage=breitemessage,hoehemessage=hoehemessage,startxbild1=startxbild1,startybild1=startybild1,breitebild1=breitebild1,hoehebild1=hoehebild1,startxbild2=startxbild2,startybild2=startybild2,breitebild2=breitebild2,hoehebild2=hoehebild2,fontname=fontname,fontcolor=fontcolor)
					xbmcvfs.delete(os.path.join(displayA_Temp, name))
			debug("(MAIN) Hole Umgebung-2")
			ending=datetime.now()
			delta=ending-starting
			debug("(MAIN) ######  Warten-1 : {0} #####".format(str(delta.total_seconds())))
			waiting=20-delta.total_seconds()
			if waiting < 2:
				waiting=2
			debug("(MAIN) ######  Warten-2 : {0} #####".format(str(waiting)))
		except Exception as e:
			failure = str(e)
			errors += 1
			if errors >= MAX_ERRORS:
				failing("ERROR - ERROR - ERROR : ########## ({0}) received... (Number: {1}/{2}) ...Ending Service ##########".format(failure, errors, MAX_ERRORS))
				break
			else:
				failing("ERROR - ERROR - ERROR : ########## ({0}) received... (Number: {1}/{2}) ...Continuing Service ##########".format(failure, errors, MAX_ERRORS))
		else:
			errors = 0
		#log("########## ... END LOOP ##########")
		if monitor.waitForAbort(waiting):
			break
