from DirectGuiExtension.DirectAutoSizer import DirectAutoSizer
from DirectGuiExtension.DirectBoxSizer import DirectBoxSizer
from direct.gui.DirectScrolledFrame import DirectScrolledFrame
from direct.gui.DirectLabel import DirectLabel
from direct.gui.DirectButton import DirectButton
from direct.gui import DirectGuiGlobals as DGG
from DirectGuiExtension import DirectGuiHelper as DGH
import subprocess
import asyncio
import sys
from dataclasses import dataclass
from panda3d.core import TextNode

@dataclass
class PackageData:
    name: str
    version_current: str = "-"
    version_new: str = ""

class EditorEntry:
    def __init__(self, parent_box, editor_display_name, editor_description, package_data, update_package_info_func, even=True):
        color_shift = 0
        if even:
            color_shift = 0.15

        default_text_scale = 14

        self.package_data = package_data
        self.update_package_info_func = update_package_info_func
        self.content_box = DirectBoxSizer(
            frameSize=(0,1030,-100,0),
            autoUpdateFrameSize=False,
            frameColor=(
                0.8 + color_shift,
                0.8 + color_shift,
                0.8 + color_shift,
                1),
            #itemMargin=(5,5,2,2),
            itemAlign=DirectBoxSizer.A_Middle)
        parent_box.addItem(self.content_box)
        #self.content_box.set_x(100)
        #self.content_box.set_z(-50)

        lbl_header = DirectLabel(
            text=editor_display_name,
            frameSize=(-5,200,-50,50),
            frameColor=(
                0.35 + color_shift,
                0.35 + color_shift,
                0.35 + color_shift,
                1),
            text_fg=(1,1,1,1),
            text_scale=20,
            text_align=TextNode.ALeft)
        self.content_box.addItem(lbl_header)

        self.lbl_description = DirectLabel(
            text=editor_description,
            frameSize=(-5,550,-50,50),
            frameColor=(0,0,0,0),
            text_scale=default_text_scale,
            text_align=TextNode.ALeft)
        self.content_box.addItem(self.lbl_description)

        self.lbl_version = DirectLabel(
            text="0.0.0",
            frameSize=(-5,50,-50,50),
            frameColor=(0,0,0,0),
            text_scale=default_text_scale,
            text_align=TextNode.ALeft)
        self.content_box.addItem(self.lbl_version)
        self.lbl_upgrade = DirectLabel(
            text="Not Installed",
            frameSize=(-5,100,-50,50),
            frameColor=(0,0,0,0),
            text_scale=default_text_scale,
            text_align=TextNode.ALeft)
        self.content_box.addItem(self.lbl_upgrade)

        btn_color = (
            (0.5, 0.5, 0.5, 1),    # normal
            (0.55, 0.55, 0.55, 1), # click
            (0.7, 0.7, 0.7, 1),    # hover
            (0.25, 0.25, 0.25, 1)) # disabled

        self.btn_action = DirectButton(
            text="Install",
            pad=(5,5),
            frameColor=btn_color,
            relief=DGG.FLAT,
            text_scale=12,
            text_fg=(1,1,1,1),
            )
        self.content_box.addItem(self.btn_action)

        self.btn_remove = DirectButton(
            text="Remove",
            borderWidth=(2,2),
            pad=(5,5),
            frameColor=btn_color,
            relief=DGG.FLAT,
            text_scale=12,
            text_fg=(1,1,1,1),
            command=self.uninstall,
            )
        self.content_box.addItem(self.btn_remove)

    def set_package_info(self, installed, outdated):
        self.installed_packages_dict = installed
        self.outdated_packages_dict = outdated
        if self.need_update():
            self.package_data = self.outdated_packages_dict[self.package_data.name]
        elif self.is_installed():
            self.package_data = self.installed_packages_dict[self.package_data.name]
        self.set_button()

    def install(self):
        print("INSTALL")
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "--user",
            self.package_data.name])
        self.update_package_info_func()

    def update(self):
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "-U", "--user",
            self.package_data.name])
        self.update_package_info_func()

    def uninstall(self):
        print("UNINSTALL")
        subprocess.check_call(
            [sys.executable, "-m", "pip", "uninstall", "-y",
            self.package_data.name])
        self.update_package_info_func()

    def set_button(self):
        self.lbl_version.setText(self.package_data.version_current)
        self.lbl_version.setFrameSize(True)
        upgrade_text = "Not Installed"
        if self.is_installed():
            upgrade_text = "Up-To-Date"
            if self.package_data.version_new != "":
                upgrade_text = f"New Version:\n{self.package_data.version_new}"
        self.lbl_upgrade.setText(upgrade_text)
        self.lbl_upgrade.setFrameSize(True)

        self.btn_action["state"] = DGG.NORMAL
        if self.is_installed():
            if self.need_update():
                self.btn_action["text"] = "Update"
                self.btn_action["command"] = self.update
            else:
                self.btn_action["text"] = "Install"
                self.btn_action["state"] = DGG.DISABLED
        else:
            self.btn_action["text"] = "Install"
            self.btn_action["command"] = self.install

        self.content_box.refresh()

    def is_installed(self):
        return self.package_data.name in self.installed_packages_dict.keys()

    def need_update(self):
        return self.package_data.name in self.outdated_packages_dict.keys()

class EditorStore:
    def __init__(self, parent):
        self.outdated_packages_dict = {}
        self.installed_packages_dict = {}

        self.initial_setup = True

        # our root element for the main box
        self.main_sizer = DirectAutoSizer(parent)

        color = (
            (0.8, 0.8, 0.8, 1),  # Normal
            (0.9, 0.9, 1, 1),  # Click
            (0.8, 0.8, 1, 1),  # Hover
            (0.5, 0.5, 0.5, 1))  # Disabled
        self.store_frame = DirectScrolledFrame(
            frameSize=(0,1,-1,0),
            frameColor=(0.25, 0.25, 0.25, 1),
            scrollBarWidth=20,
            verticalScroll_scrollSize=20,
            verticalScroll_thumb_relief=DGG.FLAT,
            verticalScroll_incButton_relief=DGG.FLAT,
            verticalScroll_decButton_relief=DGG.FLAT,
            verticalScroll_thumb_frameColor=color,
            verticalScroll_incButton_frameColor=color,
            verticalScroll_decButton_frameColor=color,
            horizontalScroll_thumb_relief=DGG.FLAT,
            horizontalScroll_incButton_relief=DGG.FLAT,
            horizontalScroll_decButton_relief=DGG.FLAT,
            horizontalScroll_thumb_frameColor=color,
            horizontalScroll_incButton_frameColor=color,
            horizontalScroll_decButton_frameColor=color,
            state=DGG.NORMAL)

        self.main_sizer.setChild(self.store_frame)

        #self.content_sizer = DirectAutoSizer(self.store_frame.canvas)
        self.content_box = DirectBoxSizer(
            self.store_frame.canvas,
            frameColor=(0,0,0,0),
            orientation=DGG.VERTICAL,
            #autoUpdateFrameSize=False
            )
        #self.content_sizer.setChild(self.content_box)

        self.lbl_loading = DirectLabel(
            self.store_frame,
            frameColor=(0,0,0,0),
            text_fg=(1,1,1,1),
            pos=(
                DGH.getRealWidth(self.store_frame)/2,
                0,
                -DGH.getRealHeight(self.store_frame)/2),
            text="LOADING...",
            scale=100)

        self.lbl_notice = DirectLabel(
            frameColor=(0,0,0,0),
            text_fg=(1,1,1,1),
            pad=(5,5),
            pos=(
                DGH.getRealWidth(self.store_frame)/2,
                0,
                -DGH.getRealHeight(self.store_frame)/2),
            text_align=TextNode.ALeft,
            text="NOTE: FRAME needs to be restarted to load up newly installed editors.",
            text_scale=14)
        self.content_box.addItem(self.lbl_notice)

        self.entries = []
        self.add_store_entries()

    def add_entry_header(self, text):
        header = DirectLabel(
            frameColor=(0,0,0,0),
            text_fg=(1,1,1,1),
            pad=(5,5),
            pos=(
                DGH.getRealWidth(self.store_frame)/2,
                0,
                -DGH.getRealHeight(self.store_frame)/2),
            text_align=TextNode.ALeft,
            text=text,
            text_scale=20)
        self.content_box.addItem(header)


    def add_store_entries(self):
        self.add_entry_header(":Editors:")
        entry = EditorEntry(
            self.content_box,
            "Scene Editor",
            "Create and edit sceneries for your Panda3D applications\nLoad and place models, collision solids and much more.",
            PackageData("SceneEditor"),
            self.update_package_info,
            False)
        self.entries.append(entry)

        entry = EditorEntry(
            self.content_box,
            "Gui Designer",
            "Design graphical user interfaces with\nPanda3Ds DirectGUI system",
            PackageData("DirectGuiDesigner"),
            self.update_package_info)
        self.entries.append(entry)

        self.add_entry_header(":Core:")
        entry = EditorEntry(
            self.content_box,
            "Direct GUI Extensions",
            "Extension toolkit for Panda3Ds DirectGUI system\nImportant: Do not uninstall this, it is vital for FRAME.",
            PackageData("DirectGuiExtension"),
            self.update_package_info,
            False)
        self.entries.append(entry)

        entry = EditorEntry(
            self.content_box,
            "Folder Browser",
            "A folder browser extension for DirectGUI\nImportant: Do not uninstall this, it is vital for FRAME.",
            PackageData("DirectFolderBrowser"),
            self.update_package_info)
        self.entries.append(entry)

        cs = self.content_box["frameSize"]
        self.store_frame["canvasSize"] = [cs[0], cs[1], cs[2] - 50, cs[3]]

    def update_package_info(self):
        self.lbl_loading.show()
        self.installed_packages_gathered = False
        self.outdated_packages_gathered = False
        taskMgr.doMethodLater(
            0.5,
            asyncio.run,
            "gather packages",
            extraArgs=[self.gather_all_packages()])

    def update_entries(self):
        for entry in self.entries:
            entry.set_package_info(
                self.installed_packages_dict,
                self.outdated_packages_dict)

    def update_package_info_done(self):
        if self.installed_packages_gathered and self.outdated_packages_gathered:
            self.lbl_loading.hide()

    def __get_filtered_pip_data(self, package_string):
        # split by spaces
        package_data_list = package_string.split(" ")
        # remove empty parts in the list
        filtered_list = list(filter(None, package_data_list))
        # Check if the entry has the desired number of parts
        return filtered_list

    async def get_pip_output_as_list(self, args_list):
        cmd = " ".join([sys.executable, "-m", "pip"] + args_list)
        proc = await asyncio.create_subprocess_shell(
            cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE)

        stdout, stderr = await proc.communicate()

        ret_list = []
        if stdout:
            ret_list = stdout.decode().split("\n")[2:]
        return ret_list

    async def get_installed_packages(self):
        output_list = await self.get_pip_output_as_list(["list"])
        self.installed_packages_dict = {}
        for package in output_list:
            filtered_list = self.__get_filtered_pip_data(package)
            # Check if the entry has the desired number of parts
            if len(filtered_list) < 2:
                continue
            # add the package data
            data = PackageData(
                filtered_list[0],
                filtered_list[1],
                "")
            self.installed_packages_dict[filtered_list[0]] = data
        self.update_entries()
        self.installed_packages_gathered = True
        self.update_package_info_done()


    async def get_outdated_packages(self):
        output_list = await self.get_pip_output_as_list(["list", "-o"])
        self.outdated_packages_dict = {}
        for package in output_list:
            filtered_list = self.__get_filtered_pip_data(package)
            if len(filtered_list) < 3:
                continue
            data = PackageData(
                filtered_list[0],
                filtered_list[1],
                filtered_list[2])
            self.outdated_packages_dict[filtered_list[0]] = data

        self.update_entries()
        self.outdated_packages_gathered = True
        self.update_package_info_done()

    async def gather_all_packages(self):
        get_installed_task = asyncio.create_task(self.get_installed_packages())
        get_outdated_task = asyncio.create_task(self.get_outdated_packages())
        await get_installed_task
        await get_outdated_task

    def is_dirty(self):
        return False

    def enable_editor(self):
        if self.initial_setup:
            self.update_package_info()
            self.initial_setup = False

    def disable_editor(self):
        pass

    def do_exception_save(self):
        # nothing to save here.
        pass
