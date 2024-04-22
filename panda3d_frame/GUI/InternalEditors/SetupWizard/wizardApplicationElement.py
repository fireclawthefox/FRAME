#!/usr/bin/python
# -*- coding: utf-8 -*-

# This file was created using the DirectGUI Designer

from direct.gui import DirectGuiGlobals as DGG

from direct.gui.DirectEntry import DirectEntry
from direct.gui.DirectButton import DirectButton
from direct.gui.DirectCheckButton import DirectCheckButton
from panda3d.core import (
    LPoint3f,
    LVecBase3f,
    LVecBase4f,
    TextNode
)

class GUI:
    def __init__(self, rootParent=None):
        
        self.txtName = DirectEntry(
            borderWidth=(0.167, 0.167),
            hpr=LVecBase3f(0, 0, 0),
            overflow=1,
            pos=LPoint3f(-213, 0, -13.85),
            scale=LVecBase3f(12, 12, 12),
            text_align=TextNode.A_left,
            text_scale=(1, 1),
            text_pos=(0, 0),
            text_fg=LVecBase4f(0, 0, 0, 1),
            text_bg=LVecBase4f(0, 0, 0, 0),
            parent=rootParent,
        )

        self.txtPath = DirectEntry(
            borderWidth=(0.167, 0.167),
            hpr=LVecBase3f(0, 0, 0),
            overflow=1,
            pos=LPoint3f(-87.5, 0, -13.85),
            scale=LVecBase3f(12, 12, 12),
            width=16.0,
            text_align=TextNode.A_left,
            text_scale=(1, 1),
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

        self.cbTerminalApp = DirectCheckButton(
            borderWidth=(2, 2),
            hpr=LVecBase3f(0, 0, 0),
            pos=LPoint3f(126, 0, -10),
            scale=LVecBase3f(0.7, 0.7, 0.7),
            text='',
            indicator_borderWidth=(2, 2),
            indicator_hpr=LVecBase3f(0, 0, 0),
            indicator_pos=LPoint3f(-11, 0, -7.2),
            indicator_relief='sunken',
            indicator_text_align=TextNode.A_center,
            indicator_text_scale=(24, 24),
            indicator_text_pos=(0, -0.2),
            indicator_text_fg=LVecBase4f(0, 0, 0, 1),
            indicator_text_bg=LVecBase4f(0, 0, 0, 0),
            text_align=TextNode.A_center,
            text_scale=(24.0, 24.0),
            text_pos=(0, 0),
            text_fg=LVecBase4f(0, 0, 0, 1),
            text_bg=LVecBase4f(0, 0, 0, 0),
            parent=rootParent,
        )

