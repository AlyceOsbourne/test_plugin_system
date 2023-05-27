from framework import *
import logging
import logging.config
import io
import configparser

class Logger(PluginMixin):
    states = ("logger", "logger_handler")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.format = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        self.logger = logging.getLogger("root")
        self.logger.setLevel(logging.DEBUG)
        self.stream_io = io.StringIO()
        self.stream_handler = logging.StreamHandler(self.stream_io)
        self.stream_handler.setFormatter(self.format)
        self.logger.addHandler(self.stream_handler)
        self.logger_handler = self


class Config(PluginMixin):
    states = ("app_config",)

    def __init__(self):
        self.app_config = configparser.ConfigParser()
        self.app_config.read("./config/config.ini")


class Utils(PluginMixin):
    states = ("logger', 'app_config")
    requirements = ("Logger", "Config")
