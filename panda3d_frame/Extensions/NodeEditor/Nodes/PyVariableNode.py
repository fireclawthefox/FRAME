#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = "Fireclaw the Fox"
__license__ = """
Simplified BSD (BSD 2-Clause) License.
See License.txt or http://opensource.org/licenses/BSD-2-Clause for more info
"""

import logging

from Panda3DNodeEditor.NodeCore.Nodes.NodeBase import NodeBase
from Panda3DNodeEditor.NodeCore.Sockets.TextSocket import TextSocket
from Panda3DNodeEditor.NodeCore.Sockets.OptionSelectSocket import OptionSelectSocket

class Node(NodeBase):
    typeMap = {
        "String": str,
        "Integer": int,
        "Float": float,
        "List": list,
        "Dict": dict,
        "Bool": bool,
        "Object": object
    }
    def __init__(self, parent):
        NodeBase.__init__(self, "Set Variable", parent)
        self.addOut("Get")
        self.addIn("Name", TextSocket)
        self.addIn("Set", TextSocket)
        self.addIn("Type", OptionSelectSocket, extraArgs=[list(Node.typeMap.keys())])

    def logic(self):
        t = Node.typeMap[self.inputList[2].getValue()]
        try:
            self.outputList[0].value = t(self.inputList[1].getValue())
        except:
            logging.error(f"couldn't cast value of '{self.inputList[1].getValue()}' to type {t}")
