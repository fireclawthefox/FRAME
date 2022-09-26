#!/usr/bin/python
__author__ = "Fireclaw the Fox"
__license__ = """
Simplified BSD (BSD 2-Clause) License.
See License.txt or http://opensource.org/licenses/BSD-2-Clause for more info
"""

# Panda3D imoprts
from direct.showbase.ShowBase import ShowBase
from direct.gui.DirectGui import DGG
from panda3d.core import (
    AntialiasAttrib,
    ConfigVariableBool)

# configuration handling
from client.core import config

# State handling
from client.core.coreFSM import CoreFSM

# import the client repository
from client.ClientRepository import GameClientRepository

#
# MAIN GAME CLASS
#
class Main(ShowBase, CoreFSM):
    """Main function of the application
    initialise the engine (ShowBase)"""

    def __init__(self):
        """initialise the engine"""
        ShowBase.__init__(self)
        base.notify.info(f"Version {config.versionstring}")
        CoreFSM.__init__(self, "FSM-Core")

        config.load_config()

        #
        # BASIC APPLICATION CONFIGURATIONS
        #
        # disable pandas default camera driver
        self.disableMouse()
        # set antialias for the complete sceen to automatic
        self.render.setAntialias(AntialiasAttrib.MAuto)
        # shader generator
        render.setShaderAuto()
        # Enhance font readability
        DGG.getDefaultFont().setPixelsPerUnit(100)

        #
        # CONFIGURATION LOADING
        #
        # load given variables or set defaults
        # check if particles should be enabled
        # NOTE: If you use the internal physics engine, this always has
        #       to be enabled!
        particles = ConfigVariableBool("particles-enabled", True).getValue()
        if particles:
            self.enableParticles()

        # automatically safe configuration at application exit
        base.exitFunc = config.write_config

        #
        # ENTER GAMES INITIAL FSM STATE
        #
        #TODO: Change this to any state you want the game to start with
        self.request("Main")

    def connectClient(self):
        """Create a connection between this client and the configured server"""

        # accept this event which will be thrown if we connected successfully
        self.accept("client-joined", self.clientJoined)

        # initialize the client
        client = GameClientRepository()

    def clientJoined(self):
        # TODO: Do the things you want to do when the client has successfully
        #       connected with the server, e.g. set up your avatar and world.
        pass
    #
    # BASIC END
    #
# CLASS Main END

#
# START GAME
#
Game = Main()
Game.run()

# start the client
base.run()
