from Frame.Extensions.NodeEditor.Nodes.P3DEventNode import Node as P3DEventNode
from Frame.Extensions.NodeEditor.Nodes.P3DCallScriptNode import Node as P3DCallScriptNode
from Frame.Extensions.NodeEditor.Nodes.P3DScriptLoaderNode import Node as P3DScriptLoaderNode
from Frame.Extensions.NodeEditor.Exporters.PythonExporter import PythonExporter

class NodeEditorExtender:
    def get_frame_logic_node_menu(self):
        return [
            {"Logic >":{
                "Catch Event": ["P3DEventNode", P3DEventNode],
                "Load Script": ["P3DScriptLoaderNode", P3DScriptLoaderNode],
                "Call Function": ["P3DCallScriptNode", P3DCallScriptNode]
            }},
            {"Export Python Script": PythonExporter}]
