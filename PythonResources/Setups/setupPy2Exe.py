"""
This is a setup.py script generated by py2applet

Usage:
    python setup.py py2app
"""

from distutils.core import setup
import py2exe

APP = ['C:\\Users/Lux/Dropbox/RamanLISTSchober_v0.1.0/R-DATA.py']

DATA_FILES = ['C:\\Users/Lux/Dropbox/RamanLISTSchober_v0.1.0/INI_PARAMETERS.txt',
              'C:\\Users/Lux/Dropbox/RamanLISTSchober_v0.1.0/LISTLUX_IN_PATH.txt',
              'C:\\Users/Lux/Dropbox/RamanLISTSchober_v0.1.0/LISTLUX_OUT_PATH.txt',
              'C:\\Users/Lux/Dropbox/RamanLISTSchober_v0.1.0/DEFAULT_HELP_RESOURCES.txt',
              'C:\\Users/Lux/Dropbox/RamanLISTSchober_v0.1.0/DEFAULT_IO_RESOURCES.txt',
              'C:\\Users/Lux/Dropbox/RamanLISTSchober_v0.1.0/DEFAULT_MENUE_RESOURCES.txt',
              'C:\\Users/Lux/Dropbox/RamanLISTSchober_v0.1.0/LISTLogo.jpg',
              'C:\\Users/Lux/Dropbox/RamanLISTSchober_v0.1.0/LISTLogo.gif'
              ]


setup(
    windows = APP,
    version='0.1.0',
    data_files=DATA_FILES
)
