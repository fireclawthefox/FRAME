from panda3d.core import TransparencyAttrib, ConfigVariableBool

from direct.showbase.DirectObject import DirectObject

from direct.gui import DirectGuiGlobals as DGG
DGG.BELOW = "below"

from direct.gui.DirectButton import DirectButton
from direct.gui.DirectFrame import DirectFrame
from direct.gui.DirectCheckBox import DirectCheckBox
from DirectGuiExtension.DirectMenuItem import DirectMenuItem, DirectMenuItemEntry, DirectMenuItemSubMenu, DirectMenuSeparator
from DirectGuiExtension.DirectBoxSizer import DirectBoxSizer

class MenuBar(DirectObject):
    def __init__(self):
        screenWidthPx = base.getSize()[0]

        #
        # Menubar
        #
        self.menu_bar = DirectBoxSizer(
            frameColor=(0.25, 0.25, 0.25, 1),
            frameSize=(0,screenWidthPx,-12, 12),
            autoUpdateFrameSize=False,
            pos=(0, 0, 0),
            itemMargin=(2,2,2,2),
            parent=base.pixel2d)

        self.project_entries = [
            DirectMenuItemEntry("New", base.messenger.send, ["FRAME_new_project"]),
            DirectMenuSeparator(),
            DirectMenuItemEntry("Open", base.messenger.send, ["FRAME_load_project"]),
            DirectMenuItemEntry("Save", base.messenger.send, ["FRAME_save_project"]),
            DirectMenuItemEntry("Close", base.messenger.send, ["FRAME_close_project"]),
            DirectMenuSeparator(),
            DirectMenuItemEntry("Quit", base.messenger.send, ["FRAME_quit_app"]),
            ]
        self.project = self.__create_menu_item("Project", self.project_entries)

        self.tools_entries = [
            DirectMenuItemEntry("Run Project", base.messenger.send, ["FRAME_run_project"]),
            DirectMenuItemEntry("Stop Project", base.messenger.send, ["FRAME_stop_project"]),
            DirectMenuItemEntry("Run Server", base.messenger.send, ["FRAME_run_project_server"]),
            DirectMenuItemEntry("Stop Server", base.messenger.send, ["FRAME_stop_project_server"]),
            DirectMenuItemEntry("Show Terminals", base.messenger.send, ["FRAME_show_terminal_window"]),
            DirectMenuItemEntry("Hide Terminals", base.messenger.send, ["FRAME_hide_terminal_window"]),
            ]
        self.tools = self.__create_menu_item("Tools", self.tools_entries)

        self.menu_bar.addItem(self.project, skipRefresh=True)
        self.menu_bar.addItem(self.tools)#, skipRefresh=True)

    def __create_menu_item(self, text, entries):
        color = (
            (0.25, 0.25, 0.25, 1), # Normal
            (0.35, 0.35, 1, 1), # Click
            (0.25, 0.25, 1, 1), # Hover
            (0.1, 0.1, 0.1, 1)) # Disabled

        sepColor = (0.7, 0.7, 0.7, 1)

        return DirectMenuItem(
            text=text,
            text_fg=(1,1,1,1),
            text_scale=0.8,
            items=entries,
            frameSize=(0,65/21,-7/21,17/21),
            frameColor=color,
            scale=21,
            relief=DGG.FLAT,
            item_text_fg=(1,1,1,1),
            item_text_scale=0.8,
            item_relief=DGG.FLAT,
            item_pad=(0.2, 0.2),
            itemFrameColor=color,
            separatorFrameColor=sepColor,
            popupMenu_itemMargin=(0,0,-.1,-.1),
            popupMenu_frameColor=color,
            highlightColor=color[2])
