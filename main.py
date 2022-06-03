import os

from direct.showbase.ShowBase import ShowBase

from panda3d.core import loadPrcFileData

from editorLogHandler import setup_log

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
logfile = setup_log(editor_name)

base = ShowBase()

home = os.path.expanduser("~")
editor_definitions_paths = [
    os.path.join(home, f".{editor_name}", "editors"),
    os.path.join(os.path.dirname(__file__), "editors")
    ]

from Frame.Frame import Frame
Frame(editor_definitions_paths)

base.run()
