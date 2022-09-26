#!/usr/bin/python
# -*- coding: utf-8 -*-

# This file was created using the DirectGUI Designer

from direct.gui import DirectGuiGlobals as DGG

from direct.gui.DirectFrame import DirectFrame
from direct.gui.DirectButton import DirectButton
from direct.gui.DirectEntry import DirectEntry
from direct.gui.DirectLabel import DirectLabel
from direct.gui.DirectOptionMenu import DirectOptionMenu
from panda3d.core import (
    LPoint3f,
    LVecBase3f,
    LVecBase4f,
    TextNode
)

class GUI:
    def __init__(self, rootParent=None):
        
        self.frmCreateProject = DirectFrame(
            borderWidth = (2, 2),
            frameSize = (-250.0, 250.0, -150.0, 150.0),
            frameColor = (1, 1, 1, 1),
            pos = LPoint3f(646.167, 0, -460),
            parent=rootParent,
        )
        self.frmCreateProject.setTransparency(0)

        self.btnOk = DirectButton(
            relief = 1,
            borderWidth = (2, 2),
            frameSize = (-50.0, 50.0, -10.0, 25.0),
            pos = LPoint3f(75, 0, -125),
            text = ['OK'],
            text0_scale = (24, 24),
            text1_scale = (24, 24),
            text2_scale = (24, 24),
            text3_scale = (24, 24),
            parent=self.frmCreateProject,
            pressEffect=1,
        )
        self.btnOk.setTransparency(0)

        self.btnCancel = DirectButton(
            relief = 1,
            borderWidth = (2, 2),
            frameSize = (-50.0, 50.0, -10.0, 25.0),
            pos = LPoint3f(190, 0, -125),
            text = ['Cancel'],
            text0_scale = (24, 24),
            text1_scale = (24, 24),
            text2_scale = (24, 24),
            text3_scale = (24, 24),
            parent=self.frmCreateProject,
            pressEffect=1,
        )
        self.btnCancel.setTransparency(0)

        self.txtName = DirectEntry(
            borderWidth = (0.08333333333333333, 0.08333333333333333),
            pos = LPoint3f(-125, 0, 100),
            scale = LVecBase3f(24, 24, 24),
            width = 15.0,
            parent=self.frmCreateProject,
        )
        self.txtName.setTransparency(0)

        self.lblName = DirectLabel(
            borderWidth = (2, 2),
            frameColor = (0.8, 0.8, 0.8, 0.0),
            pos = LPoint3f(-195, 0, 100),
            text = ['Name'],
            text0_scale = (24, 24),
            parent=self.frmCreateProject,
        )
        self.lblName.setTransparency(0)

        self.lblProjectType = DirectLabel(
            borderWidth = (2, 2),
            frameColor = (0.8, 0.8, 0.8, 0.0),
            pos = LPoint3f(-195, 0, 0),
            text = ['Type'],
            text0_scale = (24, 24),
            parent=self.frmCreateProject,
        )
        self.lblProjectType.setTransparency(0)

        self.lblProjectTemplate = DirectLabel(
            borderWidth = (2, 2),
            frameColor = (0.8, 0.8, 0.8, 0.0),
            pos = LPoint3f(-195, 0, -50),
            text = ['Template'],
            text0_scale = (24, 24),
            parent=self.frmCreateProject,
        )
        self.lblProjectTemplate.setTransparency(0)

        self.projectType = DirectOptionMenu(
            borderWidth = [0.0, 0.0],
            pos = LPoint3f(0, 0, 0),
            scale = LVecBase3f(24, 24, 24),
            items = ['FRAME'],
            popupMarker_pos = None,
            text_align = 0,
            parent=self.frmCreateProject,
        )
        self.projectType.setTransparency(0)

        self.template = DirectOptionMenu(
            borderWidth = [0.0, 0.0],
            pos = LPoint3f(0, 0, -50),
            scale = LVecBase3f(24, 24, 24),
            items = ['Simple'],
            popupMarker_pos = None,
            text_align = 0,
            parent=self.frmCreateProject,
        )
        self.template.setTransparency(0)

        self.lblCompany = DirectLabel(
            borderWidth = (2, 2),
            frameColor = (0.8, 0.8, 0.8, 0.0),
            pos = LPoint3f(-195, 0, 50),
            text = ['Company'],
            text0_scale = (24, 24),
            parent=self.frmCreateProject,
        )
        self.lblCompany.setTransparency(0)

        self.txtCompany = DirectEntry(
            borderWidth = (0.08333333333333333, 0.08333333333333333),
            pos = LPoint3f(-125, 0, 50),
            scale = LVecBase3f(24, 24, 24),
            width = 15.0,
            parent=self.frmCreateProject,
        )
        self.txtCompany.setTransparency(0)


    def show(self):
        self.frmCreateProject.show()

    def hide(self):
        self.frmCreateProject.hide()

    def destroy(self):
        self.frmCreateProject.destroy()
