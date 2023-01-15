#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = "Fireclaw the Fox"
__license__ = """
Simplified BSD (BSD 2-Clause) License.
See License.txt or http://opensource.org/licenses/BSD-2-Clause for more info
"""

from Panda3DNodeEditor.NodeCore.Nodes.NodeBase import NodeBase
from panda3d_frame.Extensions.NodeEditor.Sockets.TextSocket import TextSocket

class Node(NodeBase):
    def __init__(self, parent):
        NodeBase.__init__(self, "Function entrypoint", parent)
        self.addOut("On entry")
        self.addOut("Argument 1")

    def logic(self):
        pass
