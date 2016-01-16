import socket
import time
import threading
from limitlesslight import *
from limitlessscene import *

class LimitlessBridge():
    """The LimitlessLED/MiLight bridge"""
    """ this si the component that enacts change on a group of lights """
    SOCKETRESEND=[0,1,2]
    ANIMATEDLEAY=0.02
    def __init__(self,ipaddress="192.168.0.249",port="8899"):
        self.ipaddress = ipaddress
        self.port = port
        self.state = [None,None,None,None,None]

    def setLightGroupState(self,lightgroup):
        self.state[int(lightgroup.groupid)] = lightgroup

    def getLightGroupState(self,groupid):
        return self.state[int(groupid)]

    def applyScene(self,scene):
        # get our bridge elements from the scenes lightGroups
        lights = scene.getLights(self)
        for light in lights:
            animate=scene.animate
            reference = self.state[light.groupid]
            if reference is None:
                    animate=0
            self.light_scene(light,scene.animate,reference,scene.animateBrightness)
            self.state[light.groupid] = light.clone()
        return

    def __repr__(self):
        return self.ipaddress + ":" + self.port

    def __str__(self):
        return self.__repr__()
    
    def run(self):
        self.alive = True
        # if you want to create child threads, do not make them daemon = True!
        # They will not shutdown properly. (It's a python bug)
    def stop(self):
        self.alive = False
            
    def __send (self,data) : 
        data_ba = bytearray(data)
        try:
            family, type, proto, canonname, sockaddr = socket.getaddrinfo(self.ipaddress, self.port)[0]
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            for i in LimitlessBridge.SOCKETRESEND:
                sock.sendto(data_ba, (sockaddr[0], sockaddr[1]))
            sock.close()
            del(sock)
        except Exception as e:
            print (e)
            pass
        else:
            pass
    
    def light_scene(self,light,animate=0,reference=None,animateBrightness=False):
        if (animate > 0 and reference is not None):
            maxcps           = float(1/LimitlessBridge.ANIMATEDLEAY)
            max_changes      = (float(animate) - 0.1) * maxcps

            colordelta       = float(light.color - reference.color)
            colorsteps       = float(colordelta/max_changes)
            brightdelta      = float(light.brightness - reference.brightness)
            brightsteps      = float(brightdelta/max_changes)
            # we can do max_changes changes each of xsteps in animate time
            self.__animate_light(light,reference,colorsteps,brightsteps,max_changes,animateBrightness)
        else:
            self.__light(light)

    def __light_switch(self,light):
        data = light.getDataOn()
        self.__send(data)
        return light.on

    def __light(self,light):
        if (self.__light_switch(light)):
            cdata = light.getDataColor()
            bdata = light.getDataBrightness()
            time.sleep(0.1)
            self.__send(cdata)
            time.sleep(LimitlessBridge.ANIMATEDLEAY)
            self.__send(bdata)

    def __animate_light(self,light,reference,colorstep,brightnessstep,numsteps,animateBrightness=False):
        if (self.__light_switch(light)):
            cdata = light.getDataColor()
            bdata = light.getDataBrightness()
            #clight = 
            time.sleep(LimitlessBridge.ANIMATEDLEAY)
            rcolor=float(reference.color)
            rbright=float(reference.brightness)
            datac = reference.getDataColor()
            datab = reference.getDataBrightness()
            if animateBrightness == False:
                # because we are not animating brightness, lets set that to target right away
                datab = light.getDataBrightness()
                self.__send(datab)
            while datac[1] != light.color or datab[1] != light.brightness:
                time.sleep(0.01)
                if datac[1] != light.color:
                    rcolor+=colorstep
                if datab[1] != light.brightness:
                    rbright+=brightnessstep
                
                if int(rcolor)!=datac[1]:
                    datac[1]=int(rcolor)
                    if datac[1] > -1 and datac[1] < 256:
                        self.__send(datac)
                if int(rbright)!=datab[1]:
                    if animateBrightness:
                        datab[1]=int(rbright)
                        if datab[1] > -1 and datab[1] < 256:
                            self.__send(datab)
            self.__light(light)   
                

if __name__ == '__main__':
    br = LimitlessBridge()
    br.run()
    redbright = LimitlessScene('redbright',0)
    redbright.addLight(LimitlessLight(br,'rgbw',3,True,'red',26))

    reddim = LimitlessScene('reddim',0)
    reddim.addLight(LimitlessLight(br,'rgbw',3,True,'red',5))
    
    bluebright = LimitlessScene('bluebright',0)
    bluebright.addLight(LimitlessLight(br,'rgbw',3,True,'royal_blue',26))
    
    bluebrightani = LimitlessScene('bluebright',3,False)
    bluebrightani.addLight(LimitlessLight(br,'rgbw',3,True,'royal_blue',26))
    

    bluedim = LimitlessScene('bluedim',0)
    bluedim.addLight(LimitlessLight(br,'rgbw',3,True,'royal_blue',5))

    off = LimitlessScene('off',0)
    off.addLight(LimitlessLight(br,'rgbw',3,False,-1,27))

    normal = LimitlessScene('normal',0)
    normal.addLight(LimitlessLight(br,'rgbw',3,True,-1,27))

    br.applyScene(reddim)
    time.sleep(5)
    br.applyScene(off)
    time.sleep(5)
    br.applyScene(normal)
    #l3 = LimitlessLight(br,'rgbw',3,True,'red',26)
    #l3b = LimitlessLight(br,'rgbw',3,True,'yellow',3)
    #br.light_scene(l3,1,l3b)
    #br.light_scene(l3b,1,l3)
    #br.light_scene(l3,1,l3b)
