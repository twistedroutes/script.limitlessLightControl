import os
import time
import xbmc
import xbmcgui
import xbmcaddon
import logging
import re

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
#infolabels=["Container.Content","Container.FolderPath","Container.FolderName","Container.Viewmode","Container.SortMethod","Container.SortOrer","Container.PluginName","Container.PluginCategory","Container.ShowPlot","Container(id).NumPages","Container(id).NumItems","Container(id).CurrentPage","Container(id).CurrentItem","Container(id).Position","Container(id).Column","Container(id).Row","Container(id).Totaltime","Container(id).TotalWatched","Container(id).TotalUnWatched","Container(id).ListItem(offset).Label","Container(id).ListItem(offset).Label2","Container(id).ListItem(offset).Icon","Container(id).ListItem(offset).ActualIcon","Container(id).ListItem(offset).Thumb","Container(id).ListItemNoWrap(offset).Property","Container(id).ListItemPosition(id).[infolabel]","Container(id).ListItemAbsolute(id).[infolabel]","Container.Property(addoncategory)","Container.Property(reponame)","Listitem.Label","ListItem.Label2","ListItem.Title","ListItem.OriginalTitle","ListItem.SortLetter","ListItem.TrackNumber","ListItem.Artist","ListItem.AlbumArtist","ListItem.Property(Artist_Born)","ListItem.Property(Artist_Died)","ListItem.Property(Artist_Formed)","ListItem.Property(Artist_Disbanded)","ListItem.Property(Artist_YearsActive)","ListItem.Property(Artist_Instrument)","ListItem.Property(Artist_Description)","ListItem.Property(Artist_Mood)","ListItem.Property(Artist_Style)","ListItem.Property(Artist_Genre)","ListItem.Album","ListItem.Property(Album_Mood)","ListItem.Property(Album_Style)","ListItem.Property(Album_Theme)","ListItem.Property(Album_Type)","ListItem.Property(Album_Label)","ListItem.Property(Album_Description)","ListItem.DiscNumber","ListItem.Year","ListItem.Premiered","ListItem.Genre","ListItem.Director","ListItem.Country","ListItem.Episode","ListItem.Season","ListItem.TVShowTitle","ListItem.Property(TotalSeasons)","ListItem.Property(TotalEpisodes)","ListItem.Property(WatchedEpisodes)","ListItem.Property(UnWatchedEpisodes)","ListItem.Property(NumEpisodes)","ListItem.PictureAperture","ListItem.PictureAuthor","ListItem.PictureByline","ListItem.PictureBylineTitle","ListItem.PictureCamMake","ListItem.PictureCamModel","ListItem.PictureCaption","ListItem.PictureCategory","ListItem.PictureCCDWidth","ListItem.PictureCity","ListItem.PictureColour","ListItem.PictureComment","ListItem.PictureCopyrightNotice","ListItem.PictureCountry","ListItem.PictureCountryCode","ListItem.PictureCredit","ListItem.PictureDate","ListItem.PictureDatetime","ListItem.PictureDesc","ListItem.PictureDigitalZoom","ListItem.PictureExpMode","ListItem.PictureExposure","ListItem.PictureExposureBias","ListItem.PictureExpTime","ListItem.PictureFlashUsed","ListItem.PictureFocalLen","ListItem.PictureFocusDist","ListItem.PictureGPSLat","ListItem.PictureGPSLon","ListItem.PictureGPSAlt","ListItem.PictureHeadline","ListItem.PictureImageType","ListItem.PictureIPTCDate","ListItem.PictureIPTCTime","ListItem.PictureISO","ListItem.PictureKeywords","ListItem.PictureLightSource","ListItem.PictureLongDate","ListItem.PictureLongDatetime","ListItem.PictureMeteringMode","ListItem.PictureObjectName","ListItem.PictureOrientation","ListItem.PicturePath","ListItem.PictureProcess","ListItem.PictureReferenceService","ListItem.PictureResolution","ListItem.PictureSource","ListItem.PictureSpecialInstructions","ListItem.PictureState","ListItem.PictureSublocation","ListItem.PictureSupplementalCategories","ListItem.PictureTransmissionReference","ListItem.PictureUrgency","ListItem.PictureWhiteBalance","ListItem.FileName","ListItem.Path","ListItem.FolderName","ListItem.FolderPath","ListItem.FileNameAndPath","ListItem.FileExtension","ListItem.Date","ListItem.DateAdded","ListItem.Size","ListItem.Rating","ListItem.UserRating","ListItem.Votes","ListItem.RatingAndVotes","ListItem.Mpaa","ListItem.ProgramCount","ListItem.Duration","ListItem.DBTYPE","ListItem.DBID","ListItem.Cast","ListItem.CastAndRole","ListItem.Studio","ListItem.Top250","ListItem.Trailer","ListItem.Writer","ListItem.Tagline","ListItem.PlotOutline","ListItem.Plot","ListItem.IMDBNumber","ListItem.EpisodeName","ListItem.PercentPlayed","ListItem.LastPlayed","ListItem.PlayCount","ListItem.StartTime","ListItem.EndTime","ListItem.StartDate","ListItem.ChannelNumber","ListItem.ChannelName","ListItem.VideoCodec","ListItem.VideoResolution","ListItem.VideoAspect","ListItem.AudioCodec","ListItem.AudioChannels","ListItem.AudioLanguage","ListItem.SubtitleLanguage","ListItem.Property(AudioCodec.[n])","ListItem.Property(AudioChannels.[n])","ListItem.Property(AudioLanguage.[n])","ListItem.Property(SubtitleLanguage.[n])","ListItem.Property(Addon.Name)","ListItem.Property(Addon.Version)","ListItem.Property(Addon.Summary)","ListItem.Property(Addon.Description)","ListItem.Property(Addon.Type)","ListItem.Property(Addon.Creator)","ListItem.Property(Addon.Disclaimer)","ListItem.Property(Addon.Changelog)","ListItem.Property(Addon.ID)","ListItem.Property(Addon.Status)","ListItem.Property(Addon.Broken)","ListItem.Property(Addon.Path)","ListItem.StartTime","ListItem.EndTime","ListItem.StartDate","ListItem.EndDate","ListItem.NextTitle","ListItem.NextGenre","ListItem.NextPlot","ListItem.NextPlotOutline","ListItem.NextStartTime","ListItem.NextEndTime","ListItem.NextStartDate","ListItem.NextEndDate","ListItem.ChannelName","ListItem.ChannelNumber","ListItem.ChannelGroup","ListItem.SubChannelNumber","ListItem.ChannelNumberLabel","ListItem.Progress","ListItem.StereoscopicMode","ListItem.IsSelected","ListItem.IsPlaying","ListItem.IsResumable","ListItem.IsFolder","ListItem.IsCollection","ListItem.IsRecording","ListItem.Comment","Player.FinishTime","Player.FinishTime(format)","Player.Chapter","Player.ChapterCount","Player.Time","Player.Time(format)","Player.TimeRemaining","Player.TimeRemaining(format)","Player.Duration","Player.Duration(format)","Player.SeekTime","Player.SeekOffset","Player.SeekOffset(format)","Player.SeekStepSize","Player.ProgressCache","Player.Folderpath","Player.Filenameandpath","Player.StartTime","Player.StartTime(format)","Player.Title","Player.Filename","MusicPlayer.Title","MusicPlayer.Album","MusicPlayer.Property(Album_Mood)","MusicPlayer.Property(Album_Style)","MusicPlayer.Property(Album_Theme)","MusicPlayer.Property(Album_Type)","MusicPlayer.Property(Album_Label)","MusicPlayer.Property(Album_Description)","MusicPlayer.Artist","MusicPlayer.Property(Artist_Born)","MusicPlayer.Property(Artist_Died)","MusicPlayer.Property(Artist_Formed)","MusicPlayer.Property(Artist_Disbanded)","MusicPlayer.Property(Artist_YearsActive)","MusicPlayer.Property(Artist_Instrument)","MusicPlayer.Property(Artist_Description)","MusicPlayer.Property(Artist_Mood)","MusicPlayer.Property(Artist_Style)","MusicPlayer.Property(Artist_Genre)","MusicPlayer.Genre","MusicPlayer.Lyrics","MusicPlayer.Year","MusicPlayer.Rating","MusicPlayer.DiscNumber","MusicPlayer.Comment","MusicPlayer.Time","MusicPlayer.TimeRemaining","MusicPlayer.TimeSpeed","MusicPlayer.TrackNumber","MusicPlayer.Duration","MusicPlayer.BitRate","MusicPlayer.Channels","MusicPlayer.BitsPerSample","MusicPlayer.SampleRate","MusicPlayer.Codec","MusicPlayer.PlaylistPosition","MusicPlayer.PlaylistLength","MusicPlayer.ChannelName","MusicPlayer.ChannelNumber","MusicPlayer.SubChannelNumber","MusicPlayer.ChannelNumberLabel","MusicPlayer.ChannelGroup","VideoPlayer.Time","VideoPlayer.TimeRemaining","VideoPlayer.TimeSpeed","VideoPlayer.Duration","VideoPlayer.Title","VideoPlayer.TVShowTitle","VideoPlayer.Season","VideoPlayer.Episode","VideoPlayer.Genre","VideoPlayer.Director","VideoPlayer.Country","VideoPlayer.Year","VideoPlayer.Rating","VideoPlayer.UserRating","VideoPlayer.Votes","VideoPlayer.RatingAndVotes","VideoPlayer.mpaa","VideoPlayer.IMDBNumber","VideoPlayer.EpisodeName","VideoPlayer.PlaylistPosition","VideoPlayer.PlaylistLength","VideoPlayer.Cast","VideoPlayer.CastAndRole","VideoPlayer.Album","VideoPlayer.Artist","VideoPlayer.Studio","VideoPlayer.Writer","VideoPlayer.Tagline","VideoPlayer.PlotOutline","VideoPlayer.Plot","VideoPlayer.LastPlayed","VideoPlayer.PlayCount","VideoPlayer.VideoCodec","VideoPlayer.VideoResolution","VideoPlayer.VideoAspect","VideoPlayer.AudioCodec","VideoPlayer.AudioChannels","VideoPlayer.AudioLanguage","VideoPlayer.SubtitlesLanguage","VideoPlayer.StereoscopicMode","VideoPlayer.EndTime","VideoPlayer.NextTitle","VideoPlayer.NextGenre","VideoPlayer.NextPlot","VideoPlayer.NextPlotOutline","VideoPlayer.NextStartTime","VideoPlayer.NextEndTime","VideoPlayer.NextDuration","VideoPlayer.ChannelName","VideoPlayer.ChannelNumber","VideoPlayer.SubChannelNumber","VideoPlayer.ChannelNumberLabel","VideoPlayer.ChannelGroup","VideoPlayer.ParentalRating"]

re_tv    = re.compile('[\W](?:s\d\de\d\d|tv|episode)[\W]',re.IGNORECASE)
re_movie = re.compile('[\W](?:movie|\([12][09]\d\d)[\W]',re.IGNORECASE)

def determineContent(playingFile):
    'type playingFile: string'
    'returns contenttype: string'
    if xbmc.getInfoLabel('VideoPlayer.Episode') != "":
        return "tv"
    elif xbmc.getInfoLabel('VideoPlayer.mpaa') != "":
        return "movie"
    elif xbmc.getInfoLabel('VideoPlayer.Duration') != "":
        if re_tv.search(playingFile) is not None:
            return "tv"
        if re_movie.search(playingFile) is not None:
            return "movie"
        return "video"
    else:
        #xbmc.getInfoLabel('MusicPlayer.Codec')
        return "music"

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

        # Can't use "content" to determien the content as it shows to be unreliable (as of Jarvis b4)
        # content     = xbmc.getInfoLabel('Container.Content')
        content = determineContent(playingFile)
        utils.log_verbose("content: " + content + " file: " + playingFile)
        #for l in infolabels:
        #    ld = xbmc.getInfoLabel(l)
        #    if ld != "":
        #        utils.log_verbose(l + ": " + ld)
        
        if self.isPlaying :
            utils.log_verbose(content + ": " + playingFile)
            # activity references a scene or none

            if (content):
                if (content == "movie"):
                    return service.bridge.applyScene(getSceneByActivity("movie"))
                elif (content == "tv"):
                    return service.bridge.applyScene(getSceneByActivity("tv"))
                elif (content == "music"):
                    return service.bridge.applyScene(getSceneByActivity("music"))
                else:
                    return service.bridge.applyScene(getSceneByActivity("video"))
            else:
                return service.bridge.applyScene(getSceneByActivity("video"))
    
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

        monitor = utils.Monitor(updateCallback=self.settings_changed)
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

