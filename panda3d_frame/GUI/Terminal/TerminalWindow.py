from panda3d_frame.GUI.Terminal.Terminal import Terminal
from DirectGuiExtension.DirectAutoSizer import DirectAutoSizer
from DirectGuiExtension.DirectTabbedFrame import DirectTabbedFrame
from direct.interval.IntervalGlobal import Sequence, Func
from direct.gui.DirectButton import DirectButton
from panda3d.core import TextNode

class TerminalWindow(DirectTabbedFrame):
    def __init__(self, parent=None, **kw):
        optiondefs = (
            ("frameColor", (0.25, 0.25, 0.25, 1), None),
        )
        self.defineoptions(kw, optiondefs)
        DirectTabbedFrame.__init__(self, parent)

        self.toggle_window_scale = 0.07
        self.btn_toggle_window = self.createcomponent(
            'btnToggleWindow', (), None,
            DirectButton,
            (self,),
            text='+',
            text_align=TextNode.ALeft,
            scale=self.toggle_window_scale,
            borderWidth=(0,0),
            pressEffect=False,
            pos=(
                self["frameSize"][0]+self.toggle_window_scale*0.25,
                0,
                self["frameSize"][3]+self.toggle_window_scale*0.25),
            frameSize=(-0.25,0.75,-0.5,0.5),
            command=self.toggle_window,
        )

        self.initialiseoptions(TerminalWindow)

        self.is_visible = True

        self.slideInPos = (0,0,0)
        self.slideOutPos = (0,0,-1)
        self.slideTime = 0.1

        self.slide_out()

    def add_terminal(self, tabName, process, callbackEvent=None):
        term = Terminal(
            process=process,
            callbackEvent=callbackEvent,
            frameSize=(-1,1,0,0.9))
        holder_frame = DirectAutoSizer(self, term, extendVertical=False)
        self.add_tab(tabName, holder_frame, self.close_terminal)
        tab = self.tab_list[-1]
        tab.closeButton["frameColor"] = (
            (0,0,0,0),
            (0,0,0,0.25),
            (0,0,0,0.35),
            (0,0,0,0))
        tab["pad"] = (0,0)
        tab["borderWidth"] = (0,0)
        tab.resetFrameSize()
        self.reposition_tabs()
        holder_frame.parentObject = self

        self.update_toggle_button_number()

        return term

    def update_toggle_button_number(self):
        if len(self.tab_list) > 0:
            self.btn_toggle_window["text"] = f"+ {len(self.tab_list)}"
            # get number of digits
            x = len(str(abs(len(self.tab_list))))
            x = x*0.5
            self.btn_toggle_window["frameSize"]=(-0.25,0.75+x,-0.5,0.5)
        else:
            self.btn_toggle_window["text"] = "+"
            self.btn_toggle_window["frameSize"]=(-0.25,0.75,-0.5,0.5)

    def toggle_window(self):
        if self.is_visible:
            self.slide_out()
        else:
            self.slide_in()

    def slide_in(self):
        Sequence(
            Func(self.show_tabs),
            self.posInterval(
                self.slideTime,
                self.slideInPos,
                self.slideOutPos)
        ).start()

    def slide_out(self):
        Sequence(
            self.posInterval(
                self.slideTime,
                self.slideOutPos,
                self.slideInPos),
            Func(self.hide_tabs)
        ).start()

    def hide_tabs(self):
        for tab in self.tab_list:
            tab.hide()
        if self.current_content:
            self.current_content.hide()
        self.is_visible = False

    def show_tabs(self):
        for tab in self.tab_list:
            tab.show()
        if self.current_content:
            self.current_content.show()
        self.is_visible = True

    def refresh(self):
        self.prevTabButton.set_x(self["frameSize"][0])
        self.nextTabButton.set_x(self["frameSize"][1])

        self.btn_toggle_window.set_pos(
            self["frameSize"][0]+self.toggle_window_scale*0.25,
            0,
            self["frameSize"][3]+self.toggle_window_scale*0.25)

    def close_terminal(self, tab):
        tab['value'][0].child.close_terminal()

        taskMgr.do_method_later(0.2, self.update_toggle_button_number, "update_term_number", extraArgs=[])

    def close_all(self):
        for tab in self.tab_list:
            self.close_terminal(tab)
            self.close_tab(tab)
