"""
This is a setup.py script generated by py2applet

Usage:
    python setup.py py2app
"""

from setuptools import setup

APP = ['/Users/alexanderschober/Dropbox/RamanLISTSchober_v0.1.0/R-DATA.py']

DATA_FILES = ['/Users/alexanderschober/Dropbox/RamanLISTSchober_v0.1.0/INI_PARAMETERS.txt',
              '/Users/alexanderschober/Dropbox/RamanLISTSchober_v0.1.0/LISTalexanderschober_IN_PATH.txt',
              '/Users/alexanderschober/Dropbox/RamanLISTSchober_v0.1.0/LISTalexanderschober_OUT_PATH.txt',
              '/Users/alexanderschober/Dropbox/RamanLISTSchober_v0.1.0/DEFAULT_HELP_RESOURCES.txt',
              '/Users/alexanderschober/Dropbox/RamanLISTSchober_v0.1.0/DEFAULT_IO_RESOURCES.txt',
              '/Users/alexanderschober/Dropbox/RamanLISTSchober_v0.1.0/DEFAULT_MENUE_RESOURCES.txt',
              '/Users/alexanderschober/Dropbox/RamanLISTSchober_v0.1.0/LISTLogo.jpg',
              '/Users/alexanderschober/Dropbox/RamanLISTSchober_v0.1.0/LISTLogo.gif'
              ]

OPTIONS = {'argv_emulation': True}

setup(
    app=APP,
    version="0.1.0",
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
