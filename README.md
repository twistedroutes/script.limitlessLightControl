## script.LimitlessLightControl

This project enables control of [LimitlessLED](http://limitlessled.com)/[MiLight](http://www.milight.com/) bridges and light groups directly from Kodi without the need for running an additional home automation controller.
It has the ability to set lighting scenes based on Kodi activity (e.g. when playing a video)

### Setup
While there are many options, setup is fairly straight forward.
* Choose "settings" or "configure plugin"
* set bridge settings (only 1 bridge supported right now, more to come)

#### Activities
Lighting scenes can be automatically applied when an event occurs (activity)
* Enable Activities
* Select which scene should apply to each activity
  * Movie    - When played from your library, we can differentiate between movies and TV
  * TV       - again, when played from your library
  * Video    - When video playback starts, but the source is not your library (e.g. a streaming plugin or direcly from file/NAS/SMB etc) we can't differentiate.  WOrking on ways to differentiate
  * Music    - when you are playing music (note the "disco" option of the lights is not yet implemented.)
  * Stop     - when playback ends, is stopped or terminates
  * Pause    - when playback is paused (intermission :-) )
  * Startup  - when Kodi starts (when script starts in reality)
  * Shutdown - when kodi shutsdown/script shuts down
    * to do nothing when an activity occurs, select the "None" scene
* Now go configure the scenes

#### Scenes
Scenes configure a lighting configuration (which lights/lightGroups, color, brightness etc)
* Select the lightGroups to be involved
* Configure the color and Brightness
  * 0 Brightness = off
* Scenes available to configure are
  * Normal	- recommend using this as you "on" light
  * Dimmed	- recommend setting this as your preferred dimmed or 'sexy-time' light
  * Reading  - recommend an orange or yellow, slightly dimmed setting which seems comfortable for reading
  * Video    - recommend a red or blue light, works well behind the TV
  * Movie    - recommend a red or blue light, works well behind the TV
  * TV       - recommend a red or blue light, works well behind the TV
  * Music    - recommend...no recommendation, I'm just not cool enough
  * Off      - recommend using this to turn desired lights off.  I sued this as my schutdown activities scene

#### Menu Integration
Various skins allow menu customization.  In my case, I am using the "Arctic Zephyr" skin and have configured various actions (see the screenshots)
* LightControl    - this just calls the script directly with no parameters.  Alternatively you can run the action: RunScript(script.limitlessLightControl)
* Lights-On       - RunScript(script.limitlessLightControl,"scene","Normal")
* Lights-Off      - RunScript(script.limitlessLightControl,"scene","Off")
* Lights-Settings - RunScript(script.limitlessLightControl,"settings")
* Lights-Events   - RunScript(script.limitlessLightControl,"toggle") 

### Screenshots
[![001](http://ibin.co/2ThgIQN5py3G)](http://ibin.co/2ThdZVxCKIeO)
[![002](http://ibin.co/2ThgLEaaYh2v)](http://ibin.co/2ThdhwbgU6rI)
[![003](http://ibin.co/2ThgNjRuyQB1)](http://ibin.co/2ThdmJc0iO0H)
[![004](http://ibin.co/2ThgQXfPh7Ao)](http://ibin.co/2ThdqgcKwpXM)
[![005](http://ibin.co/2ThgTLsuPou2)](http://ibin.co/2ThduQuKZpyK)
[![006](http://ibin.co/2ThgWA6P8VZA)](http://ibin.co/2The03LK0tmr)

### ToDo
* Disco Mode (easy to do)
* Multiple bridges (need more lights and bridges)
* Dynamic TV/Movie color (based on average picture color)
* Dynamic Music color (based on music beat)
