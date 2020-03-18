#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import xbmc
import xbmcaddon
PY2 = sys.version_info[0] == 2
if PY2:
	reload(sys)
	sys.setdefaultencoding('utf8')
import md5
from django.utils.encoding import smart_str

displayADDON    = xbmcaddon.Addon("service.popwindow")
displayA_Profile = xbmc.translatePath(displayADDON.getAddonInfo('profile')).encode('utf-8').decode('utf-8')
displayA_Temp   = xbmc.translatePath(os.path.join(displayA_Profile, 'temp', '')).encode('utf-8').decode('utf-8')

def py2_enc(s, encoding='utf-8'):
	if PY2 and isinstance(s, unicode):
		s = s.encode(encoding)
	return s

def py2_uni(s, encoding='utf-8'):
	if PY2 and isinstance(s, str):
		s = unicode(s, encoding)
	return s

def debug(content):
	log(content, xbmc.LOGDEBUG)

def failing(content):
	log(content, xbmc.LOGERROR)

def log(msg, level=xbmc.LOGNOTICE):
	msg = py2_enc(msg)
	xbmc.log("["+displayADDON.getAddonInfo('id')+"-"+displayADDON.getAddonInfo('version')+"]"+msg, level)

def saveMESSAGE(addon,message,image1,grey,lesezeit,xmessage,ymessage,breitemessage,hoehemessage,breitebild1=0,hoehebild1=0,fontname="font14",fontcolor="FFFFFFFF",startxbild1=-1,startybild1=-1,image2="",startxbild2=-1,startybild2=-1,breitebild2=0,hoehebild2=0):
	incomingA_Name = addon.getAddonInfo('name').replace(' ', '-')
	message = smart_str(message)
	debug("(saveMESSAGE) ##### Message : {0} #####".format(message))
	debug("(saveMESSAGE) ##### Image1 : {0} #####".format(image1))
	debug("(saveMESSAGE) ##### Image2 : {0} #####".format(image2))
	debug("(saveMESSAGE) ##### grey : {0} #####".format(grey))
	debug("(saveMESSAGE) ##### displayA_Temp : {0} #####".format(displayA_Temp))
	debug("(saveMESSAGE) ##### Lesezeit : {0} #####".format(str(lesezeit)))
	filename = incomingA_Name+ "_"+md5.new(message).hexdigest()
	debug("(saveMESSAGE) ##### Filename : {0} #####".format(str(filename)))
	with open(os.path.join(displayA_Temp, filename), 'w') as input:
		input.write(message+"###"+image1+"###"+grey+"###"+str(lesezeit)+"###"+str(xmessage)+"###"+str(ymessage)+"###"+ str(breitemessage)+"###"+str(hoehemessage)+"###"+str(startxbild1)+"###"+str(startybild1)+ "###"+str(breitebild1)+"###"+str(hoehebild1)+"###"+image2+"###"+str(startxbild2)+"###"+str(startybild2)+ "###"+str(breitebild2)+"###"+str(hoehebild2)+"###"+ str(fontname)+"###"+fontcolor)

def deleteMESSAGE(addon):
	incomingA_Name = addon.getAddonInfo('name').replace(' ', '-')
	filename = "DELETE_"+incomingA_Name 
	with open(os.path.join(displayA_Temp, filename), 'w') as input:
		input.write("DELETE")
