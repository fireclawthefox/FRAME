from direct.showbase.ShowBase import ShowBase
from Frame.Frame import Frame

from panda3d.core import loadPrcFileData

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

base = ShowBase()

Frame()

base.run()
