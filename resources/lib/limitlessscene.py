from limitlesslight import *
from limitlessbridge import *
import utils

class LimitlessScene(object):

    def __init__(self,name="",animate=0, animateBrightness=False):
        self.name = name
        self.animate = animate
        self.animateBrightness = animateBrightness
        self.lightGroups = {}

    def addLight(self,light):
        'type light: LimitlessLight'
        utils.log_verbose("LimitlessScene.addLight: " + str(light))
        if (light):
            lighttype= light.type
            lightid  = light.groupid
            bridge   = light.bridge
            if bridge not in self.lightGroups:
                self.lightGroups[bridge] = {lightid:light}
            #self.lightGroups.update({bridge:{lightid:light}})
            self.lightGroups[bridge][lightid] = light

    def addLights(self,lights):
        for light in lights:
            self.addLight(light)

    def getLights(self,bridge=None):
        retlight = []
        if bridge is None:         
            bridges=self.lightGroups.keys()
        else:
            bridges=[bridge]
        for reqbridge in bridges:
            try:
                for lightid in self.lightGroups[reqbridge]:
                    if (lightid in self.lightGroups[reqbridge]):
                        retlight.append(self.lightGroups[reqbridge][lightid])
            except:
                pass
        return retlight

    def getAnimate(self):
        return self.animate
            

