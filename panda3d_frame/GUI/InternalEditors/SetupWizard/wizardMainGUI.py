#!/usr/bin/python
# -*- coding: utf-8 -*-

# This file was created using the DirectGUI Designer

from direct.gui import DirectGuiGlobals as DGG

from direct.gui.DirectButton import DirectButton
from direct.gui.DirectLabel import DirectLabel
from direct.gui.DirectFrame import DirectFrame
from direct.gui.DirectEntry import DirectEntry
from direct.gui.DirectCheckButton import DirectCheckButton
from direct.gui.DirectScrolledFrame import DirectScrolledFrame
from direct.gui.DirectRadioButton import DirectRadioButton
from panda3d.core import (
    LPoint3f,
    LVecBase3f,
    LVecBase4f,
    TextNode
)
from DirectGuiExtension.DirectAutoSizer import DirectAutoSizer
from DirectGuiExtension.DirectBoxSizer import DirectBoxSizer
from DirectGuiExtension.DirectTabbedFrame import DirectTabbedFrame

class GUI:
    def __init__(self, rootParent=None):
        color = (
            (0.8, 0.8, 0.8, 1),  # Normal
            (0.9, 0.9, 1, 1),  # Click
            (0.8, 0.8, 1, 1),  # Hover
            (0.5, 0.5, 0.5, 1))  # Disabled
        colorSpecial = (
            (0.2, 0.9, 0.2, 1.0),  # Normal
            (0.3, 1.0, 0.3, 1.0),  # Click
            (0.1, 0.8, 0.1, 1.0),  # Hover
            (0.5, 0.5, 0.5, 1))  # Disabled
        tab_frame_z_pos = -255

        self.main_sizer = DirectAutoSizer(rootParent)

        self.content_box = DirectBoxSizer(
            frameSize=(0,1060,-100,0),
            autoUpdateFrameSize=False,
            #frameColor=(1,0,0,1),
            orientation=DGG.VERTICAL,
            itemAlign=DirectBoxSizer.A_Left|DirectBoxSizer.A_Top
            )

        self.main_sizer.setChild(self.content_box)

        self.lblHeader = DirectLabel(
            pad=(5, 5),
            frameColor=(0.25, 0.25, 0.25, 1.0),
            text='Panda3D Setup Creation Wizard',
            text_align=TextNode.A_left,
            text_scale=(24, 24),
            text_fg=LVecBase4f(1, 1, 1, 1),
            text_bg=LVecBase4f(0.25, 0.25, 0.25, 1),
        )
        self.header_sizer = DirectAutoSizer(
            self.content_box,
            self.lblHeader,
            extendVertical=False)
        self.content_box.addItem(self.header_sizer)

        #
        # Toolbar
        #
        self.toolBar = DirectBoxSizer(
            frameColor=(0.25, 0.25, 0.25, 1),
            frameSize=(0,1,-24, 24),
            pos=(0, 0, 0),
            parent=base.pixel2d)

        self.toolbar_sizer = DirectAutoSizer(
            self.content_box,
            self.toolBar,
            extendVertical=False)
        self.content_box.addItem(self.toolbar_sizer)

        self.btnLoad = DirectButton(
            #borderWidth=(2, 2),
            frameSize=(-80.0, 80.0, -24, 24),
            frameColor=color,
            #hpr=LVecBase3f(0, 0, 0),
            #pos=LPoint3f(375, 0, -445),
            #scale=LVecBase3f(1, 1, 1),
            text='Load\nConfig',
            #text_align=TextNode.A_center,
            text_scale=18,
            #text_pos=(0.0, 4.0),
            #text_fg=LVecBase4f(0, 0, 0, 1),
            #text_bg=LVecBase4f(0, 0, 0, 0),
            command=base.messenger.send,
            extraArgs=["p3d_setup_wizard_load"],
        )
        self.toolBar.addItem(self.btnLoad)

        self.btnSave = DirectButton(
            #borderWidth=(2, 2),
            frameSize=(-80.0, 80.0, -24, 24),
            frameColor=color,
            #hpr=LVecBase3f(0, 0, 0),
            #pos=LPoint3f(125, 0, -445),
            #scale=LVecBase3f(1, 1, 1),
            text='Save\nConfig',
            #text_align=TextNode.A_center,
            text_scale=18,
            #text_pos=(0.0, 4.0),
            #text_fg=LVecBase4f(0, 0, 0, 1),
            #text_bg=LVecBase4f(0, 0, 0, 0),
            command=base.messenger.send,
            extraArgs=["p3d_setup_wizard_save"],
        )
        self.toolBar.addItem(self.btnSave)

        self.btnDeploy = DirectButton(
            #borderWidth=(2, 2),
            frameSize=(-80.0, 80.0, -24, 24),
            frameColor=colorSpecial,
            #hpr=LVecBase3f(0, 0, 0),
            #pos=LPoint3f(250, 0, -470),
            #scale=LVecBase3f(1, 1, 1),
            text='Deploy',
            #text_align=TextNode.A_center,
            text_scale=18,
            #text_pos=(0.0, 3.0),
            #text_fg=LVecBase4f(0, 0, 0, 1),
            #text_bg=LVecBase4f(0, 0, 0, 0),
            command=base.messenger.send,
            extraArgs=["p3d_setup_wizard_deploy"],
        )
        self.toolBar.addItem(self.btnDeploy)

        self.tabbedFrame = DirectTabbedFrame(
            showCloseOnTabs=False,
            tabHeight=18,
            frameSize=(-500,500,-self.content_box.getRemainingSpace(),0)
        )
        self.tabbedFrame_sizer = DirectAutoSizer(
            self.content_box,
            self.tabbedFrame,
            extendVertical=False)
        self.content_box.addItem(self.tabbedFrame_sizer)

        self.frmMetadata = DirectFrame(
            borderWidth=(2, 2),
            frameColor=(1, 1, 1, 1),
            frameSize=(-250.0, 250.0, -180.0, 150.0),
            hpr=LVecBase3f(0, 0, 0),
            pos=LPoint3f(250.0, 0, tab_frame_z_pos),
            relief=3,
            parent=rootParent,
        )
        self.frmMetadata.setTransparency(0)

        self.lblAppName = DirectLabel(
            borderWidth=(2, 2),
            frameColor=(0.0, 0.0, 0.0, 0.0),
            hpr=LVecBase3f(0, 0, 0),
            pos=LPoint3f(-140, 0, 70),
            scale=LVecBase3f(1, 1, 1),
            text='Application Name',
            text_align=TextNode.A_center,
            text_scale=(12.0, 12.0),
            text_pos=(0, 0),
            text_fg=LVecBase4f(0, 0, 0, 1),
            text_bg=LVecBase4f(0, 0, 0, 0),
            parent=self.frmMetadata,
        )
        self.lblAppName.setTransparency(0)

        self.txtAppName = DirectEntry(
            borderWidth=(0.1666, 0.166),
            hpr=LVecBase3f(0, 0, 0),
            overflow=1,
            pos=LPoint3f(-60, 0, 70),
            scale=LVecBase3f(12, 12, 12),
            width=20.0,
            text_align=TextNode.A_left,
            text_scale=(1.0, 1.0),
            text_pos=(0, 0),
            text_fg=LVecBase4f(0, 0, 0, 1),
            text_bg=LVecBase4f(0, 0, 0, 0),
            parent=self.frmMetadata,
        )
        self.txtAppName.setTransparency(0)

        self.lblMetadata = DirectLabel(
            borderWidth=(2, 2),
            frameColor=(0.0, 0.0, 0.0, 0.0),
            hpr=LVecBase3f(0, 0, 0),
            pos=LPoint3f(0, 0, 110),
            scale=LVecBase3f(1, 1, 1),
            text='Metadata',
            text_align=TextNode.A_center,
            text_scale=(12.0, 12.0),
            text_pos=(0, 0),
            text_fg=LVecBase4f(0, 0, 0, 1),
            text_bg=LVecBase4f(0, 0, 0, 0),
            parent=self.frmMetadata,
        )
        self.lblMetadata.setTransparency(0)

        self.lblAuthor = DirectLabel(
            borderWidth=(2, 2),
            frameColor=(0.0, 0.0, 0.0, 0.0),
            hpr=LVecBase3f(0, 0, 0),
            pos=LPoint3f(-140, 0, 40),
            scale=LVecBase3f(1, 1, 1),
            text='Author',
            text_align=TextNode.A_center,
            text_scale=(12.0, 12.0),
            text_pos=(0, 0),
            text_fg=LVecBase4f(0, 0, 0, 1),
            text_bg=LVecBase4f(0, 0, 0, 0),
            parent=self.frmMetadata,
        )
        self.lblAuthor.setTransparency(0)

        self.txtAuthor = DirectEntry(
            borderWidth=(0.1666, 0.1666),
            hpr=LVecBase3f(0, 0, 0),
            overflow=1,
            pos=LPoint3f(-60, 0, 40),
            scale=LVecBase3f(12, 12, 12),
            width=20.0,
            text_align=TextNode.A_left,
            text_scale=(1.0, 1.0),
            text_pos=(0, 0),
            text_fg=LVecBase4f(0, 0, 0, 1),
            text_bg=LVecBase4f(0, 0, 0, 0),
            parent=self.frmMetadata,
        )
        self.txtAuthor.setTransparency(0)

        self.txtVersion = DirectEntry(
            borderWidth=(0.167, 0.167),
            hpr=LVecBase3f(0, 0, 0),
            overflow=1,
            pos=LPoint3f(-60, 0, 10),
            scale=LVecBase3f(12, 12, 12),
            width=20.0,
            text_align=TextNode.A_left,
            text_scale=(1, 1),
            text_pos=(0, 0),
            text_fg=LVecBase4f(0, 0, 0, 1),
            text_bg=LVecBase4f(0, 0, 0, 0),
            parent=self.frmMetadata,
        )
        self.txtVersion.setTransparency(0)

        self.lblVersion = DirectLabel(
            borderWidth=(2, 2),
            frameColor=(0.8, 0.8, 0.8, 0.0),
            hpr=LVecBase3f(0, 0, 0),
            pos=LPoint3f(-140, 0, 10),
            scale=LVecBase3f(1, 1, 1),
            text='Version',
            text_align=TextNode.A_center,
            text_scale=(12.0, 12.0),
            text_pos=(0, 0),
            text_fg=LVecBase4f(0, 0, 0, 1),
            text_bg=LVecBase4f(0, 0, 0, 0),
            parent=self.frmMetadata,
        )
        self.lblVersion.setTransparency(0)

        self.tabbedFrame.add_tab("Metadata", self.frmMetadata)

        self.frmPlatforms = DirectFrame(
            borderWidth=(2, 2),
            frameColor=(1, 1, 1, 1),
            frameSize=(-250.0, 250.0, -180.0, 150.0),
            hpr=LVecBase3f(0, 0, 0),
            pos=LPoint3f(250.0, 0, tab_frame_z_pos),
            relief=3,
            parent=rootParent,
        )
        self.frmPlatforms.setTransparency(0)

        self.lblPlatforms = DirectLabel(
            borderWidth=(2, 2),
            frameColor=(0.0, 0.0, 0.0, 0.0),
            hpr=LVecBase3f(0, 0, 0),
            pos=LPoint3f(0, 0, 110),
            scale=LVecBase3f(1, 1, 1),
            text='Supported Platforms',
            text_align=TextNode.A_center,
            text_scale=(12.0, 12.0),
            text_pos=(0, 0),
            text_fg=LVecBase4f(0, 0, 0, 1),
            text_bg=LVecBase4f(0, 0, 0, 0),
            parent=self.frmPlatforms,
        )
        self.lblPlatforms.setTransparency(0)

        self.cbLinux = DirectCheckButton(
            borderWidth=(0.0, 0.0),
            frameSize=(-250.0, 250.0, -12.25, 27.55),
            hpr=LVecBase3f(0, 0, 0),
            indicatorValue=1,
            pos=LPoint3f(0, 0, 65),
            scale=LVecBase3f(0.5, 0.5, 0.5),
            text='Linux',
            indicator_borderWidth=(2, 2),
            indicator_hpr=LVecBase3f(0, 0, 0),
            indicator_pos=LPoint3f(-241.4, 0, 0.450001),
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
            parent=self.frmPlatforms,
        )
        self.cbLinux.setTransparency(0)

        self.cbMacOS = DirectCheckButton(
            borderWidth=(0.0, 0.0),
            frameSize=(-250.0, 250.0, -12.25, 27.55),
            hpr=LVecBase3f(0, 0, 0),
            indicatorValue=1,
            pos=LPoint3f(0, 0, 35),
            scale=LVecBase3f(0.5, 0.5, 0.5),
            text='MacOS',
            indicator_borderWidth=(2, 2),
            indicator_hpr=LVecBase3f(0, 0, 0),
            indicator_pos=LPoint3f(-241.4, 0, 0.450001),
            indicator_relief='sunken',
            indicator_text_align=TextNode.A_center,
            indicator_text_scale=(24, 24),
            indicator_text_pos=(0, -0.2),
            indicator_text_fg=LVecBase4f(0, 0, 0, 1),
            indicator_text_bg=LVecBase4f(0, 0, 0, 0),
            text_align=TextNode.A_center,
            text_scale=(24, 24),
            text_pos=(0, 0),
            text_fg=LVecBase4f(0, 0, 0, 1),
            text_bg=LVecBase4f(0, 0, 0, 0),
            parent=self.frmPlatforms,
        )
        self.cbMacOS.setTransparency(0)

        self.cbWindows = DirectCheckButton(
            borderWidth=(0.0, 0.0),
            frameSize=(-250.0, 250.0, -12.25, 27.55),
            hpr=LVecBase3f(0, 0, 0),
            indicatorValue=1,
            pos=LPoint3f(0, 0, 5),
            scale=LVecBase3f(0.5, 0.5, 0.5),
            text='Windows',
            indicator_borderWidth=(2, 2),
            indicator_hpr=LVecBase3f(0, 0, 0),
            indicator_pos=LPoint3f(-241.4, 0, 0.450001),
            indicator_relief='sunken',
            indicator_text_align=TextNode.A_center,
            indicator_text_scale=(24, 24),
            indicator_text_pos=(0, -0.2),
            indicator_text_fg=LVecBase4f(0, 0, 0, 1),
            indicator_text_bg=LVecBase4f(0, 0, 0, 0),
            text_align=TextNode.A_center,
            text_scale=(24, 24),
            text_pos=(0, 0),
            text_fg=LVecBase4f(0, 0, 0, 1),
            text_bg=LVecBase4f(0, 0, 0, 0),
            parent=self.frmPlatforms,
        )
        self.cbWindows.setTransparency(0)

        self.cbAndroid = DirectCheckButton(
            borderWidth=(0.0, 0.0),
            frameSize=(-250.0, 250.0, -12.25, 27.55),
            hpr=LVecBase3f(0, 0, 0),
            pos=LPoint3f(0, 0, -70),
            scale=LVecBase3f(0.5, 0.5, 0.5),
            text='Android',
            indicator_borderWidth=(2, 2),
            indicator_hpr=LVecBase3f(0, 0, 0),
            indicator_pos=LPoint3f(-241.4, 0, 0.450001),
            indicator_relief='sunken',
            indicator_text_align=TextNode.A_center,
            indicator_text_scale=(24, 24),
            indicator_text_pos=(0, -0.2),
            indicator_text_fg=LVecBase4f(0, 0, 0, 1),
            indicator_text_bg=LVecBase4f(0, 0, 0, 0),
            text_align=TextNode.A_center,
            text_scale=(24, 24),
            text_pos=(0, 0),
            text_fg=LVecBase4f(0, 0, 0, 1),
            text_bg=LVecBase4f(0, 0, 0, 0),
            parent=self.frmPlatforms,
        )
        self.cbAndroid.setTransparency(0)

        self.lblDesktop = DirectLabel(
            borderWidth=(2, 2),
            frameColor=(0.0, 0.0, 0.0, 0.0),
            hpr=LVecBase3f(0, 0, 0),
            pos=LPoint3f(0, 0, 90),
            scale=LVecBase3f(1, 1, 1),
            text='Desktop',
            text_align=TextNode.A_center,
            text_scale=(12.0, 12.0),
            text_pos=(0, 0),
            text_fg=LVecBase4f(0, 0, 0, 1),
            text_bg=LVecBase4f(0, 0, 0, 0),
            parent=self.frmPlatforms,
        )
        self.lblDesktop.setTransparency(0)

        self.lblMobile = DirectLabel(
            borderWidth=(2, 2),
            frameColor=(0.0, 0.0, 0.0, 0.0),
            hpr=LVecBase3f(0, 0, 0),
            pos=LPoint3f(0, 0, -50),
            scale=LVecBase3f(1, 1, 1),
            text='Mobile',
            text_align=TextNode.A_center,
            text_scale=(12.0, 12.0),
            text_pos=(0, 0),
            text_fg=LVecBase4f(0, 0, 0, 1),
            text_bg=LVecBase4f(0, 0, 0, 0),
            parent=self.frmPlatforms,
        )
        self.lblMobile.setTransparency(0)

        self.tabbedFrame.add_tab("Platforms", self.frmPlatforms)

        self.frmPlugins = DirectFrame(
            borderWidth=(2, 2),
            frameColor=(1, 1, 1, 1),
            frameSize=(-250.0, 250.0, -180.0, 150.0),
            hpr=LVecBase3f(0, 0, 0),
            pos=LPoint3f(250.0, 0, tab_frame_z_pos),
            relief=3,
            parent=rootParent,
        )
        self.frmPlugins.setTransparency(0)

        self.lblPlugins = DirectLabel(
            borderWidth=(2, 2),
            frameColor=(0.0, 0.0, 0.0, 0.0),
            hpr=LVecBase3f(0, 0, 0),
            pos=LPoint3f(0, 0, 110),
            scale=LVecBase3f(1, 1, 1),
            text='Plugins',
            text_align=TextNode.A_center,
            text_scale=(12.0, 12.0),
            text_pos=(0, 0),
            text_fg=LVecBase4f(0, 0, 0, 1),
            text_bg=LVecBase4f(0, 0, 0, 0),
            parent=self.frmPlugins,
        )
        self.lblPlugins.setTransparency(0)

        self.frmPluginSelection = DirectScrolledFrame(
            canvasSize=(-215.0, 215.0, -300.0, 0.0),
            frameColor=(1, 1, 1, 1),
            frameSize=(-225.0, 225.0, -240.0, 0.0),
            hpr=LVecBase3f(0, 0, 0),
            pos=LPoint3f(0, 0, 80),
            scrollBarWidth=20,
            state='normal',
            horizontalScroll_borderWidth=(2, 2),
            horizontalScroll_frameSize=(-0.05, 0.05, -10.0, 10.0),
            horizontalScroll_hpr=LVecBase3f(0, 0, 0),
            horizontalScroll_pos=LPoint3f(0, 0, 0),
            horizontalScroll_decButton_borderWidth=(2, 2),
            horizontalScroll_decButton_frameSize=(-0.05, 0.05, -10.0, 10.0),
            horizontalScroll_decButton_hpr=LVecBase3f(0, 0, 0),
            horizontalScroll_decButton_pos=LPoint3f(0, 0, 0),
            horizontalScroll_incButton_borderWidth=(2, 2),
            horizontalScroll_incButton_frameSize=(-0.05, 0.05, -10.0, 10.0),
            horizontalScroll_incButton_hpr=LVecBase3f(0, 0, 0),
            horizontalScroll_incButton_pos=LPoint3f(0, 0, 0),
            horizontalScroll_thumb_borderWidth=(2, 2),
            horizontalScroll_thumb_hpr=LVecBase3f(0, 0, 0),
            horizontalScroll_thumb_pos=LPoint3f(0, 0, 0),
            verticalScroll_borderWidth=(2, 2),
            verticalScroll_frameSize=(-10.0, 10.0, -0.05, 0.05),
            verticalScroll_hpr=LVecBase3f(0, 0, 0),
            verticalScroll_pos=LPoint3f(0, 0, 0),
            verticalScroll_decButton_borderWidth=(2, 2),
            verticalScroll_decButton_frameSize=(-10.0, 10.0, -0.05, 0.05),
            verticalScroll_decButton_hpr=LVecBase3f(0, 0, 0),
            verticalScroll_decButton_pos=LPoint3f(215, 0, -10),
            verticalScroll_incButton_borderWidth=(2, 2),
            verticalScroll_incButton_frameSize=(-10.0, 10.0, -0.05, 0.05),
            verticalScroll_incButton_hpr=LVecBase3f(0, 0, 0),
            verticalScroll_incButton_pos=LPoint3f(215, 0, -230),
            verticalScroll_thumb_borderWidth=(2, 2),
            verticalScroll_thumb_hpr=LVecBase3f(0, 0, 0),
            verticalScroll_thumb_pos=LPoint3f(215, 0, -100),
            parent=self.frmPlugins,
        )
        self.frmPluginSelection.setTransparency(0)

        self.tabbedFrame.add_tab("Plugins", self.frmPlugins)

        self.frmApplications = DirectFrame(
            borderWidth=(2.0, 2.0),
            frameColor=(1, 1, 1, 1),
            frameSize=(-250.0, 250.0, -180.0, 150.0),
            hpr=LVecBase3f(0, 0, 0),
            pos=LPoint3f(250.0, 0, tab_frame_z_pos),
            relief=3,
            parent=rootParent,
        )
        self.frmApplications.setTransparency(0)

        self.lblApplication = DirectLabel(
            borderWidth=(2, 2),
            frameColor=(0.0, 0.0, 0.0, 0.0),
            hpr=LVecBase3f(0, 0, 0),
            pos=LPoint3f(0, 0, 110),
            scale=LVecBase3f(1, 1, 1),
            text='Applications',
            text_align=TextNode.A_center,
            text_scale=(12.0, 12.0),
            text_pos=(0, 0),
            text_fg=LVecBase4f(0, 0, 0, 1),
            text_bg=LVecBase4f(0, 0, 0, 0),
            parent=self.frmApplications,
        )
        self.lblApplication.setTransparency(0)

        self.btnAddApplication = DirectButton(
            borderWidth=(2, 2),
            frameSize=(-250.0, 250.0, -12.25, 27.55),
            hpr=LVecBase3f(0, 0, 0),
            pos=LPoint3f(0, 0, 70),
            scale=LVecBase3f(0.5, 0.5, 0.5),
            text='Add Application',
            text_align=TextNode.A_center,
            text_scale=(24, 24),
            text_pos=(0, 0),
            text_fg=LVecBase4f(0, 0, 0, 1),
            text_bg=LVecBase4f(0, 0, 0, 0),
            parent=self.frmApplications,
            command=base.messenger.send,
            extraArgs=["p3d_setup_wizard_addApplication"],
        )
        self.btnAddApplication.setTransparency(0)

        self.frmApplicationSelection = DirectScrolledFrame(
            canvasSize=(-215.0, 215.0, -300.0, 0.0),
            frameColor=(1.0, 1.0, 1.0, 1.0),
            frameSize=(-225.0, 225.0, -200.0, 0.0),
            hpr=LVecBase3f(0, 0, 0),
            pos=LPoint3f(0, 0, 40),
            scrollBarWidth=20,
            state='normal',
            horizontalScroll_borderWidth=(2, 2),
            horizontalScroll_frameSize=(-0.05, 0.05, -10.0, 10.0),
            horizontalScroll_hpr=LVecBase3f(0, 0, 0),
            horizontalScroll_pos=LPoint3f(0, 0, 0),
            horizontalScroll_decButton_borderWidth=(2, 2),
            horizontalScroll_decButton_frameSize=(-0.05, 0.05, -10.0, 10.0),
            horizontalScroll_decButton_hpr=LVecBase3f(0, 0, 0),
            horizontalScroll_decButton_pos=LPoint3f(0, 0, 0),
            horizontalScroll_incButton_borderWidth=(2, 2),
            horizontalScroll_incButton_frameSize=(-0.05, 0.05, -10.0, 10.0),
            horizontalScroll_incButton_hpr=LVecBase3f(0, 0, 0),
            horizontalScroll_incButton_pos=LPoint3f(0, 0, 0),
            horizontalScroll_thumb_borderWidth=(2, 2),
            horizontalScroll_thumb_hpr=LVecBase3f(0, 0, 0),
            horizontalScroll_thumb_pos=LPoint3f(0, 0, 0),
            verticalScroll_borderWidth=(2, 2),
            verticalScroll_frameSize=(-10.0, 10.0, -0.05, 0.05),
            verticalScroll_hpr=LVecBase3f(0, 0, 0),
            verticalScroll_pos=LPoint3f(0, 0, 0),
            verticalScroll_decButton_borderWidth=(2, 2),
            verticalScroll_decButton_frameSize=(-10.0, 10.0, -0.05, 0.05),
            verticalScroll_decButton_hpr=LVecBase3f(0, 0, 0),
            verticalScroll_decButton_pos=LPoint3f(215, 0, -10),
            verticalScroll_incButton_borderWidth=(2, 2),
            verticalScroll_incButton_frameSize=(-10.0, 10.0, -0.05, 0.05),
            verticalScroll_incButton_hpr=LVecBase3f(0, 0, 0),
            verticalScroll_incButton_pos=LPoint3f(215, 0, -190),
            verticalScroll_thumb_borderWidth=(2, 2),
            verticalScroll_thumb_hpr=LVecBase3f(0, 0, 0),
            verticalScroll_thumb_pos=LPoint3f(215, 0, -73.3333),
            parent=self.frmApplications,
        )
        self.frmApplicationSelection.setTransparency(0)

        self.lblNameCol = DirectLabel(
            borderWidth=(2, 2),
            frameColor=(0.8, 0.8, 0.8, 0.0),
            hpr=LVecBase3f(0, 0, 0),
            pos=LPoint3f(-220, 0, 45),
            scale=LVecBase3f(1, 1, 1),
            text='Name',
            text_align=TextNode.A_left,
            text_scale=(12.0, 12.0),
            text_pos=(0, 0),
            text_fg=LVecBase4f(0, 0, 0, 1),
            text_bg=LVecBase4f(0, 0, 0, 0),
            parent=self.frmApplications,
        )
        self.lblNameCol.setTransparency(0)

        self.lblPathCol = DirectLabel(
            borderWidth=(2, 2),
            frameColor=(0.8, 0.8, 0.8, 0.0),
            hpr=LVecBase3f(0, 0, 0),
            pos=LPoint3f(-95, 0, 45),
            scale=LVecBase3f(1, 1, 1),
            text='Path',
            text_align=TextNode.A_left,
            text_scale=(12.0, 12.0),
            text_pos=(0, 0),
            text_fg=LVecBase4f(0, 0, 0, 1),
            text_bg=LVecBase4f(0, 0, 0, 0),
            parent=self.frmApplications,
        )
        self.lblPathCol.setTransparency(0)

        self.lblTerminalCol = DirectLabel(
            borderWidth=(2, 2),
            frameColor=(0.8, 0.8, 0.8, 0.0),
            hpr=LVecBase3f(0, 0, 0),
            pos=LPoint3f(100, 0, 45),
            scale=LVecBase3f(1, 1, 1),
            text='Terminal App',
            text_align=TextNode.A_center,
            text_scale=(12.0, 12.0),
            text_pos=(0, 0),
            text_fg=LVecBase4f(0, 0, 0, 1),
            text_bg=LVecBase4f(0, 0, 0, 0),
            parent=self.frmApplications,
        )
        self.lblTerminalCol.setTransparency(0)

        self.tabbedFrame.add_tab("Applications", self.frmApplications)

        self.frmInclude = DirectFrame(
            borderWidth=(2, 2),
            frameColor=(1, 1, 1, 1),
            frameSize=(-250.0, 250.0, -180.0, 150.0),
            hpr=LVecBase3f(0, 0, 0),
            pos=LPoint3f(250.0, 0, tab_frame_z_pos),
            relief=3,
            parent=rootParent,
        )
        self.frmInclude.setTransparency(0)

        self.btnAddIncludePattern = DirectButton(
            borderWidth=(2, 2),
            frameSize=(-250.0, 250.0, -12.25, 27.55),
            hpr=LVecBase3f(0, 0, 0),
            pos=LPoint3f(0, 0, 70),
            scale=LVecBase3f(0.5, 0.5, 0.5),
            text='Add pattern',
            text_align=TextNode.A_center,
            text_scale=(24, 24),
            text_pos=(0, 0),
            text_fg=LVecBase4f(0, 0, 0, 1),
            text_bg=LVecBase4f(0, 0, 0, 0),
            parent=self.frmInclude,
            command=base.messenger.send,
            extraArgs=["p3d_setup_wizard_addIncludePattern"],
        )
        self.btnAddIncludePattern.setTransparency(0)

        self.lblIncludePatterns = DirectLabel(
            borderWidth=(2, 2),
            frameColor=(0.8, 0.8, 0.8, 0.0),
            hpr=LVecBase3f(0, 0, 0),
            pos=LPoint3f(0, 0, 110),
            scale=LVecBase3f(1, 1, 1),
            text='Include Patterns',
            text_align=TextNode.A_center,
            text_scale=(12.0, 12.0),
            text_pos=(0, 0),
            text_fg=LVecBase4f(0, 0, 0, 1),
            text_bg=LVecBase4f(0, 0, 0, 0),
            parent=self.frmInclude,
        )
        self.lblIncludePatterns.setTransparency(0)

        self.frmIncludePatterns = DirectScrolledFrame(
            canvasSize=(-215.0, 215.0, -300.0, 0.0),
            frameColor=(1.0, 1.0, 1.0, 1.0),
            frameSize=(-225.0, 225.0, -200.0, 0.0),
            hpr=LVecBase3f(0, 0, 0),
            pos=LPoint3f(0, 0, 40),
            scrollBarWidth=20,
            state='normal',
            horizontalScroll_borderWidth=(2, 2),
            horizontalScroll_frameSize=(-0.05, 0.05, -10.0, 10.0),
            horizontalScroll_hpr=LVecBase3f(0, 0, 0),
            horizontalScroll_pos=LPoint3f(0, 0, 0),
            horizontalScroll_decButton_borderWidth=(2, 2),
            horizontalScroll_decButton_frameSize=(-0.05, 0.05, -10.0, 10.0),
            horizontalScroll_decButton_hpr=LVecBase3f(0, 0, 0),
            horizontalScroll_decButton_pos=LPoint3f(0, 0, 0),
            horizontalScroll_incButton_borderWidth=(2, 2),
            horizontalScroll_incButton_frameSize=(-0.05, 0.05, -10.0, 10.0),
            horizontalScroll_incButton_hpr=LVecBase3f(0, 0, 0),
            horizontalScroll_incButton_pos=LPoint3f(0, 0, 0),
            horizontalScroll_thumb_borderWidth=(2, 2),
            horizontalScroll_thumb_hpr=LVecBase3f(0, 0, 0),
            horizontalScroll_thumb_pos=LPoint3f(0, 0, 0),
            verticalScroll_borderWidth=(2, 2),
            verticalScroll_frameSize=(-10.0, 10.0, -0.05, 0.05),
            verticalScroll_hpr=LVecBase3f(0, 0, 0),
            verticalScroll_pos=LPoint3f(0, 0, 0),
            verticalScroll_decButton_borderWidth=(2, 2),
            verticalScroll_decButton_frameSize=(-10.0, 10.0, -0.05, 0.05),
            verticalScroll_decButton_hpr=LVecBase3f(0, 0, 0),
            verticalScroll_decButton_pos=LPoint3f(215, 0, -10),
            verticalScroll_incButton_borderWidth=(2, 2),
            verticalScroll_incButton_frameSize=(-10.0, 10.0, -0.05, 0.05),
            verticalScroll_incButton_hpr=LVecBase3f(0, 0, 0),
            verticalScroll_incButton_pos=LPoint3f(215, 0, -190),
            verticalScroll_thumb_borderWidth=(2, 2),
            verticalScroll_thumb_hpr=LVecBase3f(0, 0, 0),
            verticalScroll_thumb_pos=LPoint3f(215, 0, -73.3333),
            parent=self.frmInclude,
        )
        self.frmIncludePatterns.setTransparency(0)

        self.lblPatternCol = DirectLabel(
            borderWidth=(2, 2),
            frameColor=(0.8, 0.8, 0.8, 0.0),
            hpr=LVecBase3f(0, 0, 0),
            pos=LPoint3f(-220, 0, 45),
            scale=LVecBase3f(1, 1, 1),
            text='Pattern',
            text_align=TextNode.A_left,
            text_scale=(12.0, 12.0),
            text_pos=(0, 0),
            text_fg=LVecBase4f(0, 0, 0, 1),
            text_bg=LVecBase4f(0, 0, 0, 0),
            parent=self.frmInclude,
        )
        self.lblPatternCol.setTransparency(0)

        self.tabbedFrame.add_tab("Includes", self.frmInclude)

        self.frmExclude = DirectFrame(
            borderWidth=(2, 2),
            frameColor=(1, 1, 1, 1),
            frameSize=(-250.0, 250.0, -180.0, 150.0),
            hpr=LVecBase3f(0, 0, 0),
            pos=LPoint3f(250.0, 0, tab_frame_z_pos),
            relief=3,
            parent=rootParent,
        )
        self.frmExclude.setTransparency(0)

        self.lblExcludePatterns = DirectLabel(
            borderWidth=(2, 2),
            frameColor=(0.8, 0.8, 0.8, 0.0),
            hpr=LVecBase3f(0, 0, 0),
            pos=LPoint3f(0, 0, 110),
            scale=LVecBase3f(1, 1, 1),
            text='Exclude Patterns',
            text_align=TextNode.A_center,
            text_scale=(12.0, 12.0),
            text_pos=(0, 0),
            text_fg=LVecBase4f(0, 0, 0, 1),
            text_bg=LVecBase4f(0, 0, 0, 0),
            parent=self.frmExclude,
        )
        self.lblExcludePatterns.setTransparency(0)

        self.btnAddExcludePattern = DirectButton(
            borderWidth=(2, 2),
            frameSize=(-250.0, 250.0, -12.225, 27.55),
            hpr=LVecBase3f(0, 0, 0),
            pos=LPoint3f(0, 0, 70),
            scale=LVecBase3f(0.5, 0.5, 0.5),
            text='Add pattern',
            text_align=TextNode.A_center,
            text_scale=(24, 24),
            text_pos=(0, 0),
            text_fg=LVecBase4f(0, 0, 0, 1),
            text_bg=LVecBase4f(0, 0, 0, 0),
            command=base.messenger.send,
            extraArgs=["p3d_setup_wizard_addExcludePattern"],
            parent=self.frmExclude,
        )
        self.btnAddExcludePattern.setTransparency(0)

        self.pg23054 = DirectLabel(
            borderWidth=(2, 2),
            frameColor=(0.8, 0.8, 0.8, 0.0),
            hpr=LVecBase3f(0, 0, 0),
            pos=LPoint3f(-220, 0, 45),
            scale=LVecBase3f(1, 1, 1),
            text='Pattern',
            text_align=TextNode.A_left,
            text_scale=(12.0, 12.0),
            text_pos=(0, 0),
            text_fg=LVecBase4f(0, 0, 0, 1),
            text_bg=LVecBase4f(0, 0, 0, 0),
            parent=self.frmExclude,
        )
        self.pg23054.setTransparency(0)

        self.frmExcludePatterns = DirectScrolledFrame(
            canvasSize=(-215.0, 215.0, -300.0, 0.0),
            frameColor=(1, 1, 1, 1),
            frameSize=(-225.0, 225.0, -200.0, 0.0),
            hpr=LVecBase3f(0, 0, 0),
            pos=LPoint3f(0, 0, 40),
            scrollBarWidth=20,
            state='normal',
            horizontalScroll_borderWidth=(2, 2),
            horizontalScroll_frameSize=(-0.05, 0.05, -10.0, 10.0),
            horizontalScroll_hpr=LVecBase3f(0, 0, 0),
            horizontalScroll_pos=LPoint3f(0, 0, 0),
            horizontalScroll_decButton_borderWidth=(2, 2),
            horizontalScroll_decButton_frameSize=(-0.05, 0.05, -10.0, 10.0),
            horizontalScroll_decButton_hpr=LVecBase3f(0, 0, 0),
            horizontalScroll_decButton_pos=LPoint3f(0, 0, 0),
            horizontalScroll_incButton_borderWidth=(2, 2),
            horizontalScroll_incButton_frameSize=(-0.05, 0.05, -10.0, 10.0),
            horizontalScroll_incButton_hpr=LVecBase3f(0, 0, 0),
            horizontalScroll_incButton_pos=LPoint3f(0, 0, 0),
            horizontalScroll_thumb_borderWidth=(2, 2),
            horizontalScroll_thumb_hpr=LVecBase3f(0, 0, 0),
            horizontalScroll_thumb_pos=LPoint3f(0, 0, 0),
            verticalScroll_borderWidth=(2, 2),
            verticalScroll_frameSize=(-10.0, 10.0, -0.05, 0.05),
            verticalScroll_hpr=LVecBase3f(0, 0, 0),
            verticalScroll_pos=LPoint3f(0, 0, 0),
            verticalScroll_decButton_borderWidth=(2, 2),
            verticalScroll_decButton_frameSize=(-10.0, 10.0, -0.05, 0.05),
            verticalScroll_decButton_hpr=LVecBase3f(0, 0, 0),
            verticalScroll_decButton_pos=LPoint3f(215, 0, -10),
            verticalScroll_incButton_borderWidth=(2, 2),
            verticalScroll_incButton_frameSize=(-10.0, 10.0, -0.05, 0.05),
            verticalScroll_incButton_hpr=LVecBase3f(0, 0, 0),
            verticalScroll_incButton_pos=LPoint3f(215, 0, -190),
            verticalScroll_thumb_borderWidth=(2, 2),
            verticalScroll_thumb_hpr=LVecBase3f(0, 0, 0),
            verticalScroll_thumb_pos=LPoint3f(215, 0, -73.3333),
            parent=self.frmExclude,
        )
        self.frmExcludePatterns.setTransparency(0)

        self.tabbedFrame.add_tab("Excludes", self.frmExclude)

        self.frmAdvanced = DirectFrame(
            borderWidth=(2, 2),
            frameColor=(1, 1, 1, 1),
            frameSize=(-250.0, 250.0, -180.0, 150.0),
            hpr=LVecBase3f(0, 0, 0),
            pos=LPoint3f(250.0, 0, tab_frame_z_pos),
            relief=3,
            parent=rootParent,
        )
        self.frmAdvanced.setTransparency(0)

        self.lblAdvanced = DirectLabel(
            borderWidth=(2, 2),
            frameColor=(0.8, 0.8, 0.8, 0.0),
            hpr=LVecBase3f(0, 0, 0),
            pos=LPoint3f(0, 0, 110),
            scale=LVecBase3f(1, 1, 1),
            text='Advanced',
            text_align=TextNode.A_center,
            text_scale=(12.0, 12.0),
            text_pos=(0, 0),
            text_fg=LVecBase4f(0, 0, 0, 1),
            text_bg=LVecBase4f(0, 0, 0, 0),
            parent=self.frmAdvanced,
        )
        self.lblAdvanced.setTransparency(0)

        self.lblBuildBase = DirectLabel(
            borderWidth=(2, 2),
            frameColor=(0.8, 0.8, 0.8, 0.0),
            hpr=LVecBase3f(0, 0, 0),
            pos=LPoint3f(-180, 0, 70),
            scale=LVecBase3f(1, 1, 1),
            text='Build directory',
            text_align=TextNode.A_center,
            text_scale=(12.0, 12.0),
            text_pos=(0, 0),
            text_fg=LVecBase4f(0, 0, 0, 1),
            text_bg=LVecBase4f(0, 0, 0, 0),
            parent=self.frmAdvanced,
        )
        self.lblBuildBase.setTransparency(0)

        self.txtBuildBase = DirectEntry(
            borderWidth=(0.167, 0.167),
            hpr=LVecBase3f(0, 0, 0),
            overflow=1,
            pos=LPoint3f(-60, 0, 70),
            scale=LVecBase3f(12, 12, 12),
            width=20.0,
            text_align=TextNode.A_left,
            text_scale=(1, 1),
            text_pos=(0, 0),
            text_fg=LVecBase4f(0, 0, 0, 1),
            text_bg=LVecBase4f(0, 0, 0, 0),
            parent=self.frmAdvanced,
        )
        self.txtBuildBase.setTransparency(0)

        self.lblRequirementsPaths = DirectLabel(
            borderWidth=(2, 2),
            frameColor=(0.8, 0.8, 0.8, 0.0),
            hpr=LVecBase3f(0, 0, 0),
            pos=LPoint3f(-180, 0, 40),
            scale=LVecBase3f(1, 1, 1),
            text='Requirements file',
            text_align=TextNode.A_center,
            text_scale=(12.0, 12.0),
            text_pos=(0, 0),
            text_fg=LVecBase4f(0, 0, 0, 1),
            text_bg=LVecBase4f(0, 0, 0, 0),
            parent=self.frmAdvanced,
        )
        self.lblRequirementsPaths.setTransparency(0)

        self.txtRequirementsPaths = DirectEntry(
            borderWidth=(0.167, 0.167),
            hpr=LVecBase3f(0, 0, 0),
            overflow=1,
            pos=LPoint3f(-60, 0, 40),
            scale=LVecBase3f(12, 12, 12),
            width=20.0,
            text_align=TextNode.A_left,
            text_scale=(1, 1),
            text_pos=(0, 0),
            text_fg=LVecBase4f(0, 0, 0, 1),
            text_bg=LVecBase4f(0, 0, 0, 0),
            parent=self.frmAdvanced,
        )
        self.txtRequirementsPaths.setTransparency(0)

        self.txtOptimizedWheels = DirectLabel(
            borderWidth=(2, 2),
            frameColor=(0.8, 0.8, 0.8, 0.0),
            hpr=LVecBase3f(0, 0, 0),
            pos=LPoint3f(-180, 0, 10),
            scale=LVecBase3f(1, 1, 1),
            text='Use optimized wheels',
            text_align=TextNode.A_center,
            text_scale=(12.0, 12.0),
            text_pos=(0, 0),
            text_fg=LVecBase4f(0, 0, 0, 1),
            text_bg=LVecBase4f(0, 0, 0, 0),
            parent=self.frmAdvanced,
        )
        self.txtOptimizedWheels.setTransparency(0)

        self.cbOptimizedWheels = DirectCheckButton(
            borderWidth=(2, 2),
            hpr=LVecBase3f(0, 0, 0),
            pos=LPoint3f(70, 0, 15),
            scale=LVecBase3f(0.5, 0.5, 0.5),
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
            text_scale=(12.0, 12.0),
            text_pos=(0, 0),
            text_fg=LVecBase4f(0, 0, 0, 1),
            text_bg=LVecBase4f(0, 0, 0, 0),
            parent=self.frmAdvanced,
        )
        self.cbOptimizedWheels.setTransparency(0)

        self.lblOptimizedWheelsIndex = DirectLabel(
            borderWidth=(2, 2),
            frameColor=(0.8, 0.8, 0.8, 0.0),
            hpr=LVecBase3f(0, 0, 0),
            pos=LPoint3f(-180, 0, -20),
            scale=LVecBase3f(1, 1, 1),
            text='Optimized wheel index',
            text_align=TextNode.A_center,
            text_scale=(12.0, 12.0),
            text_pos=(0, 0),
            text_fg=LVecBase4f(0, 0, 0, 1),
            text_bg=LVecBase4f(0, 0, 0, 0),
            parent=self.frmAdvanced,
        )
        self.lblOptimizedWheelsIndex.setTransparency(0)

        self.txtOptimizedWheelsIndex = DirectEntry(
            borderWidth=(0.167, 0.167),
            hpr=LVecBase3f(0, 0, 0),
            overflow=1,
            pos=LPoint3f(-60, 0, -20),
            scale=LVecBase3f(12, 12, 12),
            width=20.0,
            text_align=TextNode.A_left,
            text_scale=(1, 1),
            text_pos=(0, 0),
            text_fg=LVecBase4f(0, 0, 0, 1),
            text_bg=LVecBase4f(0, 0, 0, 0),
            parent=self.frmAdvanced,
        )
        self.txtOptimizedWheelsIndex.setTransparency(0)

        self.lblDistDir = DirectLabel(
            borderWidth=(2, 2),
            frameColor=(0.8, 0.8, 0.8, 0.0),
            hpr=LVecBase3f(0, 0, 0),
            pos=LPoint3f(-180, 0, -50),
            scale=LVecBase3f(1, 1, 1),
            text='Distribution directory',
            text_align=TextNode.A_center,
            text_scale=(12.0, 12.0),
            text_pos=(0, 0),
            text_fg=LVecBase4f(0, 0, 0, 1),
            text_bg=LVecBase4f(0, 0, 0, 0),
            parent=self.frmAdvanced,
        )
        self.lblDistDir.setTransparency(0)

        self.txtDistDir = DirectEntry(
            borderWidth=(0.167, 0.167),
            hpr=LVecBase3f(0, 0, 0),
            overflow=1,
            pos=LPoint3f(-60, 0, -50),
            scale=LVecBase3f(12, 12, 12),
            width=20.0,
            text_align=TextNode.A_left,
            text_scale=(1, 1),
            text_pos=(0, 0),
            text_fg=LVecBase4f(0, 0, 0, 1),
            text_bg=LVecBase4f(0, 0, 0, 0),
            parent=self.frmAdvanced,
        )
        self.txtDistDir.setTransparency(0)

        self.tabbedFrame.add_tab("Advanced", self.frmAdvanced)

    def show(self):
        self.btnDeploy.show()
        self.btnLoad.show()
        self.lblHeader.show()
        self.btnSave.show()
        self.frmMetadata.show()
        self.frmPlatforms.show()
        self.frmPlugins.show()
        self.frmApplications.show()
        self.rbMetadata.show()
        self.rbPlatforms.show()
        self.rbPlugins.show()
        self.rbApplications.show()
        self.rbInclude.show()
        self.frmInclude.show()
        self.frmExclude.show()
        self.rbExclude.show()
        self.frmAdvanced.show()
        self.rbAdvanced.show()

    def hide(self):
        self.btnDeploy.hide()
        self.btnLoad.hide()
        self.lblHeader.hide()
        self.btnSave.hide()
        self.frmMetadata.hide()
        self.frmPlatforms.hide()
        self.frmPlugins.hide()
        self.frmApplications.hide()
        self.rbMetadata.hide()
        self.rbPlatforms.hide()
        self.rbPlugins.hide()
        self.rbApplications.hide()
        self.rbInclude.hide()
        self.frmInclude.hide()
        self.frmExclude.hide()
        self.rbExclude.hide()
        self.frmAdvanced.hide()
        self.rbAdvanced.hide()

    def destroy(self):
        self.btnDeploy.destroy()
        self.btnLoad.destroy()
        self.lblHeader.destroy()
        self.btnSave.destroy()
        self.frmMetadata.destroy()
        self.frmPlatforms.destroy()
        self.frmPlugins.destroy()
        self.frmApplications.destroy()
        self.rbMetadata.destroy()
        self.rbPlatforms.destroy()
        self.rbPlugins.destroy()
        self.rbApplications.destroy()
        self.rbInclude.destroy()
        self.frmInclude.destroy()
        self.frmExclude.destroy()
        self.rbExclude.destroy()
        self.frmAdvanced.destroy()
        self.rbAdvanced.destroy()
