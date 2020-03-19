import sys
import xbmc, xbmcgui, xbmcaddon
import SimpleHTTPServer
import SocketServer
import urlparse
import ewetv

addon = xbmcaddon.Addon()
username = addon.getSetting('username')
password = addon.getSetting('password')
host = addon.getSetting('host')
port = int(addon.getSetting('port'))

channels_file = addon.getSetting('playlist_path') + 'iptv_channels.m3u'

class myHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def do_GET(self):
        params = urlparse.parse_qs(self.path)
        if '/channel.m3u8?channel_id' in params:
            print params['/channel.m3u8?channel_id'][0]          
            tv.current_channel_id = params['/channel.m3u8?channel_id'][0] 
        self.send_response(301)
        red_location = tv.getChannelUrl()
        self.send_header('Location', red_location)
        self.end_headers()

tv = ewetv.EweTv(username, password)
if tv.login():
    hasChanges = tv.generateM3U(channels_file, host, port)
    if hasChanges:
        xbmcgui.Dialog().notification('EWE IPTV', 'Es wurden neue Sender gefunden. Neustart erforderlich!', xbmcgui.NOTIFICATION_INFO, 5000, True)
    monitor = xbmc.Monitor()
    xbmc.log("Starting EWE-IPTV wrapper on port " + str(port))
    SocketServer.TCPServer.allow_reuse_address = True
    handler = SocketServer.TCPServer((host, port), myHandler)
    handler.serve_forever()
     
    while not monitor.abortRequested():
        # Sleep/wait for abort for 10 seconds
        if monitor.waitForAbort(10):
            # Abort was requested while waiting. We should exit
            handler.shutdown()
            break

else:
    xbmcgui.Dialog().notification('EWE TV Fehler', 'Fehler bei Login', xbmcgui.NOTIFICATION_ERROR, 2000, True)



