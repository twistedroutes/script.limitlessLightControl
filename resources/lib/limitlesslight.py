from limitlessbridge import *

class LimitlessLight(object):
    MINBRIGHT=2
    MAXBRIGHT=27
    DEFAULTBRIGHT=20
    MAXCOLOR=255
    DEFAULTCOLOR=-1
    DEFAULTON=True
    DEFAULTTYPE='rgbw'

    colorNameMap = {             # for reference and future use
            'white':        -1,
            'violet':       0x00,
            'royal_blue':   0x10,
            'baby_blue':    0x20,
            'aqua':         0x30,
            'mint':         0x40,
            'seafoam_green':0x50,
            'green':        0x60,
            'lime_green':   0x70,
            'yellow':       0x80,
            'yellow_orange':0x90,
            'orange':       0xA0,
            'red':          0xB0,
            'pink':         0xC0,
            'fuschia':      0xD0,
            'lilac':        0xE0,
            'lavender':     0xF0
        }
    
    def __init__(self, bridge, type=DEFAULTTYPE, groupid=0, on=DEFAULTON, color=DEFAULTCOLOR, brightness=DEFAULTBRIGHT):    
        self.bridge     = bridge
        self.type       = type
        self.groupid    = int(groupid)
        self.on         = self.getOn(on)
        self.color      = self.getColorFromMap(color)
        self.brightness = self.getBrightness(brightness)
    
    def clone(self):
        return LimitlessLight(self.bridge,self.type,self.groupid,self.on,self.color,self.brightness)    
        
    def getColorFromMap(self, colorname=DEFAULTCOLOR):
        try:
            if (str(colorname).isdigit()):
                return min(int(colorname),LimitlessLight.MAXCOLOR)
            if LimitlessLight.colorNameMap[colorname]:
                return LimitlessLight.colorNameMap[colorname]
        except:
            return -1

    def getBridge(self):
        return self.bridge

    def getBrightness(self,brightness=None):
        if (brightness is None):
            return self.brightness
        else:
            try:
                if ( int(brightness) < LimitlessLight.MINBRIGHT ) :
                    self.on=False
                return max(min(int(brightness),LimitlessLight.MAXBRIGHT),LimitlessLight.MINBRIGHT)
            except:
                pass
        return LimitlessLight.DEFAULTBRIGHT
    
    def getOn(self,onstate=None):
        if (onstate is None):
            return self.on
        else:
            return onstate==True 

    def getDataOn(self):
        # on:   0-66 1-69 2-71 3-73 4-75
        # off:  0-65 2-70 2-72 3-74 4-76
        onoff=1 if self.on == True else 2
        
        ret = [66+(2*self.groupid),0,85]
        if self.groupid > 0:
            ret[0]+=onoff
        elif self.on == False:
            ret[0]-=1
        return ret            
    
    def getDataColor(self):
        if self.color == -1:
            return self.getDataColorWhite()
        return self.getDataColorRGB()

    def getDataColorWhite(self):
        # caller should use getDataOn first then delay 100ms
        # 0-194 1-197 2-199 3-201 4-203
        ret=[194+(2*self.groupid)+1,0,85]
        if self.groupid == 0:
            ret[0]-=1
        return ret

    def getDataColorRGB(self):
        # caller should use getDataOn first then delay 100ms
        # byte0 is 0x40 (64), byte 1 is the color
        return [64,self.color,85]
        
    def getDataBrightness(self):
        # caller should use getDataOn first then delay 100ms
        # byte0 is 0x4B (78), byte 1 is the color
        return [78,self.brightness,85]

    def __repr__(self):
        return "LimitlessLight= " + str(self.bridge) + ":" + str(self.groupid) + " color: " + str(self.color) + "@" + str(self.brightness)

    def __str__(self):
        return self.__repr__()