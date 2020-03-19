import xbmcaddon
import urllib2
import xbmc
import xbmcgui
 
addon       = xbmcaddon.Addon()
addonname   = addon.getAddonInfo('name')

message = urllib2.quote(addon.getSetting('message'))
messagewheninput = urllib2.quote(addon.getSetting('messagewheninput'))
splitter = urllib2.quote(addon.getSetting('splitter'))
devicekey = addon.getSetting('key')
localnet = addon.getSetting('localnet')
localip = addon.getSetting('ipaddress')
localport = addon.getSetting('localport')
timetolive = addon.getSetting('ttl')
password = urllib2.quote(addon.getSetting('password'))
group = urllib2.quote(addon.getSetting('group'))
target = urllib2.quote(addon.getSetting('target'))
sender = urllib2.quote(addon.getSetting('sender'))

list = ['Default Message: ' + message, 'Message plus User Input: ' + messagewheninput + ' + Splitter + Input']
dialog = xbmcgui.Dialog()
choice = dialog.select('Action', list)

if choice != -1:
	if choice == 1:
		userinput = dialog.input('Input', str(''), type=xbmcgui.INPUT_ALPHANUM)
		message = messagewheninput


	if localnet == 'true':
		receiver = 'http://' + localip + ':' + localport + '/' + '?message='
	elif localnet == 'false':
		receiver = 'https://autoremotejoaomgcd.appspot.com/sendmessage?key=' + devicekey + '&message='

	if choice == 0:	
		req = receiver + message + '&ttl=' + timetolive + '&password=' + password + '&collapseKey=' + group + '&target=' + target + '&sender=' + sender
		
	if choice == 1:
		req = receiver + message + splitter + userinput + '&ttl=' + timetolive + '&password=' + password + '&collapseKey=' + group + '&target=' + target + '&sender=' + sender
	 
	xbmc.executebuiltin('Notification(%s, sending message ..., 1500)'%(addonname))
	urllib2.urlopen(req)
