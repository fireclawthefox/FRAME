
try:
    from panda3d_frame.Extensions.NodeEditor.Nodes.P3DEventNode import Node as P3DEventNode
    from panda3d_frame.Extensions.NodeEditor.Nodes.P3DCallScriptNode import Node as P3DCallScriptNode
    from panda3d_frame.Extensions.NodeEditor.Nodes.P3DScriptLoaderNode import Node as P3DScriptLoaderNode
    from panda3d_frame.Extensions.NodeEditor.Exporters.PythonExporter import PythonExporter
    NODE_EDITOR_AVAILABLE = True
except:
    NODE_EDITOR_AVAILABLE = False

class NodeEditorExtender:
    def get_frame_logic_node_menu(self):
        if NODE_EDITOR_AVAILABLE:
            return [
                {"Logic >":{
                    "Catch Event": ["P3DEventNode", P3DEventNode],
                    "Load Script": ["P3DScriptLoaderNode", P3DScriptLoaderNode],
                    "Call Function": ["P3DCallScriptNode", P3DCallScriptNode]
                }},
                {"Export Python Script": PythonExporter}]
        else:
            return []
