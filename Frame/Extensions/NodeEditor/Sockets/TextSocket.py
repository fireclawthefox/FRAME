#!/usr/bin/python
# -*- coding: utf-8 -*-

# This file was created using the DirectGUI Designer

from Panda3DNodeEditor.NodeCore.Sockets.SocketBase import SocketBase, INSOCKET

from direct.gui.DirectFrame import DirectFrame
from direct.gui.DirectLabel import DirectLabel
from direct.gui.DirectEntry import DirectEntry
from direct.gui import DirectGuiGlobals as DGG
from panda3d.core import TextNode

class TextSocket(SocketBase):
    def __init__(self, node, name):
        SocketBase.__init__(self, node, name)

        self.height = 0.21

        self.type = INSOCKET

        self.frame = DirectFrame(
            frameColor=(0.25, 0.25, 0.25, 1),
            frameSize=(-1, 0, -self.height, 0),
            parent=node.frame,
        )

        SocketBase.createPlug(self, self.frame)

        self.text = DirectLabel(
            frameColor=(0, 0, 0, 0),
            frameSize=(0, 1, -self.height, 0),
            scale=(1, 1, 1),
            text=self.name,
            text_align=TextNode.A_left,
            text_scale=(0.1, 0.1),
            text_pos=(0.1, -0.02),
            text_fg=(1, 1, 1, 1),
            text_bg=(0, 0, 0, 0),
            parent=self.frame,
        )

        self.textfield = DirectEntry(
            pos=(0.5,0,-0.01),
            borderWidth=(0.1,0.1),
            width=10,
            parent=self.frame,
            command=self.updateConnectedNodes,
            focusOutCommand=self.updateConnectedNodes,
            overflow=True,
            state=DGG.DISABLED)
        self.textfield.setScale(0.1)

        self.resize(1.7)

    def disable(self):
        self.textfield["state"] = DGG.DISABLED

    def enable(self):
        if not self.connected:
            self.textfield["state"] = DGG.NORMAL

    def setValue(self, value):
        textAsString = ""
        try:
            textAsString = str(value)
        except:
            logging.error("couldn't convert node input value to string")
            return
        self.textfield.enterText(textAsString)

    def getValue(self):
        return self.textfield.get()

    def show(self, z, left):
        self.frame.setZ(z)
        self.frame.setX(left)

    def resize(self, newWidth):
        self.frame["frameSize"] = (0, newWidth, -self.height/2, self.height/2)
        self.text["frameSize"] = (0, newWidth, -self.height/2, self.height/2)

    def setConnected(self, connected):
        if connected:
            self.textfield["state"] = DGG.DISABLED
        else:
            self.textfield["state"] = DGG.NORMAL
        self.connected = connected
