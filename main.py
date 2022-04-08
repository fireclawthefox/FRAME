from direct.showbase.ShowBase import ShowBase

from panda3d.core import loadPrcFileData

from editorLogHandler import setup_log

"""
F: Free

R: fRee, Rather, Rich, Robust, Reliable, Responsive

A: Advanced, Adaptable

M: Modular

E: Editor
"""

loadPrcFileData(
    "",
    """
    sync-video #t
    textures-power-2 none
    window-title Panda3D FRAME
    #show-frame-rate-meter #t
    #want-pstats #t
    maximized #t
    win-size 1280 720
    """)

logfile = setup_log("FRAME")

base = ShowBase()

from Frame.Frame import Frame
Frame()

base.run()
