import os
import xbmcaddon
import xbmc

__addon__        = xbmcaddon.Addon()

dir_to_search = __addon__.getSetting('dir_to_search')
pattern_to_search = __addon__.getSetting('pattern_to_search')

for root, dirs, files in os.walk(dir_to_search):
    for name in files:
        (base, ext) = os.path.splitext(name) 
        if pattern_to_search in (base):          
            full_name = os.path.join(root, name)
            os.remove(full_name)
            xbmc.log('Script.Delete.Files logging: ' + full_name + ' removed')