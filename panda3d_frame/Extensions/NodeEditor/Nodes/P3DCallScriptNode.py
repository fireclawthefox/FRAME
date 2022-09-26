#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = "Fireclaw the Fox"
__license__ = """
Simplified BSD (BSD 2-Clause) License.
See License.txt or http://opensource.org/licenses/BSD-2-Clause for more info
"""

from Panda3DNodeEditor.NodeCore.Nodes.NodeBase import NodeBase
from Panda3DNodeEditor.NodeCore.Sockets.InSocket import InSocket
from panda3d_frame.Extensions.NodeEditor.Sockets.TextSocket import TextSocket

class Node(NodeBase):
    def __init__(self, parent):
        NodeBase.__init__(self, "Call script func", parent)
        self.addIn("Path", TextSocket)
        self.addIn("Func", TextSocket)
        self.addIn("Caller", InSocket, True)

    def logic(self):
        # we won't execute the script
        pass
