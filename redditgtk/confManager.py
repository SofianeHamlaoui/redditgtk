# from gettext import gettext as _
from pathlib import Path
from os.path import isfile, isdir
from os import environ as Env
from os import makedirs
import json
from gi.repository import GObject
from redditgtk.singleton import Singleton


class ConfManagerSignaler(GObject.Object):

    __gsignals__ = {
        'dark_mode_changed': (
            GObject.SignalFlags.RUN_FIRST,
            None,
            (str,)
        )
    }


class ConfManager(metaclass=Singleton):

    BASE_SCHEMA = {
        'windowsize': {
            'width': 350,
            'height': 650
        },
        'dark_mode': False,
        'refresh_token': ''
    }

    def __init__(self):
        self.window = None
        self.signaler = ConfManagerSignaler()
        self.emit = self.signaler.emit
        self.connect = self.signaler.connect

        # check if inside flatpak sandbox
        self.is_flatpak = (
            'XDG_RUNTIME_DIR' in Env.keys() and
            isfile(f'{Env["XDG_RUNTIME_DIR"]}/flatpak-info')
        )

        if self.is_flatpak:
            self.path = Path(
                f'{Env.get("XDG_CONFIG_HOME")}/org.gabmus.redditgtk.json'
            )
            self.cache_path = Path(
                f'{Env.get("XDG_CACHE_HOME")}/org.gabmus.redditgtk'
            )
        else:
            self.path = Path(
                f'{Env.get("HOME")}/.config/org.gabmus.redditgtk.json'
            )
            self.cache_path = Path(
                f'{Env.get("HOME")}/.cache/org.gabmus.redditgtk'
            )

        self.conf = None
        if isfile(str(self.path)):
            try:
                with open(str(self.path)) as fd:
                    self.conf = json.loads(fd.read())
                # verify that the file has all of the schema keys
                for k in ConfManager.BASE_SCHEMA:
                    if k not in self.conf.keys():
                        if isinstance(
                                ConfManager.BASE_SCHEMA[k], (list, dict)
                        ):
                            self.conf[k] = ConfManager.BASE_SCHEMA[k].copy()
                        else:
                            self.conf[k] = ConfManager.BASE_SCHEMA[k]
            except Exception:
                self.conf = ConfManager.BASE_SCHEMA.copy()
                self.save_conf()
        else:
            self.conf = ConfManager.BASE_SCHEMA.copy()
            self.save_conf()

        if not isdir(self.cache_path):
            makedirs(self.cache_path)

    def save_conf(self, *args):
        with open(str(self.path), 'w') as fd:
            fd.write(json.dumps(self.conf))
