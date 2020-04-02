# -*- coding: utf-8 -*-

import xbmc
import xbmcaddon
import subprocess
import sys
import os
import xbmcgui
import subprocess, platform
import pyxbmct
from resources.lib.common import Ping,wake,Note


__addon__               = xbmcaddon.Addon()
__addon_id__            = __addon__.getAddonInfo('id')
__addonname__           = __addon__.getAddonInfo('name')
__icon__                = __addon__.getAddonInfo('icon')
__addonpath__           = xbmc.translatePath(__addon__.getAddonInfo('path')).decode('utf-8')
__settings__            = xbmcaddon.Addon(id="script.skinhelper.ping")
WINDOW = xbmcgui.Window(10000)

class MyAddon:
           
    def Server(self):
         servercount=0
         serveron=0
         serveroff=0
         host1 = __settings__.getSetting("ip1")
         host2 = __settings__.getSetting("ip2")
         host3 = __settings__.getSetting("ip3")
         host4 = __settings__.getSetting("ip4")
         host5 = __settings__.getSetting("ip5")
         
         try:
            if host1 <> "":
               servercount+=1
               if Ping(host1,"SkinHelperPING.server1","on","off") == True:
                 serveron+=1
            if host2 <> "":
               servercount+=1
               if Ping(host2,"SkinHelperPING.server2","on","off") == True:
                 serveron+=1
            if host3 <> "":
               servercount+=1
               if Ping(host3,"SkinHelperPING.server3","on","off") == True:
                 serveron+=1
            if host4 <> "":
               servercount+=1
               if Ping(host4,"SkinHelperPING.server4","on","off") == True:
                 serveron+=1
            if host5 <> "":
               servercount+=1
               if Ping(host5,"SkinHelperPING.server5","on","off") == True:
                 serveron+=1
            
            WINDOW.setProperty("SkinHelperPING.servercount",str(servercount))
            WINDOW.setProperty("SkinHelperPING.serveron",str(serveron))
            WINDOW.setProperty("SkinHelperPING.serveroff",str(servercount - serveron))
            
            WINDOW.setProperty("SkinHelperPING.mac1",str(__settings__.getSetting("mac1")))
            WINDOW.setProperty("SkinHelperPING.mac2",str(__settings__.getSetting("mac2")))
            WINDOW.setProperty("SkinHelperPING.mac3",str(__settings__.getSetting("mac3")))
            WINDOW.setProperty("SkinHelperPING.mac4",str(__settings__.getSetting("mac4")))
            WINDOW.setProperty("SkinHelperPING.mac5",str(__settings__.getSetting("mac5")))
            WINDOW.setProperty("SkinHelperPING.ip1",str(__settings__.getSetting("ip1")))
            WINDOW.setProperty("SkinHelperPING.ip2",str(__settings__.getSetting("ip2")))
            WINDOW.setProperty("SkinHelperPING.ip3",str(__settings__.getSetting("ip3")))
            WINDOW.setProperty("SkinHelperPING.ip4",str(__settings__.getSetting("ip4")))
            WINDOW.setProperty("SkinHelperPING.ip5",str(__settings__.getSetting("ip5")))
            WINDOW.setProperty("SkinHelperPING.servername1",str(__settings__.getSetting("name1")))
            WINDOW.setProperty("SkinHelperPING.servername2",str(__settings__.getSetting("name2")))
            WINDOW.setProperty("SkinHelperPING.servername3",str(__settings__.getSetting("name3")))
            WINDOW.setProperty("SkinHelperPING.servername4",str(__settings__.getSetting("name4")))
            WINDOW.setProperty("SkinHelperPING.servername5",str(__settings__.getSetting("name5")))


         except Exception as msg:
             xbmc.log("PING Helper:" + str(msg) , level=xbmc.LOGNOTICE)
             
    def __init__(self):
         self.Server()

class WOL():

     def __init__(self, action=''):
         host1 = __settings__.getSetting("mac1")
         host2 = __settings__.getSetting("mac2")
         host3 = __settings__.getSetting("mac3")
         host4 = __settings__.getSetting("mac4")
         host5 = __settings__.getSetting("mac5")
         
         try:
          if action == "wol1":
            if host1 <> "":
               wake(host1)
               xbmc.log("PING Helper: Wake host with MAC:" + str(host1) , level=xbmc.LOGNOTICE) 
          elif action == "wol2":
            if host2 <> "":
               wake(host2)
               xbmc.log("PING Helper: Wake host with MAC:" + str(host2) , level=xbmc.LOGNOTICE) 
          elif action == "wol3":
            if host3 <> "":
               wake(host3)
               xbmc.log("PING Helper: Wake host with MAC:" + str(host3) , level=xbmc.LOGNOTICE) 
          elif action == "wol4":
            if host4 <> "":
               wake(host4)
               xbmc.log("PING Helper: Wake host with MAC:" + str(host4) , level=xbmc.LOGNOTICE) 
          elif action == "wol5":
            if host5 <> "":
               wake(host5)
               xbmc.log("PING Helper: Wake host with MAC:" + str(host5) , level=xbmc.LOGNOTICE) 
            
         except Exception as msg:
             xbmc.log("PING Helper:" + str(msg) , level=xbmc.LOGNOTICE) 
       

class WakeMenu(pyxbmct.AddonDialogWindow):
 
     status1 = False
     status2 = False
     status3 = False
     status4 = False
     status5 = False
     
     
     def setAnimation(self, control):
        control.setAnimations([('WindowOpen', 'effect=fade start=0 end=100 time=2000',),
                                ('WindowClose', 'effect=fade start=100 end=0 time=2000',)])
     def __init__(self):
        super(WakeMenu, self).__init__("Wake Server")
        self.setGeometry(400, 300, 6, 1)

        self.radiobutton1 = pyxbmct.RadioButton(__settings__.getSetting("name1"))
        self.placeControl(self.radiobutton1, 0,0)
        self.radiobutton2 = pyxbmct.RadioButton(__settings__.getSetting("name2"))
        self.placeControl(self.radiobutton2, 1,0)
        self.radiobutton3 = pyxbmct.RadioButton(__settings__.getSetting("name3"))
        self.placeControl(self.radiobutton3, 2,0)
        self.radiobutton4 = pyxbmct.RadioButton(__settings__.getSetting("name4"))
        self.placeControl(self.radiobutton4, 3,0)
        self.radiobutton5 = pyxbmct.RadioButton(__settings__.getSetting("name5"))
        self.placeControl(self.radiobutton5, 4,0)
        self.button = pyxbmct.Button('Close')
        self.placeControl(self.button, 5, 0)
        
        
        self.radiobutton1.controlDown(self.radiobutton2)
        self.radiobutton1.controlUp(self.button)
     
        self.radiobutton2.controlUp(self.radiobutton1)
        self.radiobutton2.controlDown(self.radiobutton3)
     
        self.radiobutton3.controlUp(self.radiobutton2)
        self.radiobutton3.controlDown(self.radiobutton4)
     
        self.radiobutton4.controlUp(self.radiobutton3)
        self.radiobutton4.controlDown(self.radiobutton5)
     
        self.radiobutton5.controlUp(self.radiobutton4)
        self.radiobutton5.controlDown(self.button)
        
        self.button.controlUp(self.radiobutton5)
        self.button.controlDown(self.radiobutton1)
        
        self.connect(self.radiobutton1, self.radio_update1)        
        self.connect(self.radiobutton2, self.radio_update2)
        self.connect(self.radiobutton3, self.radio_update3)
        self.connect(self.radiobutton4, self.radio_update4)
        self.connect(self.radiobutton5, self.radio_update5)
        self.connect(self.button,self.close)
        
        self.connect(pyxbmct.ACTION_NAV_BACK, self.close)
        self.setFocus(self.radiobutton1)
        
        host1 = __settings__.getSetting("ip1")
        host2 = __settings__.getSetting("ip2")
        host3 = __settings__.getSetting("ip3")
        host4 = __settings__.getSetting("ip4")
        host5 = __settings__.getSetting("ip5")
         
        try:
            if host1 <> "":
               if Ping(host1,"SkinHelperPING.server1","on","off") == True:
                 self.status1 = True
                 self.radiobutton1.setSelected(True)
            if host2 <> "":
               if Ping(host2,"SkinHelperPING.server2","on","off") == True:
                 self.status2 = True
                 self.radiobutton2.setSelected(True)
            if host3 <> "":
               if Ping(host3,"SkinHelperPING.server3","on","off") == True:
                 self.status3 = True
                 self.radiobutton3.setSelected(True)
            if host4 <> "":
               if Ping(host4,"SkinHelperPING.server4","on","off") == True:
                 self.status4 = True
                 self.radiobutton4.setSelected(True)
            if host5 <> "":
               if Ping(host5,"SkinHelperPING.server5","on","off") == True:
                 self.status5 = True
                 self.radiobutton1.setSelected(True)
        except Exception as msg:
             xbmc.log("PING Helper:" + str(msg) , level=xbmc.LOGNOTICE) 
             

     def radio_update1(self):
         host1 = __settings__.getSetting("mac1")
         self.radiobutton1.setSelected(self.status1)
         if host1 <> "":
            wake(host1)
            xbmc.log("PING Helper: Wake host with MAC:" + str(host1) , level=xbmc.LOGNOTICE)
            Note("name1")
                          
     def radio_update2(self):
         host2 = __settings__.getSetting("mac2")
         self.radiobutton2.setSelected(self.status2)
         if host2 <> "":
            wake(host2)
            xbmc.log("PING Helper: Wake host with MAC:" + str(host2) , level=xbmc.LOGNOTICE) 
            Note("name2")
                          
     def radio_update3(self):        
         host3 = __settings__.getSetting("mac3")
         self.radiobutton3.setSelected(self.status3)
         if host3 <> "":
            wake(host3)
            xbmc.log("PING Helper: Wake host with MAC:" + str(host3) , level=xbmc.LOGNOTICE) 
            Note("name3")
                 
     def radio_update4(self):
         host4 = __settings__.getSetting("mac4")
         self.radiobutton4.setSelected(self.status4)
         if host4 <> "":
            wake(host4)
            xbmc.log("PING Helper: Wake host with MAC:" + str(host4) , level=xbmc.LOGNOTICE) 
            Note("name4")
                 
     def radio_update5(self):
         host5 = __settings__.getSetting("mac5")
         self.radiobutton5.setSelected(self.status5)
         if host5 <> "":
            wake(host5)
            xbmc.log("PING Helper: Wake host with MAC:" + str(host5) , level=xbmc.LOGNOTICE) 
            Note("name5")

if __name__ == '__main__':
    try:
        para = sys.argv[1]
        action = para[0:3]
        if action == "wol":
            xbmc.log("PING Helper script: WOL", level=xbmc.LOGNOTICE)
            WOL(para)
        elif action == "men":
            xbmc.log("PING Helper script: WOLMENU", level=xbmc.LOGNOTICE)
            window = WakeMenu()
            window.doModal()
            del window
    except IndexError:
        xbmc.log("PING Helper script: start", level=xbmc.LOGNOTICE)
        MyAddon()
        xbmc.log("PING Helper script: stop", level=xbmc.LOGNOTICE)
