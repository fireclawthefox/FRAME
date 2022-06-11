class Editor:
    def __init__(self, parent):
        # Initial setup of the Editor

        # path of the log file, don't change it here. This will be set when
        # the editor is initialized in FRAME!
        self.log_file = ""
        # path of the configuration file, don't change it here. This will be
        # set when the editor is initialized in FRAME!
        self.config_file = ""

    def is_dirty(self):
        """
        This method returns True if an unsaved state of the editor is given
        """
        return False

    def enable_editor(self):
        """
        Enable the editor.
        """
        # Do things like catching events, enabling tasks, etc.
        pass

    def disable_editor(self):
        """
        Disable the editor.
        """
        # Do things like ignoring events, stop tasks, etc.
        pass

    def do_exception_save(self):
        """
        Save content of editor if the application crashes
        """
        # Save all data, preferably in a crash save file to prevent overriding
        # existing saves with corrupted data.
        pass
