# -*- coding: utf-8 -*-
import os
import sys
import urllib
import xbmc
import xbmcaddon
import xbmcgui, xbmcplugin
import xbmcvfs
import re, shutil, requests, cgi
from bs4 import BeautifulSoup

# Globals
addon = xbmcaddon.Addon()
addon_handle = int(sys.argv[1])
translation = addon.getLocalizedString
addonPath = xbmc.translatePath(addon.getAddonInfo('profile')).decode("utf-8")
tempPath = xbmc.translatePath(os.path.join(addonPath, 'tempPath', '')).decode("utf-8")
extractSubtitleDirectory = xbmc.translatePath(os.path.join(tempPath, 'subs', '')).decode("utf-8")
subtitleDownloadDirectory = xbmc.translatePath(os.path.join(tempPath, 'download', '')).decode("utf-8")
mainUrl = "https://www.subcentral.de"
#
video = {}
video['year'] = xbmc.getInfoLabel("VideoPlayer.Year")  # Year
video['season'] = str(xbmc.getInfoLabel("VideoPlayer.Season"))  # Season
video['episode'] = str(xbmc.getInfoLabel("VideoPlayer.Episode"))  # Episode
video['tvshow'] = xbmc.getInfoLabel("VideoPlayer.TVshowtitle")  # Show
video['title'] = xbmc.getInfoLabel("VideoPlayer.OriginalTitle")  # try to get original title
video['file_original_path'] = xbmc.Player().getPlayingFile().decode('utf-8')  # Full path of a playing file


def createAndResetDirectories():
    if xbmcvfs.exists(extractSubtitleDirectory):
        shutil.rmtree(extractSubtitleDirectory)
    xbmcvfs.mkdirs(extractSubtitleDirectory)
    if xbmcvfs.exists(subtitleDownloadDirectory):
        shutil.rmtree(subtitleDownloadDirectory)
    xbmcvfs.mkdirs(subtitleDownloadDirectory)
    if xbmcvfs.exists(tempPath):
        shutil.rmtree(tempPath)
    xbmcvfs.mkdirs(tempPath)
    xbmcvfs.mkdirs(extractSubtitleDirectory)
    xbmcvfs.mkdirs(subtitleDownloadDirectory)


def debug(content):
    log(content, xbmc.LOGDEBUG)


def notice(content):
    log(content, xbmc.LOGNOTICE)

def log(msg, level=xbmc.LOGNOTICE):
    addon = xbmcaddon.Addon()
    addonID = addon.getAddonInfo('id')
    xbmc.log('%s: %s' % (addonID, msg), level)

def getSettings():
    global user
    user = addon.getSetting("user")
    global pw
    pw = addon.getSetting("pw")
    global backNav
    if user == "" or pw == "":
        showErrorNotification("Username or Pw is empty")
        addon.openSettings()
        sys.exit()


def getParams():
    param = {}
    paramstring = sys.argv[2]
    if len(paramstring) >= 2:
        cleanedparams = paramstring.replace('?', '')
        pairsofparams = cleanedparams.split('&')
        for i in range(len(pairsofparams)):
            splitparams = pairsofparams[i].split('=')
            if (len(splitparams)) == 2:
                param[splitparams[0]] = splitparams[1]
    return param


def login():
    getSettings()
    global session
    session = requests.Session()
    headers = {'user-agent': 'Mozilla', 'Content-Type': 'application/x-www-form-urlencoded'}
    payload = {'form': 'UserLogin', 'loginUsername': user, 'loginPassword': pw, 'useCookies': '1'}
    r = session.post(mainUrl + "/index.php", headers=headers, data=payload)
    debug("Login response: " + str(r))
    debug("Set-Cookie: " + r.headers["Set-Cookie"])


def getUrl(url):
    r = session.get(url)
    debug("getUrl response: " + str(r))
    return r.content


def search():
    getTvShowSeasonAndEpisodeFromFile()
    getTvShowSeasonAndEpisodeFromVideoPlayer()
    characters, subItems, select = getSerien()
    if video['tvshow'] == "":
        options = selectCharacter(characters, subItems)
        selectedTvShowId = selectTvShow(options)
        getSeasons(selectedTvShowId)
    else:
        options = findTvShowByTitle(select)
        if len(options) < 1:
            options = selectCharacter(characters, subItems)
            selectedTvShowId = selectTvShow(options)
            getSeasons(selectedTvShowId)
        if len(options) == 1:
            getSeasons(options[0]['value'])
        if len(options) > 1:
            selectedTvShowId = selectTvShow(options)
            getSeasons(selectedTvShowId)


def findTvShowByTitle(select):
    searchString = cleanTitle(video['tvshow'].lower())
    debug("SearchString: "+searchString)
    return select.find_all('option', text=re.compile("(?i)"+searchString))


def selectTvShow(options):
    tvShowIds = []
    tvShowNames = []
    for option in options:
        tvShowIds.append(option['value'])
        tvShowNames.append(option.string)
    dialog = xbmcgui.Dialog()
    selectedTvShowId = dialog.select("subcentral.de - select tvshow", tvShowNames)
    if selectedTvShowId == -1:
        sys.exit()
    return tvShowIds[selectedTvShowId]


def selectCharacter(characters, subItems):
    dialog = xbmcgui.Dialog()
    selectedId = dialog.select("subcentral.de - select character", characters)
    if selectedId == -1:
        sys.exit()
    return subItems[selectedId].find_all("option")


def cleanTitle(title):
    title = title.lower().replace('the ', '')
    title = title.lower().replace(', ', ' ')
    title = title.lower().replace('- ', ' ')
    title = title.lower().replace(': ', ' ')
    title = title.strip()
    return title[0:5]


def getSerien():
    content = getUrl(mainUrl + "/index.php")
    htmlPage = BeautifulSoup(content, 'html.parser')
    select = htmlPage.find("select", {"id": "QJselect"})
    optgroups = select.find_all('optgroup')
    characters = []
    subItems = []
    for character in optgroups:
        subItems.append(character)
        characters.append(character['label'])
    return characters, subItems, select


def addLink(name, url, lang):
    url = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=download"
    if lang == "de":
        icon = "de"
        lang = translation(30110)
    else:
        icon = "en"
        lang = translation(30111)
    xbmcListItem = xbmcgui.ListItem(label=lang, label2=name, thumbnailImage=icon, iconImage=str(5))
    xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=url, listitem=xbmcListItem)


def getEpisodes(url):
    content = getUrl(url)
    showInfoNotification("Loading Subtitle...")
    htmlPage = BeautifulSoup(content, 'html.parser')
    divs = htmlPage.find_all('div', id=re.compile('a\d'))
    if len(divs) < 1:
        quoteBody = htmlPage.find_all("div", class_="quoteBody")
        divs = quoteBody[0].find_all('table')
    for div in divs:
        trs = div.find_all('tr')
        imgs = trs[0].find_all('img')
        for tr in trs:
            if tr.has_attr("class"):
                if tr['class'] == 'inaktiv':
                    continue
            subLinks = tr.find_all('a')
            titles = tr.find_all("td", class_="release")
            if titles is None or len(titles) < 1:
                continue
            episodeTitle = titles[0].string
            for link, img in zip(subLinks, imgs):
                subLink = link.get('href')
                author = link.string
                imgSrc = img.get('src')
                release = img.parent.contents[1]
                match = re.compile('flags\/(.*?)\.', re.DOTALL).findall(imgSrc)
                language = match[0]
                if author is None: author = ""
                if release is None: release = ""
                if episodeTitle is not None and subLink is not None and language is not None:
                    addLink(name=episodeTitle + " " + author + " " + release, url=subLink, lang=language)
    xbmcplugin.endOfDirectory(addon_handle)

def getSeasons(seasonId):
    tvShowUrl = mainUrl + "/index.php?page=Board&boardID=" + seasonId
    content = getUrl(tvShowUrl)
    htmlPage = BeautifulSoup(content, 'html.parser')
    sticky = htmlPage.find("div", {"id": 'stickiesStatus'})
    topics = sticky.find_all('p', id=re.compile('threadTitle\d *'))
    tvShowSeasonUrl = selectSeason(topics)
    getEpisodes(mainUrl + "/" + tvShowSeasonUrl)


def selectSeason(topics):
    seasonNames = []
    seasonsLinks = []
    playingSeasonId = ""
    for index, topic in enumerate(topics):
        if checkCurrentlyPlayingSeason(topic):
            playingSeasonId = index
        names = topic.a.string.split('Staffel')
        if len(names) == 1:
            seasonNames.append(names[0])
        else:
            seasonNames.append('Staffel ' + names[1])
        seasonsLinks.append(topic.a['href'])
    if playingSeasonId != "":
        return seasonsLinks[playingSeasonId]
    dialog = xbmcgui.Dialog()
    selectedSeasonId = dialog.select("subcentral.de", seasonNames)
    if selectedSeasonId == -1:
        sys.exit()
    return seasonsLinks[selectedSeasonId]


def checkCurrentlyPlayingSeason(topic):
    match = re.compile('.*Staffel (\d).*', re.DOTALL).findall(topic.a.string)
    if len(match) > 0:
        debug("Playing: "+str(match[0]))
        debug("Season: "+str(video['season']))
    if video['season'] != "" and len(match) > 0 and video['season'].strip() == match[0].strip():
        return True
    return False

def getTvShowSeasonAndEpisodeFromVideoPlayer():
    global video
    videoPlayer = xbmc.getInfoLabel('VideoPlayer.Title').lower()
    debug("VideoPlayer: "+videoPlayer)
    match = re.compile('(.+?)- s(.+?)e(.+?)', re.DOTALL).findall(videoPlayer)
    if len(match) > 0:
        if video['episode'] == "":
            video['episode'] = match[0][2].strip()
        if video['season'] == "":
            video['season'] = match[0][1].strip()
        if video['tvshow'] == "":
            video['tvshow'] = match[0][0].strip()


def getTvShowSeasonAndEpisodeFromFile():
    global video
    dirName, fileName = getFile()
    matchDir = re.compile('(.+?)- s(.+?)e(.+?)', re.DOTALL).findall(dirName)
    matchFile = re.compile('(.+?)- s(.+?)e(.+?)', re.DOTALL).findall(fileName)
    if len(matchDir) > 0:
        if video['tvshow'] == "":
            video['tvshow'] = matchDir[0][0].strip()
        if video['season'] == "":
            video['season'] = match[0][1].strip()
        if video['episode'] == "":
            video['episode'] = matchDir[0][2].strip()
    if len(matchFile) > 0:
        if video['tvshow'] == "":
            video['tvshow'] = matchFile[0][0].strip()
        if video['season'] == "":
            video['season'] = matchFile[0][1].strip()
        if video['episode'] == "":
            video['episode'] = matchFile[0][2].strip()


def getFile():
    dirName = ""
    fileName = ""
    currentFile = xbmc.Player().getPlayingFile()
    try:
        currentFile = currentFile.replace("\\", "/").split("/")
        dirName = currentFile[-2].lower()
        fileName = currentFile[-1].lower()
    except:
        pass
    return dirName, fileName


def downloadUrlToDirectory(url, directory):
    headers = {'user-agent': 'Mozilla'}
    result = session.get(url, headers=headers, stream=True)
    if result.status_code == 403:
        showErrorNotification("Username or Pw is wrong")
        addon.openSettings()
        sys.exit()
    params = cgi.parse_header(
        result.headers.get('Content-Disposition', ''))[-1]
    if 'filename' not in params:
        debug('downloadUrlToDirectory Could not find a filename')
    filename = os.path.basename(params['filename'])
    abs_path = os.path.join(directory, filename)
    with open(abs_path, 'wb') as target:
        result.raw.decode_content = True
        shutil.copyfileobj(result.raw, target)
    return filename


def downloadSubtitle():
    subtitleUrl = urllib.unquote_plus(params.get('url', ''))
    downloadUrl = mainUrl + "/" + subtitleUrl
    filename = downloadUrlToDirectory(downloadUrl, subtitleDownloadDirectory)
    #fileLocation = subtitleDownloadDirectory + filename
    fileLocation = xbmc.translatePath(os.path.join(subtitleDownloadDirectory, filename)).decode("utf-8")
    debug("BLU :"+fileLocation)
    fileLocation=urllib.quote_plus(fileLocation)
    debug("+####+"+fileLocation)
    showInfoNotification(filename)
    #xbmc.executebuiltin("XBMC.Extract(" + fileLocation + ", " + extractSubtitleDirectory + ")", True)
    try:
        liste=xbmcvfs.listdir("rar://"+fileLocation)
        type="rar://"
    except:    
        liste=xbmcvfs.listdir("zip://"+fileLocation)
        type="zip://"
    debug(fileLocation)
    debug(type)
    debug(liste)
    for element in liste:
        debug(element)
        if not element==[]:
           ziel=xbmc.translatePath(os.path.join(extractSubtitleDirectory, element[0])).decode("utf-8")
           quelle=xbmc.translatePath(os.path.join(type, fileLocation)).decode("utf-8")
           quelle=quelle+"/"+element[0]
           debug(ziel)
           debug(quelle)
           xbmcvfs.copy(quelle, ziel)
           
    selectSubTitleFile()


def selectSubTitleFile():
    subtitleFileList = []
    for file in xbmcvfs.listdir(extractSubtitleDirectory)[1]:
        file = os.path.join(extractSubtitleDirectory, file)
        subtitleFileList.append(file)
    if len(subtitleFileList) > 1:
        dialog = xbmcgui.Dialog()
        fileId = dialog.select("subcentral.de", subtitleFileList)
        subTitleFile = subtitleFileList[fileId]
        xbmcListItem = xbmcgui.ListItem(label=subTitleFile)
    else:
        subTitleFile = subtitleFileList[0]
        xbmcListItem = xbmcgui.ListItem(label=subTitleFile)
    xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=subTitleFile, listitem=xbmcListItem, isFolder=False)
    xbmcplugin.endOfDirectory(addon_handle)


def showInfoNotification(message):
    xbmcgui.Dialog().notification("subcentral.de", message, xbmcgui.NOTIFICATION_INFO, 5000)


def showErrorNotification(message):
    xbmcgui.Dialog().notification("subcentral.de", message, xbmcgui.NOTIFICATION_ERROR, 5000)


createAndResetDirectories()
login()
params = getParams()
if params['action'] == 'search':
    search()
if params['action'] == 'download':
    downloadSubtitle()