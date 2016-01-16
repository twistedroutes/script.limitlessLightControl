import os
import time
import xbmc
import xbmcgui
import xbmcaddon
import logging

from resources.lib import utils
from resources.lib.limitlessbridge import *
from resources.lib.limitlesslight import *
from resources.lib.limitlessscene import *

#TODO
# multiple bridges
# animation/transition
# Automate adding menu items

addon	   = xbmcaddon.Addon()
addonname  = addon.getAddonInfo('name')

ACTIVITIES = {"video":None,"movie":None,"tv":None,"music":None,"stop":None,"pause":None,"startup":None,"shutdown":None}
SCENES = {"None":[],"Normal":[],"Dimmed":[],"Reading":[],"Movie":[],"TV":[],"Video":[],"Music":[],"Off":[]}
__addon__ = xbmcaddon.Addon()

def getSceneByActivity(activity):
    if activity in ACTIVITIES:
        return SCENES[ACTIVITIES[activity]]
    return None

class CustomPlayer(xbmc.Player):
    def __init__( self, *args ):
        pass

    def setService(self,service):
        self.service=service
        self.bridge = service.bridge

    def onPlayBackStarted(self):
        if utils.get_bool_setting("activity_enable") == False:
            return
        service = self.service
        # in the future we can either use a call-back pattern (if I can figure that out in python)
        # for multiple bridges that would allow the service logic (or a bridge-manager object) to fire events to all bridges
        playingFile = self.getPlayingFile()
        content     = xbmc.getInfoLabel('Container.Content')
        utils.log_verbose("onPlayBackStarted: file = " + playingFile)
        
        if self.isPlayingVideo:
            # activity references a scene or none

            if (content):
                if (content == "movies"):
                    return service.bridge.applyScene(getSceneByActivity("movie"))
                else:
                    if (content == "episodes"):
                        return service.bridge.applyScene(getSceneByActivity("tv"))
                    else:
                        return service.bridge.applyScene(getSceneByActivity("video"))
            else:
                return service.bridge.applyScene(getSceneByActivity("video"))
        else:
            utils.log_verbose("Audio: " + self.getPlayingFile())
            return service.bridge.applyScene(getSceneByActivity("music"))
    
    def onPlayBackResumed(self):
        return self.onPlayBackStarted()

    def onPlayBackEnded(self):
        if utils.get_bool_setting("activity_enable"):
            return self.service.bridge.applyScene(getSceneByActivity("stop"))

    def onPlayBackPaused(self):
        if utils.get_bool_setting("activity_enable"):
            return self.service.bridge.applyScene(getSceneByActivity("pause"))

    def onPlayBackStopped(self):
        return self.onPlayBackEnded()

    def onStartup(self):
        if utils.get_bool_setting("activity_enable"):
            return self.service.bridge.applyScene(getSceneByActivity("startup"))
    
    def onShutdown(self):
        if utils.get_bool_setting("activity_enable"):
            return self.service.bridge.applyScene(getSceneByActivity("shutdown"))


class Main(object):
    def __init__(self):
        utils.log_normal("Starting service")

        monitor = utils.Monitor(updated_settings_callback=self.settings_changed)
        self.configured = self.apply_basic_settings()
        if self.configured:            
            self.bridge.run()
            utils.log_verbose("Bridge ip: " + self.bridge.ipaddress + " port: " + self.bridge.port)

            myplayer = CustomPlayer();
            myplayer.setService(self)
            myplayer.onStartup()

        while not monitor.abortRequested():
            # Sleep/wait for abort for 10 seconds
            if monitor.waitForAbort(4):
                # Abort was requested while waiting. We should exit
                myplayer.onShutdown()
                self.bridge.stop()
                break

    def getScene(self,sceneName=None):        
        if sceneName in SCENES:
            return SCENES[sceneName]
        return None
                
    def settings_changed(self):
        utils.log_verbose("Applying settings")
        self.configured = self.apply_basic_settings()

    def apply_basic_settings(self):
        global SCENES
        scenenames = SCENES.keys()
        labels = map(lambda x:x.lower(),scenenames)
        utils.log_verbose("Applying basic settings")
        # Get the bridges
        self.bridge = LimitlessBridge(__addon__.getSetting("b0_host"),__addon__.getSetting("b0_port"))

        # Get the scenes
        #labels     =["normal","dimmed","reading","movie","tv","music"]
        #scenenames = ["Normal","Dimmed","Reading","Movie","TV","Music"]
        for label,scenename in zip (labels,scenenames):
            scene = LimitlessScene(scenename,0,False)
            for i in ("0","1","2","3","4"):
                enabled=utils.get_bool_setting("b0_l"+i+"_"+label+"_enable")
                if enabled:
                    color       = utils.get_setting("b0_l"+i+"_"+label+"_color")
                    brightness  = utils.get_setting("b0_l"+i+"_"+label+"_brightness")
                    light       = LimitlessLight(self.bridge,'rgbw',i,True,color,brightness)
                    utils.log_verbose("Settings: label: " + label + " scenename: " + scenename + " lights: " + str(light))
                    scene.addLight(light)
            SCENES[scenename] = scene
        for activity in ACTIVITIES.keys():
            # map activity to scenes
            activity_scene = utils.get_setting("activity_"+activity)
            ACTIVITIES[activity] = activity_scene
        utils.log_verbose("Enabled: " + utils.get_setting("activity_enable"))
        return True

if __name__ == "__main__":
    #monitor = xbmc.Monitor()    
    

    Main()

