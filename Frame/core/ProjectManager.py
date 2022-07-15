import os
from direct.showbase.DirectObject import DirectObject
from Frame.GUI.ProjectManagement.NewProjectDialogHandler import NewProjectDialogHandler
from Frame.core.FrameProject import FrameProject
from Frame.core.PmanProject import PmanProject
from DirectFolderBrowser.DirectFolderBrowser import DirectFolderBrowser

class ProjectManager(DirectObject):
    def __init__(self, tooltip):
        self.project_type = ""
        self.project = None
        self.tt = tooltip

    def new_project(self):
        self.accept("FRAME_create_project", self.create_new_project)
        self.newProjectDlg = NewProjectDialogHandler(self.tt)

    def create_new_project(self, confirm, path):
        self.newProjectDlg.destroy()
        if not confirm:
            self.newProjectDlg = None
            return

        self.project_type = self.newProjectDlg.project_type
        if self.project_type == "pman":
            self.project = PmanProject()
            self.project.create_new_project(path)
        else:
            self.project_type = "FRAME"
            self.project = FrameProject()

            self.project.create_new_project(
                path,
                self.newProjectDlg.project_name,
                self.newProjectDlg.project_template)
        self.newProjectDlg = None

    def run_project(self):
        if self.project is None:
            base.messenger.send("FRAME_show_warning", ["No Project loaded"])
            return
        self.project.run_project()

    def load_project(self):
        def select_project_path(confirm):
            if confirm:
                if self.project is not None:
                    self.close()
                path = self.browser.get()
                if os.path.exists(os.path.join(path, ".pman")):
                    self.project_type = "pman"
                    self.project = PmanProject()
                    self.project.load_project(self.browser.get())
                else:
                    self.project_type = "FRAME"
                    self.project = FrameProject()
                    self.project.load_project(self.browser.get())
            self.browser.hide()
            self.browser = None
        self.browser = DirectFolderBrowser(
            select_project_path,
            False,
            "",
            "",
            tooltip=self.tt)
        self.browser.show()

    def close(self):
        self.project.close()
        self.project = None
