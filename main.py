from kivy.app import App
from kivy.lang.builder import Builder

from kivy.uix.screenadmin import Screenadmin, Screen

from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout

from kivy.uix.widget import Widget

# from kivy.factory import Factory
from kivy.properties import ObjectProperty, NumericProperty
from kivy.uix.popup import Popup

from kivy.clock import Clock

# from kivy.core.window import Window

import vlc

from os.path import isfile, isdir, join
from os import walk
from re import search

from subprocess import check_output
import re

import rpirpconfig

global player


class SwitchSongs:
    def __init__(self, value):
        self.value = value
        self.len = len(value)

    def __iter__(self):
        self.index = 0
        return self

    def __next__(self):
        self.index += 1
        if 0 < self.index < self.len:
            return self.value[self.index]
        else:
            self.index = 0
            return self.value[0]
#            raise StopIteration

    def __previous__(self):
        self.index -= 1
        if 0 < self.index < self.len:
            return self.value[self.index]
        else:
            self.index = 0
            return self.value[0]
#            raise StopIteration


def FileFolder(path, filename):
    """Takes two arguments: path, filename
    returns folder or file depending on the input"""

    if isfile(filename):
        return "file"
    elif isdir(filename):
        return "folder"


class Radio(Widget):
    isplaying = NumericProperty(0)


class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)
    load_file = ObjectProperty(None)
    text_input = ObjectProperty(None)

    def get_path(self):
        return rpirpconfig.path_to_folder


class KesselWindow(Screen):
    loadfile = ObjectProperty(None)
    text_input = ObjectProperty(None)
    song_list = []
    playfolder = False
    _current = None
    _paused = False

#    def __init__(f):
        #mediaplayer = sm.KesselWindow()
#        self.start_player()
#        Clock.schedule_interval(self.update, 1.0)

    def get_attributes(self):
        return rpirpconfig.radio_stations

    def play_music(self, path, filename):

        self.start_player()
        Clock.schedule_interval(self.update, 1.0)
        # If it is a folder, then loop through folder
        # Otherwise play single song
        file_or_folder = FileFolder(path, filename[0])

        self._popup.dismiss()
        if file_or_folder == "file":
            self._list_player = vlc.MediaPlayer(filename[0])
            self._list_player.play()
            self._current = filename[0]

        if file_or_folder == "folder":
            for root, dirs, files in walk(path):
                for name in files:
                    if search("mp3", name) or search("ogg", name):
                        self.song_list.append(join(root, name))

            self.playfolder = True

            self.songiter = SwitchSongs(self.song_list).__iter__()

    def show_load(self):
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Lade Musik", content=content, size_hint=(1, 1))
        self._popup.open()

    def load(self, path, filename):
        self.text_input.text = str(filename)
        self.dismiss_popup()
        self.play_music(path, filename)

    def dismiss_popup(self, instance=None):
        # if "player" in locals() or "player" in globals():
        self._popup.dismiss()

    def play_radio(self, url):
        radio_url = url
        self._current = str(radio_url)
        instance = vlc.Instance()
        player = instance.media_player_new()
        media = instance.media_new(radio_url)
        media_list = instance.media_list_new([radio_url])
        media.get_mrl()
        player.set_media(media)
        self._list_player = instance.media_list_player_new()
        self._list_player.set_media_list(media_list)
        self.text_input.text = str(url)
        self._list_player.play()

    def stop_player(self):
        self._list_player.stop()
        self.playfolder = False
        self.song_list = []

    def pause_player(self):
        self._list_player.pause()
        if self._paused is False:
            self._paused = True
        elif self._paused is True:
            self._paused = False
        else:
            assert False, (
                "This should not happen. Either the player is "
                "paused or not. This function is called when "
                "Pause / Resume is pressed"
            )

    def resume_player(self):
        self._paused = False

    def song_back(self):
        self._list_player.stop()
        song = self.songiter.__previous__()
        self._current = song
        self._list_player = vlc.MediaPlayer(song)
        self._list_player.play()

    def song_forward(self):
        self._list_player.stop()
        song = self.songiter.__next__()
        self._current = song
        self._list_player = vlc.MediaPlayer(song)
        self._list_player.play()

    def start_player(self):
        self._list_player = vlc.MediaPlayer()

    def play_folder(self):

        if self._paused is False:
            song = self.songiter.__next__()
            # self.song_list.pop()
            self._current = song
            self._list_player = vlc.MediaPlayer(song)
            self._list_player.play()

    def update(self, dt):
        if self.playfolder is True and self._list_player.is_playing() == 0:
            self.text_input.text = str(self._current)
            self.play_folder()
        elif self.playfolder is True and self._list_player.is_playing() == 1:
            self.text_input.text = str(self._current)
        elif self.playfolder is False:
            self.text_input.text = str(self._current)
        else:
            self.text_input.text = "Keine weiteren Lieder in der Playlist"


class Netzwerk(Screen):
    def change_vpn_de(self):
        output = check_output(["ssh", "admin@router", 
        "doas /home/admin/scripte/scripte_router/switch_vpn.sh", "is-de"]) 
        self.text_input.text = str(output.decode('UTF-8'))

    def change_vpn_at(self):
        output = check_output(["ssh", "admin@router", 
            "doas /home/admin/scripte/scripte_router/switch_vpn.sh", "ch-at"]) 
        self.text_input.text = str(output.decode('UTF-8'))

    def change_vpn_fr(self):
        output = check_output(["ssh", "admin@router",
       "doas /home/admin/scripte/scripte_router/switch_vpn.sh", "ch-fr"])
        self.text_input.text = str(output.decode('UTF-8'))

    def change_vpn_us(self):
        output = check_output(["ssh", "admin@router",
        "doas /home/admin/scripte/scripte_router/switch_vpn.sh", "is-us"])
        self.text_input.text = str(output.decode('UTF-8'))

    def ping_host(self, host):
        command = ['ping', '-c', '4', '-q', host]
        output = check_output(command)
        output_host = re.search(r'4 packets .*',output.decode('UTF-8'))
        package_loss = output_host.group(0).split(',')[2].strip().split('%')[0].strip()
        if package_loss == '0':
            out = 'erreichbar'
        elif package_loss == '100':
            out = 'nicht erreichbar'
        else:
            out = "langsame Verbindung"
 
        return out


    def check_connectivity(self):
        # Router
        host = '192.168.178.2.1'
        package_loss = self.ping_host(host)
        output = f"Router (router) {package_loss}\n"
        self.text_input.text = output
       # NAS
        host = '192.168.178.2.28'
        package_loss = self.ping_host(host)
        output = output + f"Nas (Nas) {package_loss}\n"
        self.text_input.text = output
        #Fritz Box
        host = '192.168.178.1'
        package_loss = self.ping_host(host)
        output = output + f"FritzBox (Router) {package_loss}\n"
        self.text_input.text = output
        # Internet (IP)
        host = '9.9.9.9'
        package_loss = self.ping_host(host)
        output = output + f"Internet {package_loss}\n"
        self.text_input.text = output
        # Internet (DNS)
        host = 'google.com'
        package_loss = self.ping_host(host)
        output = output + f"Internet (DNS) {package_loss}\n"
        self.text_input.text = output

        # Get IP + country
#        output = output + self.ip() + "\n"
#        output = output + self.country() + "\n"
#        self.text_input.text = output

    def refresh_log(self):
        output = check_output(["ssh", "admin@router", "/usr/bin/tail /var/log/messages"])
        self.text_input.text = str(output.decode('UTF-8'))


class Windowadmin(Screenadmin):
    pass


Builder.load_file("CustomStyles/FileIconEntry.kv")
kv = Builder.load_file("kessel.kv")


class KesselApp(App):
    def build(self):

        return kv


if __name__ == "__main__":
    if rpirpconfig.fullscreen is True:
        Window.fullscreen = "auto"
    KesselApp().run()
