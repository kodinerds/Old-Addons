#!/usr/bin/python

import re

class TVDScraper():

    def __init__(self):

        # Items of highlights pages

        self.channel = ''
        self.title = ''
        self.thumb = ''
        self.detailURL = ''
        self.starttime = ''
        self.runtime = '0'
        self.genre = ''
        self.extrainfos = ''
        self.outline = ''

        # Items of detail pages

        self.endtime = ''
        self.ratingValue = '-'
        self.bestRating = '-'
        self.plot = ''
        self.keywords = ''
        self.ratingdata = [{'ratingtype': 'Spannung', 'rating': '-'},
                           {'ratingtype': 'Action',  'rating': '-'},
                           {'ratingtype': 'Humor', 'rating': '-'},
                           {'ratingtype': 'Romantik', 'rating': '-'},
                           {'ratingtype': 'Sex', 'rating': '-'}]
        self.broadcastflags = ''

    def scrapeHighlights(self, content):

        try:
            self.channel = re.compile('/programm/" title="(.+?) Programm"', re.DOTALL).findall(content)[0]
            self.thumb = re.compile('src="(.+?)"', re.DOTALL).findall(content)[0]
            _info = re.compile('<a class="highlight-title(.+?)<h2>', re.DOTALL).findall(content)[0]
            self.detailURL = re.compile('href="(.+?)"', re.DOTALL).findall(_info)[0]

            self.title = re.compile('<h2><span>(.+?)</span></h2>', re.DOTALL).findall(content)[0].strip()
        except IndexError:
            if not self.title:
                try:
                    self.title = re.compile('<h2 class="highlight-title">(.+?)</h2>', re.DOTALL).findall(content)[0]
                except IndexError:
                    pass

        try:
            self.extrainfos = re.compile('<strong>(.+?)</strong>', re.DOTALL).findall(content)[0]
            self.genre = self.extrainfos.split('|')[0].strip()
            self.runtime = re.match('\d+', self.extrainfos.split('|')[-1].strip()).group()
        except IndexError:
            pass

        try:
            self.date = re.compile('highlight-date">(.+?) | </div>', re.DOTALL).findall(content)[0]
            self.starttime = re.compile('highlight-time">(.+?)</div>', re.DOTALL).findall(content)[0]
        except IndexError:
            pass

        try:
            self.outline = re.compile('<strong>(.+?)</strong>', re.DOTALL).findall(content)[1]
        except IndexError:
            pass

    def scrapeDetailPage(self, content, contentID):

        if contentID in content:

            container = content.split(contentID)
            container.pop(0)
            content = container[0]

            try:
                # Broadcast info (channel, start, stop)
                '''
                bd = re.compile('<li id="broadcast-title" itemprop="name">(.+?)<li id="broadcast-genre', re.DOTALL).findall(content)[0]
                bd = re.compile('<li>(.+?)</li>', re.DOTALL).findall(bd)[0]
                bd = re.sub(re.compile('<.*?>', re.DOTALL), '', bd)

                _t = bd.split('|')[2]
                self.endtime = _t.split('-')[1].strip()
                '''
                bd = re.compile('<div class="broadcast-time">(.+?)</div>', re.DOTALL).findall(content)[0]
                self.endtime = bd.split('-')[1].strip()
            except IndexError:
                pass

            # Ratings
            try:
                self.ratingValue = re.compile('<span itemprop="ratingValue">(.+?)</span>', re.DOTALL).findall(content)[0]
            except IndexError:
                pass

            # best Ratings
            try:
                self.bestRating = re.compile('<span itemprop="bestRating">(.+?)</span>', re.DOTALL).findall(content)[0]
            except IndexError:
                pass

            # Movie description
            try:
                self.plot = re.compile('<div class="description">(.+?)</div>', re.DOTALL).findall(content)[0]
                self.plot = re.compile('<p>(.+?)</p>', re.DOTALL).findall(content)[0]
            except IndexError:
                pass

            # Keywords
            try:
                _keywords = re.compile('<ul class="genre-list">(.+?)</ul>', re.DOTALL).findall(content)[0]
                self.keywords = ', '.join(re.compile('itemprop="genre">(.+?)</a>', re.DOTALL).findall(_keywords))
            except IndexError:
                pass

            # Rating details
            try:
                ratingbox = re.compile('<ul class="rating-genre"(.+?)</ul>', re.DOTALL).findall(content)[0].split('<li>')
                ratingbox.pop(0)
                for rating in ratingbox:
                    for item in self.ratingdata:
                        if item['ratingtype'] == rating.split('span')[0][:-1]:
                            item['rating'] = re.compile('class="rating-(.+?)">', re.DOTALL).findall(rating)
            except IndexError:
                pass

            # Broadcast Flags
            try:
                bc_info = re.compile('<div class="broadcast-feature">(.+?)</div>', re.DOTALL).findall(content)[0]
                self.broadcastflags = ', '.join(re.compile('<span class="(.+?)"></span>', re.DOTALL).findall(bc_info))
            except IndexError:
                pass
