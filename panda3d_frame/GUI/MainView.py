import logging

from direct.showbase.DirectObject import DirectObject

from direct.gui import DirectGuiGlobals as DGG
from direct.gui.DirectFrame import DirectFrame

from DirectGuiExtension.DirectBoxSizer import DirectBoxSizer
from DirectGuiExtension.DirectAutoSizer import DirectAutoSizer

from panda3d_frame.GUI.MenuBar import MenuBar
from panda3d_frame.GUI.EditorSelection import EditorSelection

from panda3d_frame.GUI.Terminal.TerminalWindow import TerminalWindow

class MainView(DirectObject):
    def __init__(self):
        logging.debug("Setup GUI")

        self.is_setup_done = False
        self.menuBarHeight = 24

        #
        # LAYOUT SETUP
        #

        # the box everything get's added to
        self.main_box = DirectBoxSizer(
            frameColor=(0,0,0,0),
            state=DGG.DISABLED,
            orientation=DGG.VERTICAL,
            autoUpdateFrameSize=False)
        # our root element for the main box
        self.main_sizer = DirectAutoSizer(
            frameColor=(0,0,0,0),
            parent=base.pixel2d,
            child=self.main_box,
            childUpdateSizeFunc=self.main_box.refresh
            )

        # our menu bar
        self.menu_bar_sizer = DirectAutoSizer(
            updateOnWindowResize=False,
            frameColor=(0,0,0,0),
            parent=self.main_box,
            extendVertical=False)

        # our editor box
        self.editor_box = DirectBoxSizer(
            frameColor=(0,0,1,0.25),
            state=DGG.DISABLED,
            autoUpdateFrameSize=False)
        self.editor_box_sizer = DirectAutoSizer(
            frameColor=(0,0,0,0),
            parent=self.main_box,
            parentGetSizeFunction=self.get_main_box_size,
            child=self.editor_box,
            childUpdateSizeFunc=self.refresh_content_area,
            extendVertical=False,
            extendHorizontal=False
            )

        # CONNECT THE UI ELEMENTS
        self.main_box.addItem(
            self.menu_bar_sizer,
            updateFunc=self.menu_bar_sizer.refresh,
            skipRefresh=True)
        self.main_box.addItem(
            self.editor_box_sizer,
            updateFunc=self.editor_box_sizer.refresh,
            skipRefresh=True)

        #
        # CONTENT SETUP
        #
        self.menu_bar = MenuBar()
        self.menu_bar_sizer.setChild(self.menu_bar.menu_bar)
        self.menu_bar_sizer["childUpdateSizeFunc"] = self.menu_bar.menu_bar.refresh

        self.editor_selection = EditorSelection(-self.menuBarHeight)
        self.editor_box.addItem(self.editor_selection.editor_selection)

        self.editor_frame = self.setup_editor_holder_frame()
        self.editor_selection.set_editor_holder_frame(self.editor_frame)
        self.editor_box.addItem(self.editor_frame)

        self.terminal_window = TerminalWindow(frameSize=(-1,1,-1,1))
        self.terminal_window_sizer = DirectAutoSizer(
            frameColor=(0,0,0,0),
            pos=(0,0,-1),
            child=self.terminal_window,
            frameSize=(-1,1,-1,1),
            extendVertical=False,
            childUpdateSizeFunc=self.terminal_window.refresh)
        self.terminal_window_sizer.set_bin("gui-popup", 0)

        self.is_setup_done = True
        self.main_box.refresh()

    def show_terminal_window(self):
        self.terminal_window.slide_in()

    def hide_terminal_window(self):
        self.terminal_window.slide_out()

    def refresh_content_area(self):
        if not self.is_setup_done:
            return
        self.editor_box.refresh()
        self.editor_frame["frameSize"] = self.get_editor_frame_size()
        self.editor_selection.refresh()

    def setup_editor_holder_frame(self):
        return DirectFrame(
            frameSize=self.get_editor_frame_size(),
            frameColor=(0,0,0,0),
            pos=(self.editor_selection.width, 0, self.menuBarHeight))

    def get_editor_frame_size(self):
        return (
            0,
            base.get_size()[0] - self.editor_selection.width,
            -base.get_size()[1] + self.menuBarHeight,
            0)

    def get_main_box_size(self):
        return (
            -base.get_size()[0]/2,
            base.get_size()[0]/2,
            0,
            base.get_size()[1] - self.menuBarHeight)
