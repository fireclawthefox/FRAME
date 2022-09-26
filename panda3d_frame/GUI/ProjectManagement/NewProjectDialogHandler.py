from panda3d_frame.GUI.ProjectManagement.NewProjectDialog import GUI as NewProjectDialog
from panda3d.core import ConfigVariableBool
from DirectFolderBrowser.DirectFolderBrowser import DirectFolderBrowser

class NewProjectDialogHandler(NewProjectDialog):
    def __init__(self, tooltip):
        NewProjectDialog.__init__(self, base.pixel2d)
        self.frmCreateProject.set_bin("gui-popup", 0)

        self.tt = tooltip

        project_types = ["FRAME"]
        if ConfigVariableBool("use-pman-project", False).getValue():
            project_types.append("pman")
        self.projectType["items"] = project_types
        self.projectType.resetFrameSize()

        self.btnOk["command"] = self.accept
        self.btnCancel["command"] = self.cancel

        self.projectType["command"] = self.project_type_changed

        self.frmCreateProject.set_pos(
            base.getSize()[0]/2,
            0,
            -base.getSize()[1]/2)
        self.project_type_changed("FRAME")

    def accept(self):
        self.hide()
        def select_project_path(confirm):

            self.project_type = self.projectType.get()
            self.project_name = self.txtName.get()
            self.project_company = self.txtCompany.get()
            self.project_template = self.template.get()
            print(self.project_type)
            print(self.project_template)

            base.messenger.send(
                "FRAME_create_project",
                [confirm, self.browser.get()])
            self.browser.hide()
            self.browser = None
        self.browser = DirectFolderBrowser(
            select_project_path,
            False,
            "",
            "",
            tooltip=self.tt)
        self.browser.show()

    def cancel(self):
        base.messenger.send(
            "FRAME_create_project",
                [False, ""])

    def project_type_changed(self, project_type):
        if project_type == "pman":
            self.template["items"] = ["Simple"]
        else:
            self.template["items"] = ["Simple", "Multiplayer"]
