import sys
import os
import logging
import json
import importlib

from dataclasses import dataclass

from panda3d.core import (
    Filename,
    loadPrcFileData,
    TextNode,
    ConfigVariableBool,
    WindowProperties
)

from direct.showbase.DirectObject import DirectObject
from direct.gui import DirectGuiGlobals as DGG
from direct.gui.DirectDialog import OkCancelDialog, OkDialog
from direct.gui.DirectFrame import DirectFrame

from DirectGuiExtension.DirectTooltip import DirectTooltip

from DirectFolderBrowser.DirectFolderBrowser import DirectFolderBrowser

from panda3d_frame.GUI.MainView import MainView
from panda3d_frame.GUI.InternalEditors.EditorStore import EditorStore
from panda3d_frame.core.ProjectManager import ProjectManager
from panda3d_frame.Extensions.NodeEditor.NodeEditorExtender import NodeEditorExtender


@dataclass
class Editor:
    name: str
    class_def: str
    config_to_enable: str
    order: int
    icon: str
    file_extension: str
    extra_args_func: str
    extra_args: list

    def __lt__(self, other):
        return self.order < other.order




class Frame(DirectObject, NodeEditorExtender):
    def __init__(self, editor_definitions_paths, log_file, config_file):
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

        self.editors = []
        for path in editor_definitions_paths:
            if not os.path.exists(path):
                continue
            for root, dirs, files in os.walk(path):
                for filename in files:
                    if not filename.endswith(".json"):
                        continue
                    editor_definition_file = os.path.join(root, filename)
                    editor = self.load_editor_definition(editor_definition_file, root)
                    if not editor:
                        continue
                    self.editors.append(editor)
        self.editors.sort()
        for editor in self.editors:
            if not ConfigVariableBool(editor.config_to_enable, True).getValue():
                continue

            editor_class_extra_args = None

            if editor.extra_args_func != "":
                try:
                    if hasattr(editor.class_def, editor.extra_args_func):
                        editor_class_extra_args = getattr(
                            editor.class_def,
                            editor.extra_args_func)()
                    elif hasattr(self, editor.extra_args_func):
                        editor_class_extra_args = getattr(
                            self,
                            editor.extra_args_func)()
                except Exception as e:
                    logging.error(
                        f"FRAME: Could not get extra arguments for {editor.name} via method call {editor.extra_args_func}",
                        exc_info=True)
            if len(editor.extra_args) > 0:
                if type(editor_class_extra_args) is list:
                    editor_class_extra_args.append(editor.extra_args)
                elif editor_class_extra_args is not None:
                    editor_class_extra_args = [editor_class_extra_args] \
                        + editor.extra_args
                else:
                    editor_class_extra_args = editor.extra_args

            logging.debug(f"load editor: {editor}")
            editor_frame = self.main_view.editor_selection.create_editor_button(
                editor.icon,
                editor.class_def,
                self.tt,
                editor.name,
                log_file,
                config_file,
                editor_class_extra_args)

            if first_editor_frame is None:
                first_editor_frame = editor_frame

        es_ef = self.main_view.editor_selection.create_editor_button(
            "icons/EditorSelectionStore.png",
            EditorStore,
            self.tt,
            "Editor Store",
            log_file,
            config_file,
            )

        if first_editor_frame is not None:
            self.main_view.editor_selection.select_editor(first_editor_frame)

        self.screenSize = base.getSize()
        sys.excepthook = self.excHandler
        base.win.setCloseRequestEvent("FRAME_quit_app")

        self.project_manager = ProjectManager(self.tt)

        self.enable_events()

    def load_editor_definition(self, editor_definition_file, root_path):
        try:
            with open(editor_definition_file, 'r') as edf:
                edf_content = json.load(edf)
                if edf_content is None:
                    raise Exception("Editor definition not valid")

                editor_module = importlib.import_module(edf_content["module"])
                class_def = getattr(editor_module, edf_content["class"])

                return Editor(
                    edf_content["name"],
                    class_def,
                    edf_content["configToEnable"],
                    edf_content["order"],
                    os.path.join(root_path, edf_content["icon"]),
                    edf_content["fileExtension"]
                    if "fileExtension" in edf_content else "",
                    edf_content["extraArgsFunc"]
                    if "extraArgsFunc" in edf_content else "",
                    edf_content["extraArgs"] if "extraArgs" in edf_content else []
                    )
        except Exception as e:
            logging.error(
                f"FRAME: Couldn't load editor definition {editor_definition_file}",
                exc_info=True)
        return None

    def enable_events(self):
        self.accept("FRAME_quit_app", self.quit_app)

        self.accept("FRAME_new_project", self.project_manager.new_project)
        self.accept("FRAME_load_project", self.project_manager.load)
        self.accept("FRAME_save_project", self.project_manager.save)
        self.accept("FRAME_close_project", self.project_manager.close)

        self.accept("FRAME_run_project", self.project_manager.run_project)
        self.accept("FRAME_stop_project", self.project_manager.stop_project)
        self.accept("FRAME_run_project_server", self.project_manager.run_project_server)
        self.accept("FRAME_stop_project_server", self.project_manager.stop_project_server)

        self.accept("FRAME_show_terminal_window", self.main_view.show_terminal_window)
        self.accept("FRAME_hide_terminal_window", self.main_view.hide_terminal_window)

        self.accept("FRAME_add_terminal_process", self.main_view.terminal_window.add_terminal)

        self.accept("FRAME_show_warning", self.show_warning)

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

    def show_warning(self, warning):
        def close_warning_dialog(decission):
            self.dlg_warning.destroy()
            self.dlg_warning_shadow.destroy()
            self.dlg_warning = None
            self.dlg_warning_shadow = None

        self.dlg_warning = OkDialog(
            text=warning,
            state=DGG.NORMAL,
            relief=DGG.RIDGE,
            frameColor=(1,1,1,1),
            scale=300,
            pos=(base.getSize()[0]/2, 0, -base.getSize()[1]/2),
            sortOrder=1,
            button_relief=DGG.FLAT,
            button_frameColor=(0.8, 0.8, 0.8, 1),
            command=close_warning_dialog,
            parent=base.pixel2d)
        self.dlg_warning.set_bin("gui-popup", 0)
        self.dlg_warning_shadow = DirectFrame(
            state=DGG.NORMAL,
            sortOrder=0,
            frameColor=(0,0,0,0.5),
            frameSize=(0, base.getSize()[0], -base.getSize()[1], 0),
            parent=base.pixel2d)

    def __quit(self, selection):
        if selection == 1:
            try:
                self.main_view.terminal_window.close_all()
            except:
                logging.error("Failed to close all terminals. Remaining processes may still exist.", exc_info=(ex_type, ex_value, ex_traceback))
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
        self.dlg_quit.set_bin("gui-popup", 0)
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
            try:
                editor_frame.editor_instance.do_exception_save()
            except:
                logging.error("Failed to save exception save", exc_info=(ex_type, ex_value, ex_traceback))

        try:
            self.main_view.terminal_window.close_all()
        except:
            logging.error("Failed to close all terminals. Remaining processes may still exist.", exc_info=(ex_type, ex_value, ex_traceback))
