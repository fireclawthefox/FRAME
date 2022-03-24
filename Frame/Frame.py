import sys
import os
import logging

from panda3d.core import (
    Filename,
    loadPrcFileData,
    TextNode,
    ConfigVariableBool,
    WindowProperties
)

from direct.showbase.DirectObject import DirectObject
from direct.gui import DirectGuiGlobals as DGG
from direct.gui.DirectDialog import OkCancelDialog
from direct.gui.DirectFrame import DirectFrame

from DirectGuiExtension.DirectTooltip import DirectTooltip

from Frame.GUI.MainView import MainView

HAS_SCENE_EDITOR = True
try:
    from SceneEditor.SceneEditor import SceneEditor
except:
    HAS_SCENE_EDITOR = False

HAS_GUI_EDITOR = True
try:
    from DirectGuiDesigner.DirectGuiDesigner import DirectGuiDesigner
except:
    HAS_GUI_EDITOR = False

class Frame(DirectObject):
    def __init__(self):
        fn = Filename.fromOsSpecific(os.path.dirname(__file__))
        fn.makeTrueCase()
        self.icon_dir = str(fn) + "/"
        loadPrcFileData("", f"model-path {self.icon_dir}")

        self.dlg_quit = None

        self.main_view = MainView()

        self.tt = DirectTooltip(
            text = "Tooltip",
            #text_fg = (1,1,1,1),
            pad=(0.2, 0.2),
            scale = 16,
            text_align = TextNode.ALeft,
            frameColor = (1, 1, 0.7, 1),
            parent=base.pixel2d,
            sortOrder=1000)

        first_editor_frame = None
        if HAS_SCENE_EDITOR:
            se_ef = self.main_view.editor_selection.createEditorButton(
                "icons/EditorSelectionSE.png",
                SceneEditor,
                self.tt,
                "Scene Editor")
            first_editor_frame = se_ef

        if HAS_GUI_EDITOR:
            dg_ef = self.main_view.editor_selection.createEditorButton(
                "icons/EditorSelectionGD.png",
                DirectGuiDesigner,
                self.tt,
                "GUI Designer")
            if first_editor_frame is None:
                first_editor_frame = dg_ef

        if first_editor_frame is not None:
            self.main_view.editor_selection.select_editor(first_editor_frame)

        self.screenSize = base.getSize()
        sys.excepthook = self.excHandler
        base.win.setCloseRequestEvent("FRAME_quit_app")

        self.enable_events()

    def enable_events(self):
        self.accept("FRAME_quit_app", self.quit_app)

        self.accept("request_dirty_name", self.set_dirty_name)
        self.accept("request_clean_name", self.set_clean_name)

    def disable_events(self):
        self.ignore_all()

    def set_dirty_name(self):
        wp = WindowProperties()
        wp.setTitle("*Panda3D FRAME")
        base.win.requestProperties(wp)

    def set_clean_name(self):
        if not self.get_any_editor_dirty():
            wp = WindowProperties()
            wp.setTitle("Panda3D FRAME")
            base.win.requestProperties(wp)

    def __quit(self, selection):
        if selection == 1:
            base.userExit()
        else:
            self.dlg_quit.destroy()
            self.dlg_quit_shadow.destroy()
            self.dlg_quit = None
            self.dlg_quit_shadow = None

    def quit_app(self):
        if self.dlg_quit is not None: return
        if ConfigVariableBool("skip-ask-for-quit", False).getValue() or self.get_any_editor_dirty() == False:
            self.__quit(1)
            return

        self.dlg_quit = OkCancelDialog(
            text="You have unsaved changes!\nReally Quit?",
            state=DGG.NORMAL,
            relief=DGG.RIDGE,
            frameColor=(1,1,1,1),
            scale=300,
            pos=(base.getSize()[0]/2, 0, -base.getSize()[1]/2),
            sortOrder=1,
            button_relief=DGG.FLAT,
            button_frameColor=(0.8, 0.8, 0.8, 1),
            command=self.__quit,
            parent=base.pixel2d)
        self.dlg_quit_shadow = DirectFrame(
            state=DGG.NORMAL,
            sortOrder=0,
            frameColor=(0,0,0,0.5),
            frameSize=(0, base.getSize()[0], -base.getSize()[1], 0),
            parent=base.pixel2d)

    def get_any_editor_dirty(self):
        dirty = False
        for editor_frame in self.main_view.editor_selection.editor_frames:
            dirty |= editor_frame.editor_instance.is_dirty()
        return dirty

    def excHandler(self, ex_type, ex_value, ex_traceback):
        logging.error("Unhandled exception", exc_info=(ex_type, ex_value, ex_traceback))
        #print("Try to save project after unhandled exception. Please restart FRAME to automatically load the exception save file!")

        for editor_frame in self.main_view.editor_selection.editor_frames:
            editor_frame.editor_instance.do_exception_save()
