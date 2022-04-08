import os
import logging
import shutil
from datetime import datetime

FRAME_ROOT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

class FrameProject:
    def __init__(self):
        self.template_path = os.path.join(FRAME_ROOT_PATH, "templates")

    def create_new_project(self, root_path):
        if len(os.listdir(root_path)) != 0:
            logging.error("Selected directory for new project is not empty!")
            return
        app_path = os.path.join(root_path, "gamename")
        os.mkdir(app_path)
        os.mkdir(os.path.join(app_path, "core"))
        os.mkdir(os.path.join(app_path, "assets"))

        with open(os.path.join(root_path, "README.md"), "w") as readme_file:
            readme_file.write("# gamename\n\n")
            readme_file.write("TODO: write me")
        with open(os.path.join(root_path, "LICENSE.txt"), "w") as license_file:
            license_file.write("TODO: Add license text!")
        shutil.copyfile(
            os.path.join(self.template_path, "setup.py"),
            os.path.join(root_path, "setup.py"))
        shutil.copyfile(
            os.path.join(self.template_path, "setup.cfg"),
            os.path.join(root_path, "setup.cfg"))
        shutil.copyfile(
            os.path.join(self.template_path, "requirements.txt"),
            os.path.join(root_path, "requirements.txt"))

        self.__replace_placeholders(os.path.join(root_path, "setup.cfg"))

        self.__copy_code_templates(app_path)

    def __copy_code_templates(self, app_path):
        shutil.copyfile(
            os.path.join(self.template_path, "baseProject", "coreFSM.py"),
            os.path.join(app_path, "core", "coreFSM.py"))
        shutil.copyfile(
            os.path.join(self.template_path, "baseProject", "config.py"),
            os.path.join(app_path, "core", "config.py"))
        shutil.copyfile(
            os.path.join(self.template_path, "baseProject", "main.py"),
            os.path.join(app_path, "main.py"))

        self.__replace_placeholders(os.path.join(app_path, "core", "config.py"))

    def __replace_placeholders(self, filename):
        content = ""
        with open(filename, "r") as edit_file:
            content = edit_file.read()
            content = content.replace("{{COMPANY_NAME}}", "Company Name")
            content = content.replace("{{APP_NAME}}", "gamename")
            content = content.replace("{{DATE_VERSION}}",
                    datetime.now().strftime("%y.%m"))
        with open(filename, "w") as edit_file:
            edit_file.write(content)
