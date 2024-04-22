#!/usr/bin/python
# -*- coding: utf-8 -*-

# This file was created using the DirectGUI Designer

from direct.gui import DirectGuiGlobals as DGG

from direct.gui.DirectEntry import DirectEntry
from direct.gui.DirectButton import DirectButton
from panda3d.core import (
    LPoint3f,
    LVecBase3f,
    LVecBase4f,
    TextNode
)

class GUI:
    def __init__(self, rootParent=None):

        self.txtPattern = DirectEntry(
            borderWidth=(0.1666, 0.1666),
            hpr=LVecBase3f(0, 0, 0),
            overflow=1,
            pos=LPoint3f(-213, 0, -13.85),
            scale=LVecBase3f(12, 12, 12),
            width=28.5,
            text_align=TextNode.A_left,
            text_scale=(1.0, 1.0),
            text_pos=(0, 0),
            text_fg=LVecBase4f(0, 0, 0, 1),
            text_bg=LVecBase4f(0, 0, 0, 0),
            parent=rootParent,
        )

        self.btnRemove = DirectButton(
            borderWidth=(2, 2),
            hpr=LVecBase3f(0, 0, 0),
            pad=(5.0, 7.0),
            pos=LPoint3f(156.65, 0, -12.55),
            scale=LVecBase3f(0.5, 0.5, 0.5),
            text='Remove',
            text_align=TextNode.A_center,
            text_scale=(24, 24),
            text_pos=(0, 0),
            text_fg=LVecBase4f(0, 0, 0, 1),
            text_bg=LVecBase4f(0, 0, 0, 0),
            parent=rootParent,
        )

