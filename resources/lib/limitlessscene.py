from limitlesslight import *
from limitlessbridge import *

class LimitlessScene(object):

    def __init__(self,name="",animate=0, animateBrightness=False):
        self.name = name
        self.animate = animate
        self.animateBrightness = animateBrightness
        self.lightGroups = {}

    def addLight(self,light):
        'type light: LimitlessLight'
        if (light):
            lighttype= light.type
            lightid  = light.groupid
            bridge   = light.bridge
            self.lightGroups.update({bridge:{lightid:light}})
            a='b'

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
            

