from DirectGuiExtension.DirectBoxSizer import DirectBoxSizer

from direct.gui import DirectGuiGlobals as DGG

from direct.gui.DirectButton import DirectButton
from direct.gui.DirectFrame import DirectFrame

from panda3d.core import TransparencyAttrib

class EditorFrame:
    editor_instance = None
    editor_frame = None
    selection_button = None

class EditorSelection:
    def __init__(self, top):
        self.top = top
        self.width = 64

        self.editor_frames = []
        self.current_editor_frame = None
        self.editor_holder_frame = None

        self.editor_selection = DirectBoxSizer(
            parent = base.pixel2d,
            frameSize = (
                -self.width/2, self.width/2,
                -base.getSize()[1], self.top),
            frameColor=(0.25, 0.25, 0.25, 1),
            orientation = DGG.VERTICAL,
            itemMargin = (0,0,0,0),
            autoUpdateFrameSize = False)

    def set_editor_holder_frame(self, editor_holder_frame):
        self.editor_holder_frame = editor_holder_frame

    def create_editor_button(self, icon, editor_class, tooltip, tooltip_text, log_file, config_file, editor_class_extra_args=None):
        image_pad = 5
        half_width = self.width / 2

        # create our editor holder class
        ef = EditorFrame()

        # create the frame into which the editor will be embeded
        ef.editor_frame = DirectFrame(
            parent=self.editor_holder_frame,
            frameSize=self.editor_holder_frame["frameSize"],
            frameColor=(0,0,0,0))
        ef.editor_frame.hide()

        # create a deactivated instance
        if editor_class_extra_args:
            ef.editor_instance = editor_class(
                ef.editor_frame,
                *editor_class_extra_args)
        else:
            ef.editor_instance = editor_class(ef.editor_frame)

        editor_save_name = tooltip_text.replace(" ", "_").lower()
        editor_specific_conf = config_file[:-4] + f"_{editor_save_name}.prc"
        ef.editor_instance.log_file = log_file
        ef.editor_instance.config_file = editor_specific_conf
        ef.editor_instance.disable_editor()

        # Create the selection button on the left
        ef.selection_button = DirectButton(
            text="FE",
            frameColor=(0,0,0,0),
            image=icon,
            image_scale=half_width - image_pad,
            pressEffect=False,
            frameSize=(-half_width,half_width,-half_width,half_width),
            command=self.select_editor)
        ef.selection_button.set_transparency(TransparencyAttrib.M_alpha)
        self.editor_selection.addItem(ef.selection_button)
        ef.selection_button.bind(DGG.ENTER, tooltip.show, [tooltip_text])
        ef.selection_button.bind(DGG.EXIT, tooltip.hide)
        ef.selection_button["extraArgs"] = [ef]

        # add the editor frame to the list of editors
        self.editor_frames.append(ef)

        return ef

    def select_editor(self, editor_frame):
        if self.current_editor_frame is not None:
            self.current_editor_frame.editor_frame.hide()
            self.current_editor_frame.editor_instance.disable_editor()
        self.current_editor_frame = editor_frame
        self.current_editor_frame.editor_frame.show()
        self.current_editor_frame.editor_instance.enable_editor()

    def refresh(self):
        self.editor_selection["frameSize"] = (
            -self.width/2, self.width/2,
            -base.getSize()[1], self.top)

        for editor_frame in self.editor_frames:
            editor_frame.editor_frame["frameSize"] = self.editor_holder_frame["frameSize"]
