import logging
try:
    from panda3d_frame.Extensions.NodeEditor.Nodes.EntryNode import Node as EntryNode
    from panda3d_frame.Extensions.NodeEditor.Nodes.ExitNode import Node as ExitNode
    from panda3d_frame.Extensions.NodeEditor.Nodes.PyVariableNode import Node as PyVariableNode
    from panda3d_frame.Extensions.NodeEditor.Nodes.P3DEventNode import Node as P3DEventNode
    from panda3d_frame.Extensions.NodeEditor.Nodes.P3DCallScriptNode import Node as P3DCallScriptNode
    from panda3d_frame.Extensions.NodeEditor.Nodes.P3DScriptLoaderNode import Node as P3DScriptLoaderNode
    from panda3d_frame.Extensions.NodeEditor.Exporters.PythonExporter import PythonExporter
    NODE_EDITOR_AVAILABLE = True
except:
    logging.error("Import Nodes for NodeEditor extension failed!", exc_info=True)
    NODE_EDITOR_AVAILABLE = False

class NodeEditorExtender:
    def get_frame_logic_node_menu(self):
        print(f"WANT EXTEND!: {NODE_EDITOR_AVAILABLE}")
        if NODE_EDITOR_AVAILABLE:
            return [
                {
                "Function Entry": ["EntryNode", EntryNode],
                "Function Return": ["ExitNode", ExitNode],
                "Logic >":{
                    "Variable": ["PyVariableNode", PyVariableNode],
                    "Catch Event": ["P3DEventNode", P3DEventNode],
                    "Load Script": ["P3DScriptLoaderNode", P3DScriptLoaderNode],
                    "Call Function": ["P3DCallScriptNode", P3DCallScriptNode]
                }},
                {"Export Python Script": PythonExporter}]
        else:
            return []
