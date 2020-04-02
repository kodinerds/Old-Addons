# -*- coding: utf-8 -*-

import simple_requests as requests
from credentials import Credentials
from common import *

class Client:

    def __init__(self):
    
        self.headers = {
            'User-Agent': 'Kodi',
            'Referer': 'http://www.laola1.tv'
        }
                            
        self.params = {}
        self.post_data = {}
        self.cookie = cookie
                            
        self.v2 = 'https://club.laola1.tv/sp/laola1tv/api/v2/'
        self.v3 ='https://club.laola1.tv/sp/laola1tv/api/v3/'
        self.feed = 'http://www.laola1.tv'
        self.web_login = 'https://club.laola1.tv/sp/laola1tv/web/login'
        
        self.partner = '22'
        self.target = '8'
        self.target_vod = '2'
        self.target_live = '17'

    def menu(self):
        return self.json_request('%s/%s-%s/apps/menu' % (self.feed, lang, portal))
        
    def feeds(self, pagetype, id, page=''):
        return self.json_request('%s/%s-%s/apps/%s/%s/%s' % (self.feed, lang, portal, pagetype, id, page))
        
    def live_feed(self):
        self.params = {
            'targetID': self.target_live,
            'order': 'asc',
            'partner': self.partner,
            'lang': lang,
            'geo': portal,
            'records': '50',
            'format': 'json'
        }
        return self.json_request('%s/feed/app_video.feed.php' % (self.feed))
            
    def player(self, id, params):
        if params == 'true':
            target = self.target_live
        else:
            target = self.target_vod
            
        self.headers.update({'cookie': self.cookie})
        
        self.post_data = {
            '0': 'tv.laola1.laolatv.premiumclub',
            '1': 'tv.laola1.laolatv.premiumclub_all_access'
        }
                            
        self.params = {
            'videoId': id,
            'label': 'laola1tv',
            'area': 'laola1tv',
            'target': target
        }
        return self.json_request(self.v3 + 'user/session/premium/player/stream-access')
            
    def unas_xml(self,id):
        r = requests.get(id + '&format=iphone', headers=self.headers)
        if r:
            return r.text
        else:
            return ''
        
    def login(self):
        credentials = Credentials()
        if credentials.email and credentials.password:
            post_data = {
                'e': utfenc(credentials.email),
                'p': utfenc(credentials.password)
            }
            r = requests.post(self.v2 + 'session', headers=self.headers, data=post_data)
            if r.headers.get('content-type', '').startswith('application/json') and not '<html>' in r.text:
                data = r.json()
                if data.get('error', None):
                    msg = data['error'][0]
                    log('[%s] login: %s' % (addon_id, msg))
                    dialog.ok(addon_name, msg)
                    self.cookie = ''
                    credentials.reset()
                elif data.get('result', None):
                    self.cookie = r.headers.get('set-cookie', '')
                    log('[%s] login: premium=%s' % (addon_id, data['result']['premium']))
                    credentials.save()
                else:
                    self.cookie = ''
                    log('[%s] login: %s' % (addon_id, 'error - reset cookie'))
            else:
                post_data_ = {
                    'email': utfenc(credentials.email),
                    'password': utfenc(credentials.password)
                }
                params_ = {'redirect': 'http://www.laola1.tv/de-de/home/'}
                r = requests.post(self.web_login, headers=self.headers, params=params_, data=post_data_, allow_redirects=False)
                self.cookie = r.headers.get('set-cookie', '')
                self.session()
                result = self.user(login_=False)
                if result:
                    credentials.save()
                else:
                    self.cookie = ''
                    credentials.reset()
        addon.setSetting('cookie', self.cookie)
        
    def logout(self):
        if self.cookie:
            self.headers['cookie'] = self.cookie
            r = requests.post(self.v2 + 'session/delete', headers=self.headers)
            
    def session(self):
        self.headers['cookie'] = self.cookie
        r = requests.get(self.v2 + 'session', headers=self.headers)
        self.cookie = r.headers.get('set-cookie', '')
        addon.setSetting('cookie', self.cookie)

    def deletesession(self):
        if self.cookie:
            self.headers['cookie'] = self.cookie
            r = requests.post(self.v3 + 'user/session/premium/delete', headers=self.headers)

    def user(self, login_=True):
        result = False
        self.headers['cookie'] = self.cookie
        data = self.json_request(self.v2 + 'user')
        if data.get('error', None):
            log('[%s] user: %s' % (addon_id, data['error'][0]))
            if login_:
                self.login()
        elif data.get('result', None):
            log('[%s] user: country=%s premium=%s' % (addon_id, data['result']['country'], data['result']['premium']))
            result = True
            if login_:
                self.session()
        else:
            log('[%s] user: %s' % (addon_id, 'error - reset cookie'))
            self.cookie = ''
            addon.setSetting('cookie', self.cookie)
        if not login_:
            return result
        
    def json_request(self, url):
        if self.post_data:
            r = requests.post(url, headers=self.headers, data=self.post_data, params=self.params)
        else:
            r = requests.get(url, headers=self.headers, params=self.params)
        if r.headers.get('content-type', '').startswith('application/json'):
            return r.json()
        else:
            log('[%s] error: json request failed with %s response' % (addon_id, str(r.status_code)))
            return {}