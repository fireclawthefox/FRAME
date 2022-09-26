# Panda3D imoprts
from direct.fsm.FSM import FSM

class CoreFSM(FSM):
    def enterMain(self):
        # main application logic should be started here

        # connect the client to the server. This method is located in
        # the main.py script
        self.connectClient()

    def exitMain(self):
        # cleanup for application code
        pass
