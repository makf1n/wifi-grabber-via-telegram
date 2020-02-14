# Wifi
from lazagne.softwares.wifi.wifi import Wifi

def get_categories():
    return { 'wifi': {'help': 'Wifi'} }

def get_modules():
    return [ Wifi()]
