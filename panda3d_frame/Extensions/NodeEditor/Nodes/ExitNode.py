#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = "Fireclaw the Fox"
__license__ = """
Simplified BSD (BSD 2-Clause) License.
See License.txt or http://opensource.org/licenses/BSD-2-Clause for more info
"""

from Panda3DNodeEditor.NodeCore.Nodes.NodeBase import NodeBase
from Panda3DNodeEditor.NodeCore.Sockets.InSocket import InSocket

class Node(NodeBase):
    def __init__(self, parent):
        NodeBase.__init__(self, "Function exitpoint", parent)
        self.addIn("Do Return", InSocket)
        self.addIn("Return Value", InSocket)

    def logic(self):
        pass
