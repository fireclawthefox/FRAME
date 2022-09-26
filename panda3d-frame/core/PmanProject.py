try:
    import pman
    CAN_USE_PMAN = True
except:
    CAN_USE_PMAN = False
import os

class PmanProject:
    def __init__(self):
        self.project_config = None

    def run_project(self):
        if not CAN_USE_PMAN: return
        if not self.project_config:
            return
        print(self.project_config)
        pman.run(self.project_config)

    def stop_project(self):
        return

    def run_server(self):
        base.messenger.send("FRAME_show_warning", ["No a multiplayer project"])
        return

    def stop_server(self):
        return

    def load(self, project_root_path):
        if not CAN_USE_PMAN: return
        self.project_config = pman.get_config(project_root_path)

    def create_new_project(
            self,
            root_path):
        if not CAN_USE_PMAN: return
        if len(os.listdir(root_path)) != 0:
            logging.error("Selected directory for new project is not empty!")
            base.messenger.send(
                "FRAME_show_warning",
                ["Project creation failed!\nSelected directory for new project is not empty!"])
            return
        pman.create_project(root_path)
        self.project_config = pman.get_config(root_path)

    def save(self):
        pass

    def close(self):
        self.project_config = None
