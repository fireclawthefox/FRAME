import os
import sys
import logging
import shutil
import subprocess
import json
from datetime import datetime
from panda3d.core import Filename

FRAME_ROOT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

class FrameProject:
    def __init__(self):
        main_dir = Filename(base.main_dir).to_os_specific()
        self.template_path = os.path.join(FRAME_ROOT_PATH, "templates")
        self.project_path = ""
        self.game_name = ""
        self.company_name = ""
        self.template_type = ""
        self.client_process = None
        self.server_process = None

    def create_new_project(
            self,
            root_path,
            game_name="gamename",
            company_name="Company Name",
            template_type="simple"):
        if len(os.listdir(root_path)) != 0:
            logging.error("Selected directory for new project is not empty!")
            base.messenger.send(
                "FRAME_show_warning",
                ["Project creation failed!\nSelected directory for new project is not empty!"])
            return
        app_path = os.path.join(root_path, game_name)
        self.game_name = game_name
        self.company_name = company_name
        self.template_type = template_type
        os.mkdir(app_path)
        os.mkdir(os.path.join(app_path, "assets"))

        with open(os.path.join(root_path, "README.md"), "w") as readme_file:
            readme_file.write(f"# {game_name}\n\n")
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

        with open(os.path.join(root_path, "FRAME.project"), "w") as project_file:
            project_json = {}
            project_json["name"] = game_name
            project_json["company"] = company_name
            project_json["type"] = template_type
            json.dump(project_json, project_file, indent=2)

        self.project_path = root_path

    def load(self, project_root_path):
        self.close()
        self.project_path = project_root_path
        project_file_path = os.path.join(project_root_path, "FRAME.project")
        file_content = None
        with open(project_file_path, 'r') as project_file:
            try:
                file_content = json.load(project_file)
            except Exception as e:
                logging.error(f"Couldn't load project file {project_file_path}")
                logging.exception(e)
                base.messenger.send(
                    "FRAME_show_warning",
                    ["Error while loading Project!\nPlease check log files for more information."])
                return

        if file_content is None:
            logging.error(f"Couldn't load project file {project_file_path}")
            return

        self.game_name = file_content["name"] if "name" in file_content else "gamename"
        self.company_name = file_content["company"] if "company" in file_content else "Company Name"
        self.template_type = file_content["type"] if "type" in file_content else "Simple"

    def run_server(self):
        self.stop_server()
        if self.template_type != "Multiplayer":
            base.messenger.send("FRAME_show_warning", ["Not a multiplayer project"])
            return
        main_path = os.path.join(self.project_path, self.game_name, "dedicatedServer.py")
        if not os.path.exists(main_path):
            print(main_path)
            base.messenger.send("FRAME_show_warning", ["Server script not found"])
            return
        try:
            print("RUN SERVER!")
            self.server_process = subprocess.Popen(
                [sys.executable, main_path],
                stdout=subprocess.PIPE)
            #ret = self.server_process.poll()

            base.messenger.send("FRAME_add_terminal_process", ["Server", self.server_process, "FRAME_stop_project_server"])
            #print(ret)
            #print(self.server_process.stdout)
        except Exception as e:
            logging.error("couldn't run server script of project!")
            logging.exception(e)
            base.messenger.send(
                "FRAME_show_warning",
                ["Can't run server."])
            return

    def stop_server(self):
        if self.server_process is not None:
            self.server_process.terminate()
            try:
                self.server_process.communicate()
            except Exception as e:
                # this process is probalby already gone
                pass
        self.server_process = None

    def run_project(self):
        main_path = os.path.join(self.project_path, self.game_name, "main.py")
        if not os.path.exists(main_path):
            return
        self.client_process = subprocess.Popen(
            [sys.executable, main_path],
            stdout=subprocess.PIPE)

        base.messenger.send("FRAME_add_terminal_process", ["App", self.client_process, "FRAME_stop_project"])

    def stop_project(self):
        if self.client_process is not None:
            self.client_process.terminate()
            try:
                self.client_process.communicate()
            except Exception as e:
                # this process is probalby already gone
                pass
        self.client_process = None

    def __copy_code_templates(self, app_path):
        if self.template_type == "Multiplayer":
            self.__copy_multiplayer_template(app_path)
        else:
            self.__copy_base_template(app_path)

    def __copy_multiplayer_template(self, app_path):
        #
        # COPY CLIENT SIDE
        #
        os.mkdir(os.path.join(app_path, "client"))
        os.mkdir(os.path.join(app_path, "client", "core"))
        shutil.copyfile(
            os.path.join(self.template_path, "multiplayerProject", "client", "core", "coreFSM.py"),
            os.path.join(app_path, "client", "core", "coreFSM.py"))
        shutil.copyfile(
            os.path.join(self.template_path, "multiplayerProject", "client", "core", "config.py"),
            os.path.join(app_path, "client", "core", "config.py"))
        shutil.copyfile(
            os.path.join(self.template_path, "multiplayerProject", "client", "ClientRepository.py"),
            os.path.join(app_path, "client", "ClientRepository.py"))
        shutil.copyfile(
            os.path.join(self.template_path, "multiplayerProject", "main.py"),
            os.path.join(app_path, "main.py"))

        #
        # COPY INTERFACES
        #
        os.mkdir(os.path.join(app_path, "interfaces"))
        shutil.copyfile(
            os.path.join(self.template_path, "multiplayerProject", "interfaces", "direct.dc"),
            os.path.join(app_path, "interfaces", "direct.dc"))
        shutil.copyfile(
            os.path.join(self.template_path, "multiplayerProject", "interfaces", "game.dc"),
            os.path.join(app_path, "interfaces", "game.dc"))

        #
        # COPY SERVER SIDE
        #
        os.mkdir(os.path.join(app_path, "server"))
        shutil.copyfile(
            os.path.join(self.template_path, "multiplayerProject", "server", "AIRepository.py"),
            os.path.join(app_path, "server", "AIRepository.py"))
        shutil.copyfile(
            os.path.join(self.template_path, "multiplayerProject", "server", "ServerRepository.py"),
            os.path.join(app_path, "server", "ServerRepository.py"))
        shutil.copyfile(
            os.path.join(self.template_path, "multiplayerProject", "dedicatedServer.py"),
            os.path.join(app_path, "dedicatedServer.py"))

        # EDIT PLACEHOLDERS
        self.__replace_placeholders(os.path.join(app_path, "client", "core", "config.py"))

    def __copy_base_template(self, app_path):
        os.mkdir(os.path.join(app_path, "core"))

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
            content = content.replace("{{COMPANY_NAME}}", self.company_name)
            content = content.replace("{{APP_NAME}}", self.game_name)
            content = content.replace("{{DATE_VERSION}}",
                    datetime.now().strftime("%y.%m"))
        with open(filename, "w") as edit_file:
            edit_file.write(content)

    def save(self):
        pass

    def close(self):
        self.project_path = ""
        self.game_name = ""
        self.company_name = ""
        self.template_type = ""
        if self.server_process is not None:
            self.server_process.terminate()
        self.server_process = None
