#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import datetime
import time
from xml.dom import minidom
import urllib
import urllib2
from socket import *
try:
    import simplejson as json
except ImportError:
    import json

class WLScraper():

    def __init__(self):

        # Items of wunschlistenmain pages

        self.channel = ''
        self.tvshowname =''
        self.tvshowstarttime = ''
        self.tvshowendtime = ''
        self.starttimestamp = ''
        self.date = ''
        self.episode = ''
        self.staffel = ''        
        self.title = ''
        self.detailURL = ''
        self.runtime = ''
        self.neueepisode = ''
        self.nameURL = ''

        # Items of Detail pages

        self.rating = ''
        self.plot = ''
        self.epiid = ''
        self.pic_path = ''
        self.firstaired = ''

        self.posterUrl = ''
        self.fanartUrl = ''
        self.genre = ''
        self.studio = ''
        self.content_rating = ''
        self.status = ''
        self.year = ''

        # Original name of TVShow

        self.orig_tvshow = ''
        self.detailpath = ''

        # FanartTV

        self.clearlogo = ''


    def scrapeserien(self, container):

        try:
            for channel in container.findAll("span", {"class" : "d3 senderlogo"}):
                channel = channel.img["title"].encode('utf-8')
                channel = channel.replace(' (Pay-TV)','').strip()
                channel = channel.replace(' (Österreich)','').strip()
                self.channel = channel.replace(' (Schweiz)','').strip()

            for details in container.findAll("span", {"class" : "sendung"}):
                self.tvshowname = details.get_text()

                _timestamps = details.a["href"]
                _tvshowstarttime = re.compile('start=(.+?)&ktermin', re.DOTALL).findall(_timestamps)[0]
                _tvshowstarttime = datetime.datetime(*(time.strptime(_tvshowstarttime, '%Y%m%dT%H%M%S')[0:6]))
                self.tvshowstarttime = _tvshowstarttime.strftime('%H:%M')

                self.date = _tvshowstarttime.strftime('%d.%m.%Y')

                _tvshowendtime = re.compile('ende=(.+?)&kid', re.DOTALL).findall(_timestamps)[0]
                _tvshowendtime = datetime.datetime(*(time.strptime(_tvshowendtime, '%Y%m%dT%H%M%S')[0:6]))
                self.starttimestamp = _tvshowstarttime

                self.tvshowendtime = _tvshowendtime.strftime('%H:%M')

                _runtime = _tvshowendtime - _tvshowstarttime
                self.runtime = _runtime.seconds/60
            for details_1 in container.findAll("span", {"class" : "sf1"}):    
                try:
                    _episode = re.compile('title="Episode">(.+?)</span>', re.DOTALL).findall(str(details_1))[0]
                    self.episode = _episode.lstrip('0')
                except IndexError:
                    _episode = ''
                    self.episode = ''
                try:
                    _staffel = re.compile('title="Staffel">(.+?)</span>', re.DOTALL).findall(str(details_1))[0]
                    self.staffel = _staffel.lstrip('0')
                except IndexError:
                    _staffel = ''
                    self.staffel = ''
            
            for hinweis in container.findAll("span", {"class" : "hinweis"}):
                self.neueepisode = hinweis.get_text()

            for titles in container.findAll("div", {"class" : "ep2"}):
                _title = titles.get_text()
                _title = _title.lstrip("%s" % _staffel)
                _title = _title.lstrip("%s" % _episode)
                _title = _title.replace("%s" % self.neueepisode, '')
                self.title = _title            
            try:
                self.nameURL = re.compile('class="entry"><a href="(.+?)" class', re.DOTALL).findall(content)[0]            
                self.detailURL = re.compile('&nbsp;<a href="(.+?)" class', re.DOTALL).findall(content)[0]
            except:
                pass


        except IndexError:
            pass

    def scrapeDetailPage(self, content, contentID):

        if contentID in content:

            container = content.split(contentID)
            container.pop(0)
            content = container[0]

            # Erstaustrahlung
            try:
                self.firstaired = re.compile('Original-Erstausstrahlung: (.+?) <em>', re.DOTALL).findall(content)[0]
            except IndexError:
                pass    

            # Episode description
            try:
                _plot = re.compile('<p class="clear mb4"></p>(.+?)<p class="credits">', re.DOTALL).findall(content)
                plot = _plot[0]
                self.plot = plot.replace('<p class="clear mb4"></p>','').strip()
            except IndexError:
                pass                

            # Ratings
            try:
                self.rating = re.compile('class="wertung">(.+?)<', re.DOTALL).findall(content)[0]
            except IndexError:
                pass

            # picture path
            try:
                self.pic_path = re.compile('class="big"><a href="(.+?)" rel="', re.DOTALL).findall(content)[0]
            except IndexError:
                pass

    def get_detail_thetvdb(self, imdbnumber, staffel, episode):
        try:
            url_str="http://thetvdb.com/api/DECE3B6B5464C552/series/"+imdbnumber+"/all/de.xml"
            xml_str = urllib.urlopen(url_str).read() 
        except timeout:
            time.sleep(3)
            url_str="http://thetvdb.com/api/DECE3B6B5464C552/series/"+imdbnumber+"/all/de.xml"
            xml_str = urllib.urlopen(url_str).read()

        try:
            xmldoc = minidom.parseString(xml_str)

            series_details = xmldoc.getElementsByTagName("Series")

            for Series in series_details:
                try:
                    posterUrl = Series.getElementsByTagName("poster")[0].firstChild.nodeValue
                    self.posterUrl = "http://thetvdb.com/banners/"+posterUrl
                except (AttributeError, IndexError):
                    pass

                try:
                    fanartUrl = Series.getElementsByTagName("fanart")[0].firstChild.nodeValue
                    self.fanartUrl = "http://thetvdb.com/banners/"+fanartUrl
                except (AttributeError, IndexError):
                    pass   

                try:
                    _genre = Series.getElementsByTagName("Genre")[0].firstChild.nodeValue
                    _genre = _genre[1:-1]
                    self.genre = _genre.replace('|',' | ').strip()
                except (AttributeError, IndexError):
                    pass

                try:
                    self.studio = Series.getElementsByTagName("Network")[0].firstChild.nodeValue
                except (AttributeError, IndexError):
                    pass

                try:
                    self.content_rating = Series.getElementsByTagName("ContentRating")[0].firstChild.nodeValue
                except (AttributeError, IndexError):
                    pass

                try:
                    self.status = Series.getElementsByTagName("Status")[0].firstChild.nodeValue
                except (AttributeError, IndexError):
                    pass

                try:
                    year = Series.getElementsByTagName("FirstAired")[0].firstChild.nodeValue
                    self.year = year[:-6]
                except (AttributeError, IndexError):
                    pass


            episodes_detail = xmldoc.getElementsByTagName("Episode")

            for Episode in episodes_detail:
                if Episode.getElementsByTagName('SeasonNumber')[0].firstChild.nodeValue == staffel and Episode.getElementsByTagName('EpisodeNumber')[0].firstChild.nodeValue == episode:  
                    try:
                        self.epiid = Episode.getElementsByTagName("id")[0].firstChild.nodeValue
                    except IndexError:
                        pass
                    try:
                        self.plot = Episode.getElementsByTagName("Overview")[0].firstChild.nodeValue
                    except:
                        pass
                    try:
                        self.rating = Episode.getElementsByTagName("Rating")[0].firstChild.nodeValue
                    except:
                        pass
                    try:
                        self.firstaired = Episode.getElementsByTagName("FirstAired")[0].firstChild.nodeValue
                    except:
                        pass
                    try:
                        self.pic_path = "http://www.thetvdb.com/banners/episodes/"+imdbnumber+"/"+self.epiid+".jpg"
                    except AttributeError:
                        self.pic_path = False

        except:
            url_str="http://tvdb.cytec.us/api/9DAF49C96CBF8DAC/series/"+imdbnumber+"/all/en.xml"
            xml_str = urllib.urlopen(url_str).read()               
            xmldoc = minidom.parseString(xml_str)
            series_details = xmldoc.getElementsByTagName("Series")
            
            for Series in series_details:
                try:
                    posterUrl = Series.getElementsByTagName("poster")[0].firstChild.nodeValue
                    self.posterUrl = "http://thetvdb.com/banners/"+posterUrl
                except (AttributeError, IndexError):
                    pass

                try:
                    fanartUrl = Series.getElementsByTagName("fanart")[0].firstChild.nodeValue
                    self.fanartUrl = "http://thetvdb.com/banners/"+fanartUrl
                except (AttributeError, IndexError):
                    pass   

                try:
                    _genre = Series.getElementsByTagName("Genre")[0].firstChild.nodeValue
                    _genre = _genre[1:-1]
                    self.genre = _genre.replace('|',' | ').strip()
                except (AttributeError, IndexError):
                    pass

                try:
                    self.studio = Series.getElementsByTagName("Network")[0].firstChild.nodeValue
                except (AttributeError, IndexError):
                    pass

                try:
                    self.content_rating = Series.getElementsByTagName("ContentRating")[0].firstChild.nodeValue
                except (AttributeError, IndexError):
                    pass

                try:
                    self.status = Series.getElementsByTagName("Status")[0].firstChild.nodeValue
                except (AttributeError, IndexError):
                    pass

                try:
                    year = Series.getElementsByTagName("FirstAired")[0].firstChild.nodeValue
                    self.year = year[:-6]
                except (AttributeError, IndexError):
                    pass


            episodes_detail = xmldoc.getElementsByTagName("Episode")

            for Episode in episodes_detail:
                if Episode.getElementsByTagName('SeasonNumber')[0].firstChild.nodeValue == staffel and Episode.getElementsByTagName('EpisodeNumber')[0].firstChild.nodeValue == episode:  
                    try:
                        self.epiid = Episode.getElementsByTagName("id")[0].firstChild.nodeValue
                    except IndexError:
                        pass
                    try:
                        self.plot = Episode.getElementsByTagName("Overview")[0].firstChild.nodeValue
                    except:
                        pass
                    try:
                        self.rating = Episode.getElementsByTagName("Rating")[0].firstChild.nodeValue
                    except:
                        pass
                    try:
                        self.firstaired = Episode.getElementsByTagName("FirstAired")[0].firstChild.nodeValue
                    except:
                        pass
                    try:
                        self.pic_path = "http://www.thetvdb.com/banners/episodes/"+imdbnumber+"/"+self.epiid+".jpg"
                    except AttributeError:
                        self.pic_path = False


    def get_original_series_name(self, content, tvshow):

        try:
            orig_tvshow = re.compile('class="otitel">(.+?)</span>', re.DOTALL).findall(content)[0]
            _orig_tvshow = orig_tvshow.replace('(','').strip()
            self.orig_tvshow = _orig_tvshow.replace(')', '').strip()
            self.orig_tvshow = self.orig_tvshow.replace('&', 'and')

        except IndexError:
            pass



    def get_scrapedetail_pcpath(self, content, contentID):

        if contentID in content:

            container = content.split(contentID)
            container.pop(0)
            content = container[0]


            # picture path
            try:
                self.pic_path = re.compile('class="big"><a href="(.+?)" rel="', re.DOTALL).findall(content)[0]
            except:
                pass            

    def get_scrapper_fernsehserien_path(self, content, tvshow, title):

        content = content.replace("\\","")

        try:
            detailpath = re.compile('%s/folgen/%s-(.+?)" onclick' % (tvshow, title), re.DOTALL).findall(content)[0]
            detailpath = detailpath.replace('(','-')
            detailpath = detailpath.replace(')','')
            self.detailpath = "http://www.fernsehserien.de/"+tvshow+"/folgen/"+title+"-"+detailpath
        except (AttributeError, IndexError):
            pass

    
    def get_details_fernseserien(self, content, tvshow, title):

        
        if 'class="episode-output-inhalt">' in content:
            container = content.split('class="episode-output-inhalt">')
            container.pop(0)
            content = container[0]
            try:
                self.plot = re.compile('<p>(.+?)<', re.DOTALL).findall(content)[0]
            except IndexError:
                pass

            try:
                self.pic_path = re.compile('src="(.+?)"', re.DOTALL).findall(content)[0]
            except IndexError:
                pass

            try:
                self.firstaired = re.compile('Erstausstrahlung: (.+?) <', re.DOTALL).findall(content)[0]
                self.firstaired = self.firstaired[-10:]
            except IndexError:
                pass


    def get_fanarttv_clearlogo(self, tvdb_id, art_type, lang = 'en'):

        API_KEY = 'd97752d8f49fede7114b010f07b3b71f'
        API_URL_TV = 'http://webservice.fanart.tv/v3/tv/%s?api_key=%s'   

        try:
            if art_type == 'clearlogo':
                find_types = [ 'hdtvlogo', 'clearlogo' ]
            else:
                find_types = [ 'tv' + str(art_type) ]
            url = API_URL_TV % (tvdb_id, API_KEY)
            data = json.load(urllib.urlopen(url))
            if not data:
                self.clearlogo = None

            ret = None
            for find in find_types:
                logos = data.get(find, [])
                for logo in logos:
                    if logo['lang'] == lang:
                        self.clearlogo = logo['url']
                    # We'll accept the wrong language as a fallback, as they are sometimes mislabeled.
                    if not self.clearlogo:
                        self.clearlogo = logo['url']
        except:
            pass                               