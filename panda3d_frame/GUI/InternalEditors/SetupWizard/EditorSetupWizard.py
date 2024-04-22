#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, os, logging
import configparser
import importlib

from direct.showbase.DirectObject import DirectObject

from panda3d.core import TextNode
from direct.gui import DirectGuiGlobals as DGG
from direct.gui.DirectCheckButton import DirectCheckButton
from direct.gui.DirectDialog import OkDialog

from panda3d_frame.GUI.InternalEditors.SetupWizard.wizardMainGUI import GUI as MainGUI
from panda3d_frame.GUI.InternalEditors.SetupWizard.wizardPatternElement import GUI as PatternElement
from panda3d_frame.GUI.InternalEditors.SetupWizard.wizardApplicationElement import GUI as ApplicationElement
from panda3d_frame.GUI.InternalEditors.SetupWizard.wizardProcessingScreen import GUI as ProcessingScreen

from DirectGuiExtension.DirectTooltip import DirectTooltip
from DirectFolderBrowser.DirectFolderBrowser import DirectFolderBrowser

PLUGIN_LIBS = [
    "p3vision",
    "p3vrpn",
    "p3windisplay",
    "panda",
    "pandaai",
    "pandabullet",
    "pandaegg",
    "pandaexpress",
    "pandafx",
    "pandagl",
    "pandaode",
    "pandaphysics",
    "pandaskel",
    "p3assimp",
    "p3direct",
    "p3dtool",
    "p3dtoolconfig",
    "p3ffmpeg",
    "p3fmod_audio",
    "p3interrogatedb",
    "p3openal_audio",
    "p3ptloader",
    "p3tinydisplay"]

DEFAULT_PLUGINS = [
    "pandagl",
    "p3openal_audio"
]

class EditorSetupWizard(DirectObject):
    def __init__(self, parent):

        self.filePath = "~/setup.cfg"

        self.setup_config = configparser.ConfigParser()
        self.include_patterns = []
        self.exclude_patterns = []
        self.applications = []
        self.plugins = []

        self.tt = DirectTooltip(
            text = "Tooltip",
            #text_fg = (1,1,1,1),
            pad=(0.2, 0.2),
            scale = 16,
            text_align = TextNode.ALeft,
            frameColor = (1, 1, 0.7, 1),
            parent=base.pixel2d,
            sortOrder=1000)

        # setup main gui window
        self.main_gui = MainGUI(parent)

        self.processingScreen = ProcessingScreen(parent)
        self.processingScreen.frmProcessing["state"] = DGG.NORMAL
        self.processingScreen.frmProcessing.hide()

        self.loadPlugins()
        for plugin in self.plugins:
            if plugin["text"] in DEFAULT_PLUGINS:
                plugin["indicatorValue"] = True

        # catch GUI events
        self.accept("p3d_setup_wizard_addApplication", self.addApplication)
        self.accept("p3d_setup_wizard_deploy", self.deploy)
        self.accept("p3d_setup_wizard_load", self.load)
        self.accept("p3d_setup_wizard_save", self.save)
        self.accept("p3d_setup_wizard_addIncludePattern", self.addIncludePattern)
        self.accept("p3d_setup_wizard_addExcludePattern", self.addExcludePattern)

        # PLATFORM SUPPORT: Android support is currently not fully available
        self.main_gui.lblMobile.hide()
        self.main_gui.cbAndroid.hide()

        # Add some default entries
        self.main_gui.txtVersion.set("0.0.0")

        self.addIncludePattern()
        self.include_patterns[0].txtPattern.set("**/*.png")

        self.addApplication()
        self.applications[0].txtName.set("Name")
        self.applications[0].txtPath.set("main.py")

        self.main_gui.cbOptimizedWheels["indicatorValue"] = True

        # select the first tab
        #self.main_gui.rbMetadata.check()

        self.loadBrowser = DirectFolderBrowser(self.loadExecute, True, defaultFilename="setup.cfg", tooltip=self.tt, title="Load setup config", fileExtensions=[".cfg"])
        self.loadBrowser.hide()
        self.saveBrowser = DirectFolderBrowser(self.saveExecute, True, defaultFilename="setup.cfg", tooltip=self.tt, title="Save setup config", fileExtensions=[".cfg"])
        self.saveBrowser.hide()
        self.deployBrowser = DirectFolderBrowser(self.deployExecute, True, defaultFilename="setup.py", tooltip=self.tt, title="Select setup.py script", fileExtensions=[".py"])
        self.deployBrowser.hide()

    def deploy(self):
        self.deployBrowser.folderMoveIn(os.path.dirname(self.filePath))
        self.deployBrowser.show()

    def deployExecute(self, ok):
        self.deployBrowser.hide()
        if not ok:
            return

        self.processingScreen.frmProcessing.show()
        base.graphicsEngine.renderFrame()
        base.graphicsEngine.renderFrame()

        script = self.deployBrowser.get()

        #
        # Check if we have an existing python script
        # create it if we don't
        #
        if not os.path.exists(script):
            with open(script, 'w') as py_setup_script:
                py_setup_script.write("from setuptools import setup\n")
                py_setup_script.write("setup()\n")

        #
        # Check if we have a requirements.txt file
        #
        if self.setup_config.get("build_apps", "requirements_path", fallback="") == "":
            # create a default requirements.txt
            with open(os.path.join(os.path.dirname(script), "requirements.txt"), 'w') as requirements:
                requirements.write("panda3d")

        #
        # Run the setup python script
        #
        hasError = False
        folder_name = os.path.realpath(os.path.dirname(script))
        old_location = os.curdir
        try:
            os.chdir(folder_name)
            preArgv = sys.argv
            sys.argv = [os.path.split(script)[1], "bdist_apps"]
            pythonFilePath = script
            spec = importlib.util.spec_from_file_location("", pythonFilePath)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            sys.argv = preArgv
        except Exception as e:
            logging.exception(f"Failed to run setup {script}")
            hasError = True
            dlg = OkDialog(
                frameColor=(1.0, 0.0, 0.0, 1.0),
                frameSize=(-0.5, 0.5, -0.3, 0.1),
                pos=(250, 0, -200),
                scale=(300, 300, 300),
                state=DGG.NORMAL,
                relief=DGG.RIDGE,
                text="Error while building packages!\nSee terminal output for more\ninformation.",
                text_align=TextNode.A_center,
                text_fg=(1, 1, 1, 1),
                parent=base.pixel2d
            )
            dlg["text_pos"] = (0, -0.005)
            dlg.buttonList[0].setZ(dlg.buttonList[0], 0.025)
            dlg["Button0_frameSize"] = (-0.1, 0.1, -0.017, 0.05)
            def destroyDlg(args):
                dlg.destroy()
            dlg["command"] = destroyDlg
            dlg.show()
        finally:
            os.chdir(old_location)

        if not hasError:
            dlg = OkDialog(
                frameColor=(0.2, 0.9, 0.2, 1.0),
                frameSize=(-0.3, 0.3, -0.3, 0.1),
                pos=(250, 0, -200),
                scale=(300, 300, 300),
                state=DGG.NORMAL,
                relief=DGG.RIDGE,
                text="Build Successful!",
                text_align=TextNode.A_center,
                parent=base.pixel2d
            )
            dlg["text_pos"] = (0, -0.005)
            dlg.buttonList[0].setZ(dlg.buttonList[0], 0.025)
            dlg["Button0_frameSize"] = (-0.1, 0.1, -0.017, 0.05)
            def destroyDlg(args):
                dlg.destroy()
            dlg["command"] = destroyDlg
            dlg.show()

        self.processingScreen.frmProcessing.hide()

    def load(self):
        self.loadBrowser.folderMoveIn(os.path.dirname(self.filePath))
        self.loadBrowser.show()

    def loadExecute(self, ok):
        if not ok:
            self.loadBrowser.hide()
            return
        self.filePath = self.loadBrowser.get()
        self.setup_config.read(self.filePath)

        #
        # Clear and load metadata
        #
        self.main_gui.txtAppName.set(self.setup_config.get("metadata", "name", fallback=""))
        self.main_gui.txtAuthor.set(self.setup_config.get("metadata", "author", fallback=""))
        self.main_gui.txtVersion.set(self.setup_config.get("metadata", "version", fallback=""))

        #
        # Clear and load include patterns
        #
        while len(self.include_patterns) > 0:
            self.removeIncludePattern(0)
        inc_pattern = self.setup_config.get("build_apps", "include_patterns", fallback="")
        idx = 0
        if inc_pattern != "":
            for pattern in inc_pattern.strip().split("\n"):
                self.addIncludePattern()
                self.include_patterns[idx].txtPattern.set(pattern)
                idx += 1

        #
        # Clear and load exclude patterns
        #
        while len(self.exclude_patterns) > 0:
            self.removeExcludePattern(0)
        exc_pattern = self.setup_config.get("build_apps", "exclude_patterns", fallback="")
        idx = 0
        if exc_pattern != "":
            for pattern in exc_pattern.strip().split("\n"):
                self.addExcludePattern()
                self.exclude_patterns[idx].txtPattern.set(pattern)
                idx += 1

        #
        # Clear and load applications
        #
        while len(self.applications) > 0:
            self.removeApplication(0)
        gui_applications = self.setup_config.get("build_apps", "gui_apps", fallback="")
        idx = 0
        if gui_applications != "":
            for application in gui_applications.strip().split("\n"):
                name, path = gui_applications.split("=")
                self.addApplication()
                self.applications[idx].txtName.set(name.strip())
                self.applications[idx].txtPath.set(path.strip())
                idx += 1

        console_applications = self.setup_config.get("build_apps", "console_apps", fallback="")
        if console_applications != "":
            for applicatin in console_applications.strip().split("\n"):
                name, path = console_applications.split("=")
                self.addApplication()
                self.applications[idx].txtName.set(name.strip())
                self.applications[idx].txtPath.set(path.strip())
                self.applications[idx].cbTerminalApp["indicatorValue"] = True
                idx += 1

        #
        # Clear and load platforms
        #
        platforms = self.setup_config.get("build_apps", "platforms", fallback="")
        self.main_gui.cbLinux["indicatorValue"] = False
        self.main_gui.cbMacOS["indicatorValue"] = False
        self.main_gui.cbWindows["indicatorValue"] = False
        self.main_gui.cbAndroid["indicatorValue"] = False
        if platforms != "":
            split_platforms = platforms.strip().split("\n")
            if "manylinux2010_x86_64" in split_platforms:
                self.main_gui.cbLinux["indicatorValue"] = True
            if "macosx_10_9_x86_64" in split_platforms:
                self.main_gui.cbMacOS["indicatorValue"] = True
            if "win_amd64" in split_platforms:
                self.main_gui.cbWindows["indicatorValue"] = True
        else:
            # Default selection
            self.main_gui.cbLinux["indicatorValue"] = True
            self.main_gui.cbMacOS["indicatorValue"] = True
            self.main_gui.cbWindows["indicatorValue"] = True

        #
        # Clear and load plugins
        #
        plugins = self.setup_config.get("build_apps", "plugins", fallback="")
        for plugin in self.plugins:
            plugin["indicatorValue"] = False
        if plugins != "":
            split_plugins = plugins.strip().split("\n")
            for plugin in self.plugins:
                if plugin["text"] in split_plugins:
                    plugin["indicatorValue"] = True
        else:
            for plugin in self.plugins:
                if plugin["text"] in DEFAULT_PLUGINS:
                    plugin["indicatorValue"] = True

        self.main_gui.txtBuildBase.set(self.setup_config.get("build_apps", "build_base", fallback=""))
        self.main_gui.txtRequirementsPaths.set(self.setup_config.get("build_apps", "requirements_path", fallback=""))
        self.main_gui.cbOptimizedWheels["indicatorValue"] = self.setup_config.getboolean("build_apps", "use_optimized_wheels", fallback=True)
        self.main_gui.txtOptimizedWheelsIndex.set(self.setup_config.get("build_apps", "optimized_wheel_index", fallback=""))
        self.main_gui.txtDistDir.set(self.setup_config.get("bdist_apps", "dist_dir", fallback=""))

        self.loadBrowser.hide()

    def save(self):
        self.saveBrowser.folderMoveIn(os.path.dirname(self.filePath))
        self.saveBrowser.show()

    def saveExecute(self, ok):
        if not ok:
            self.saveBrowser.hide()
            return
        self.filePath = self.saveBrowser.get()

        #
        # METADATA
        #
        self.setup_config["metadata"] = {}
        self.setup_config["metadata"]["name"] = self.main_gui.txtAppName.get()
        self.setup_config["metadata"]["author"] = self.main_gui.txtAuthor.get()
        self.setup_config["metadata"]["version"] = self.main_gui.txtVersion.get()

        #
        # BUILD APPS
        #
        self.setup_config["build_apps"] = {}

        #
        # include patterns
        #
        inc_pattern = ""
        for patternElement in self.include_patterns:
            inc_pattern += patternElement.txtPattern.get() + "\n"
        if inc_pattern != "":
            self.setup_config["build_apps"]["include_patterns"] = inc_pattern.rstrip()

        #
        # exclude patterns
        #
        exc_pattern = ""
        for patternElement in self.exclude_patterns:
            exc_pattern += patternElement.txtPattern.get() + "\n"
        if exc_pattern != "":
            self.setup_config["build_apps"]["exclude_patterns"] = exc_pattern.rstrip()

        #
        # GUI and console apps
        #
        gui_applications = ""
        console_applications = ""
        for applicationElement in self.applications:
            entry = applicationElement.txtName.get() + "=" + applicationElement.txtPath.get() + "\n"
            if applicationElement.cbTerminalApp["indicatorValue"]:
                console_applications += entry
            else:
                gui_applications += entry
        self.setup_config["build_apps"]["gui_apps"] = gui_applications.rstrip()
        self.setup_config["build_apps"]["console_apps"] = console_applications.rstrip()

        #
        # plugins
        #
        plugins = ""
        for plugin in self.plugins:
            if plugin["indicatorValue"]:
                plugins += plugin["text"] + "\n"
        self.setup_config["build_apps"]["plugins"] = plugins.rstrip()

        #
        # platforms
        #
        platforms = ""
        if self.main_gui.cbLinux["indicatorValue"]:
            platforms += "manylinux2010_x86_64\n"
        if self.main_gui.cbMacOS["indicatorValue"]:
            platforms += "macosx_10_9_x86_64\n"
        if self.main_gui.cbWindows["indicatorValue"]:
            platforms += "win_amd64\n"
        #if self.main_gui.cbAndroid["indicatorValue"]:
        #    platforms += "android\n"
        self.setup_config["build_apps"]["platforms"] = platforms.rstrip()

        #
        # Advanced stuff
        #
        buildBase = self.main_gui.txtBuildBase.get()
        if buildBase != "":
            self.setup_config["build_apps"]["build_base"] = buildBase
        requirementsPaths = self.main_gui.txtRequirementsPaths.get()
        if requirementsPaths != "":
            self.setup_config["build_apps"]["requirements_paths"] = requirementsPaths
        if not self.main_gui.cbOptimizedWheels["indicatorValue"]:
            self.setup_config["build_apps"]["use_optimized_wheels"] = str(self.main_gui.cbOptimizedWheels["indicatorValue"])
        optimizedWheelsIndex = self.main_gui.txtOptimizedWheelsIndex.get()
        if optimizedWheelsIndex != "":
            self.setup_config["build_apps"]["optimized_wheel_index"] = optimizedWheelsIndex

        #
        # DISTRIBUTE APPS
        #
        self.setup_config["bdist_apps"] = {}

        #
        # Advanced stuff
        #
        distDir = self.main_gui.txtDistDir.get()
        if distDir != "":
            self.setup_config["bdist_apps"]["dist_dir"] = distDir

        #
        # SAVE SETUP CONFIG FILE
        #
        with open(self.filePath, 'w') as configfile:
            self.setup_config.write(configfile)

        # finally hide the browser
        self.saveBrowser.hide()

    def loadPlugins(self):
        z = 10
        for i in range(len(PLUGIN_LIBS)):
            if i%2 == 0:
                z -= 20

            x = i%2 * 200 - 125
            self.plugins.append(DirectCheckButton(
                pos=(x,0,z),
                pad=(4,4),
                text_align=TextNode.ALeft,
                text_scale=24,
                borderWidth=(0, 0),
                text=PLUGIN_LIBS[i],
                indicator_text_scale=24,
                indicator_borderWidth=(2, 2),
                parent=self.main_gui.frmPluginSelection.getCanvas(),
                scale=0.5))
            self.plugins[-1].indicator["text"] = (" ", "X")
        cs = self.main_gui.frmPluginSelection["canvasSize"]
        self.main_gui.frmPluginSelection["canvasSize"] = (
            cs[0], cs[1], z, cs[3])

    def addApplication(self):
        element_id = len(self.applications)

        element = ApplicationElement(self.main_gui.frmApplicationSelection.getCanvas())
        element.txtName.setZ(element.txtName.getZ() - element_id * 24)
        element.txtPath.setZ(element.txtPath.getZ() - element_id * 24)
        element.cbTerminalApp.setZ(element.cbTerminalApp.getZ() - element_id * 24)
        element.btnRemove.setZ(element.btnRemove.getZ() - element_id * 24)
        element.btnRemove["command"] = self.removeApplication
        element.btnRemove["extraArgs"] = [element_id]

        self.applications.append(element)

        # recalculate the canvas of the Include Pattern frame
        cs = self.main_gui.frmApplicationSelection["canvasSize"]
        self.main_gui.frmApplicationSelection["canvasSize"] = (
            cs[0], cs[1], element_id * -27, cs[3])
        self.main_gui.frmApplicationSelection.setCanvasSize()

    def removeApplication(self, application_index):
        self.applications[application_index]

        for i in range(len(self.applications)):
            if i == application_index:
                element = self.applications[i]
                element.txtName.destroy()
                element.txtPath.destroy()
                element.cbTerminalApp.destroy()
                element.btnRemove.destroy()
            elif i > application_index:
                newIndex = i-1
                element = self.applications[i]
                element.txtName.setZ(element.txtName.getZ() + 24)
                element.txtPath.setZ(element.txtPath.getZ() + 24)
                element.cbTerminalApp.setZ(element.cbTerminalApp.getZ() + 24)
                element.btnRemove.setZ(element.btnRemove.getZ() + 24)
                element.btnRemove["extraArgs"] = [newIndex]
                self.applications[newIndex] = self.applications[i]

        # rmove the last, now empty index
        del self.applications[-1]

        # recalculate the canvas of the Include Pattern frame
        cs = self.main_gui.frmApplicationSelection["canvasSize"]
        self.main_gui.frmApplicationSelection["canvasSize"] = (
            cs[0], cs[1], len(self.applications) * 24, cs[3])
        self.main_gui.frmApplicationSelection.setCanvasSize()

    def addIncludePattern(self):
        element_id = len(self.include_patterns)

        element = PatternElement(self.main_gui.frmIncludePatterns.getCanvas())
        element.txtPattern.setZ(element.txtPattern.getZ() - element_id * 24)
        element.btnRemove.setZ(element.btnRemove.getZ() - element_id * 24)
        element.btnRemove["command"] = self.removeIncludePattern
        element.btnRemove["extraArgs"] = [element_id]

        self.include_patterns.append(element)

        # recalculate the canvas of the Include Pattern frame
        cs = self.main_gui.frmIncludePatterns["canvasSize"]
        self.main_gui.frmIncludePatterns["canvasSize"] = (
            cs[0], cs[1], element_id * -27, cs[3])
        self.main_gui.frmIncludePatterns.setCanvasSize()

    def removeIncludePattern(self, pattern_index):
        self.include_patterns[pattern_index]

        for i in range(len(self.include_patterns)):
            if i == pattern_index:
                element = self.include_patterns[i]
                element.txtPattern.destroy()
                element.btnRemove.destroy()
            elif i > pattern_index:
                newIndex = i-1
                element = self.include_patterns[i]
                element.txtPattern.setZ(element.txtPattern.getZ() + 24)
                element.btnRemove.setZ(element.btnRemove.getZ() + 24)
                element.btnRemove["extraArgs"] = [newIndex]
                self.include_patterns[newIndex] = self.include_patterns[i]

        # rmove the last, now empty index
        del self.include_patterns[-1]

        # recalculate the canvas of the Include Pattern frame
        cs = self.main_gui.frmIncludePatterns["canvasSize"]
        self.main_gui.frmIncludePatterns["canvasSize"] = (
            cs[0], cs[1], len(self.include_patterns) * 24, cs[3])
        self.main_gui.frmIncludePatterns.setCanvasSize()

    def addExcludePattern(self):
        element_id = len(self.exclude_patterns)

        element = PatternElement(self.main_gui.frmExcludePatterns.getCanvas())
        element.txtPattern.setZ(element.txtPattern.getZ() - element_id * 24)
        element.btnRemove.setZ(element.btnRemove.getZ() - element_id * 24)
        element.btnRemove["command"] = self.removeExcludePattern
        element.btnRemove["extraArgs"] = [element_id]

        self.exclude_patterns.append(element)

        # recalculate the canvas of the Exclude Pattern frame
        cs = self.main_gui.frmExcludePatterns["canvasSize"]
        self.main_gui.frmExcludePatterns["canvasSize"] = (
            cs[0], cs[1], element_id * -27, cs[3])
        self.main_gui.frmExcludePatterns.setCanvasSize()

    def removeExcludePattern(self, pattern_index):
        self.exclude_patterns[pattern_index]

        for i in range(len(self.exclude_patterns)):
            if i == pattern_index:
                element = self.exclude_patterns[i]
                element.txtPattern.destroy()
                element.btnRemove.destroy()
            elif i > pattern_index:
                newIndex = i-1
                element = self.exclude_patterns[i]
                element.txtPattern.setZ(element.txtPattern.getZ() + 24)
                element.btnRemove.setZ(element.btnRemove.getZ() + 24)
                element.btnRemove["extraArgs"] = [newIndex]
                self.exclude_patterns[newIndex] = self.exclude_patterns[i]

        # rmove the last, now empty index
        del self.exclude_patterns[-1]

        # recalculate the canvas of the Exclude Pattern frame
        cs = self.main_gui.frmExcludePatterns["canvasSize"]
        self.main_gui.frmExcludePatterns["canvasSize"] = (
            cs[0], cs[1], len(self.exclude_patterns) * 24, cs[3])
        self.main_gui.frmExcludePatterns.setCanvasSize()

    def is_dirty(self):
        return False

    def enable_editor(self):
        pass

    def disable_editor(self):
        pass

    def do_exception_save(self):
        # nothing to save here.
        pass
