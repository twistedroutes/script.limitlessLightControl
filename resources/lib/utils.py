import xbmc
import xbmcaddon
import xbmcgui
import os
import time
import glob

__addon__ = xbmcaddon.Addon()
__id__ = __addon__.getAddonInfo('id')
__icon__  = __addon__.getAddonInfo('icon').decode("utf-8")
__version__ = __addon__.getAddonInfo('version')
addon_name = __addon__.getAddonInfo('name')

def log(message, level=xbmc.LOGNOTICE):
    xbmc.log("{0} v{1}: {2}".format(__id__, __version__, message), level=level)
       
def log_normal(message):
    if int(__addon__.getSetting('debug')) > 0:
        log(message)
    
def log_verbose(message):
    if int(__addon__.getSetting('debug')) == 2:
        log(message)
        
def log_error(message):
    log(message, xbmc.LOGERROR)        

def notify(msg, time=10000):
    xbmcgui.Dialog().notification(addon_name, msg, __icon__, time)

def addon_info(info):
    return __addon__.getAddonInfo(info)

def get_string(key):
    return __addon__.getLocalizedString(key)

def get_setting(key):
    return __addon__.getSetting(key)

def get_bool_setting(key):
    return get_setting(key) == "true"

def get_int_setting(key):
    try:
        return int(get_setting(key))
    except ValueError:
        return None

def get_float_setting(key):
    return float(get_setting(key))

def set_setting(key, value):
    __addon__.setSetting(key, value)

def open_settings(callback=None):
    if callback is not None:
        callback()
    __addon__.openSettings()

def error_dialog(msg):
    xbmcgui.Dialog().ok("Error", msg)
    open_settings()

class Monitor(xbmc.Monitor):
    def __init__(self, updateCallback):
        xbmc.Monitor.__init__(self)
        self.updateCallback = updateCallback

    def onSettingsChanged(self):
        self.updateCallback()
