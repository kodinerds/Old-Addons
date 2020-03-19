# -*- coding: utf-8 -*-
import os
import sys
import requests
import time
import xbmcvfs

class EweTv():
    def __init__(self, username, password):
        self.app_id = 'HJ8n59WO0Jcmr9l0U0FLXYlXaQOyzn'
        self.session = requests.Session()
        self.session.headers["User-Agent"] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36'
        self.username = username
        self.password = password
        self.valid_until = str(time.time()).replace('.', '')
        self.current_channel_id = ''

    def login(self):
        url = 'https://tvonline.ewe.de/external/client/core/Login.do'
        headers = self.session.headers
        headers["Content-Type"] = "application/x-www-form-urlencoded"
        payload = {'appId': self.app_id, 'userId': self.username, 'password': self.password}
        r = self.session.post(url, data=payload, headers=headers)
        print r.text
        if 'errors' in r.json():
            return False

        return True       

    def getChannelUrl(self):
        channels = self.getChannelList()
        for c in channels:
            if c['vodkatvChannelId'] == self.current_channel_id:
                return c['url']

        return ''

    def getChannelList(self):
        url = 'https://tvonline.ewe.de/external/client/plugins/television/FindChannels.do'
        headers = self.session.headers
        r = self.session.get(url, headers=headers)
        data = r.json()
        if 'errors' in data:
            if data['errors'][0]['code'] == 'access_denied':
                if self.login():
                    self.getChannelList()
        else:
            return r.json()['channels']['elements']

    def generateM3U(self, path, host, port):
        channels = self.getChannelList()
        m3u_lines = []
        has_changed = False

        if xbmcvfs.exists(path):
            f = xbmcvfs.File(path, 'r')
            m3u_lines = f.read().split('\n')
            f.close()            

        for c in channels:
            line = ('#EXTINF:-1 tvg-id=%s.de tvg-logo=%s.de tvg-name=%s, %s' % (c['name'].replace(' ', ''), c['name'].replace(' ', ''), c['name'].replace(' ', '_'), c['name'])).encode('utf8')
            line2 = ('http://' + host + ':' + str(port) + '/channel.m3u8?channel_id=' + c['vodkatvChannelId']).encode('utf8')
            if not line in m3u_lines and not line2 in m3u_lines:
                m3u_lines.append(line)
                m3u_lines.append(line2)
                has_changed = True

        if has_changed:
            f = xbmcvfs.File(path, 'w+')
            if not m3u_lines[0].startswith('#EXTM3U'):
                f.write('#EXTM3U\n')
            for item in m3u_lines:
                if not item == '':
                    f.write(item + '\n')
            f.close()

        del m3u_lines[:]
        return has_changed
    
