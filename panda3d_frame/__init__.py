#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = "Fireclaw the Fox"
__license__ = """
Simplified BSD (BSD 2-Clause) License.
See License.txt or http://opensource.org/licenses/BSD-2-Clause for more info
"""

import os

from direct.showbase.ShowBase import ShowBase

from panda3d.core import loadPrcFileData

from . import editorLogHandler

def main():
    editor_name = "FRAME"

    loadPrcFileData(
        "",
        f"""
        sync-video #t
        textures-power-2 none
        window-title Panda3D {editor_name}
        #show-frame-rate-meter #t
        #want-pstats #t
        maximized #t
        win-size 1280 720
        """)
    log_file, config_file = editorLogHandler.setup_log(editor_name, True)

    base = ShowBase()

    home = os.path.expanduser("~")
    editor_definitions_paths = [
        os.path.join(home, f".{editor_name}", "editors"),
        os.path.join(os.path.dirname(__file__), "editors")
        ]

    from .Frame import Frame
    f = Frame(editor_definitions_paths, log_file, config_file)

    f.project_manager.open_project("/home/fireclaw/FRAMETests/My Multiplayer Project/")

    base.run()

if __name__ == "__main__":
    main()
