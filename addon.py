import xbmcaddon
import xbmcgui
import logging
import threading
import socket
import time
import random
import sys
from resources.lib.limitlessbridge import *
from resources.lib.limitlesslight import *
from resources.lib.limitlessscene import *
from resources.lib import utils
from service import SCENES

addon	    = xbmcaddon.Addon()
addonname   = addon.getAddonInfo('name')

class Main(object):
    def __init__(self,scenename):
        utils.log_normal("Applying Scene: " + scenename)
        self.bridge = LimitlessBridge(addon.getSetting("b0_host"),addon.getSetting("b0_port"))
        scene = LimitlessScene(scenename,0,False)
        for i in ("0","1","2","3","4"):
            lowerscenename = scenename.lower()
            enabled=utils.get_bool_setting("b0_l"+i+"_"+lowerscenename+"_enable")
            if enabled:
                color       = utils.get_setting("b0_l"+i+"_"+lowerscenename+"_color")
                brightness  = utils.get_setting("b0_l"+i+"_"+lowerscenename+"_brightness")
                light       = LimitlessLight(self.bridge,'rgbw',i,True,color,brightness)
                utils.log_verbose("Settings: label: " + lowerscenename + " scenename: " + scenename + " lights: " + str(light))
                scene.addLight(light)
        self.bridge.applyScene(scene)

if __name__ == "__main__":
    count = len(sys.argv) - 1
    if count > 0:
        Main(sys.argv[1])
        
    else:
        dialog = xbmcgui.Dialog()
        activityState = utils.get_bool_setting("activity_enable")
        currentState = "Enabled" if activityState else "Disabled"
        toggleState = "Disable" if activityState else "Enable"
        options = sorted([elem for elem in SCENES.keys() if elem!="None"])
        change_index = len(options)
        options.append(" - " + toggleState + " Activities -")
        options.append(" - Settings -")
        options.append(" - Cancel - ")
        rets = dialog.select("Select a Scene (Activities " + currentState + ")",options)
        txt = options[rets]
        if rets < change_index:
            Main(options[rets])
        elif txt == " - Settings -":
            utils.open_settings()
        elif txt == " - Enable Activities -":
            utils.set_setting("activity_enable","true")
            dialog = xbmcgui.Dialog().ok("Activities Enabled","Scenes will be applied according to your activity settings")
        elif txt == " - Disable Activities -":
            utils.set_setting("activity_enable","false")
            dialog = xbmcgui.Dialog().ok("Activities Disabled","Scenes will be no loger be applied.  You may still manually control the scene.")
        pass

