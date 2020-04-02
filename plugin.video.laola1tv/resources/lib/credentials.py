# -*- coding: utf-8 -*-

from common import *
import base64,pyDes

class Credentials:

    def __init__(self):
        self.email = addon.getSetting('email')
        self.password = addon.getSetting('password')
        self.credentials = False
        self.run()

    def encode(self, data):
        k = pyDes.triple_des(uniq_id(t=2), pyDes.CBC, "\0\0\0\0\0\0\0\0", padmode=pyDes.PAD_PKCS5)
        d = k.encrypt(data)
        return base64.b64encode(d)

    def decode(self, data):
        k = pyDes.triple_des(uniq_id(t=2), pyDes.CBC, "\0\0\0\0\0\0\0\0", padmode=pyDes.PAD_PKCS5)
        d = k.decrypt(base64.b64decode(data))
        return d

    def run(self):
        if self.email and self.password:
            self.email = self.decode(self.email)
            self.password = self.decode(self.password)
            self.credentials = True
        else:
            self.email = dialog.input(getString(30002), type=xbmcgui.INPUT_ALPHANUM)
            if self.email:
                self.password = dialog.input(getString(30003), type=xbmcgui.INPUT_ALPHANUM, option=xbmcgui.ALPHANUM_HIDE_INPUT)

    def save(self):
        if not self.credentials:
            addon.setSetting('email', self.encode(self.email))
            addon.setSetting('password', self.encode(self.password))
            
    def reset(self):
        addon.setSetting('email', '')
        addon.setSetting('password', '')