import sys
import os
from direct.gui.DirectScrolledFrame import DirectScrolledFrame
from direct.gui.DirectLabel import DirectLabel
from direct.gui import DirectGuiGlobals as DGG
from panda3d.core import TextNode
from DirectGuiExtension import DirectGuiHelper as DGH


from threading  import Thread
from queue import Queue, Empty

class Terminal(DirectScrolledFrame):
    def __init__(self, parent = None, process = None, callbackEvent = None, **kw):
        optiondefs = (
            ('terminalWidth',  80, None),
            ('font', 'cmtt12', None),
            ('fontSize', 0.09, None),
            ('fontColor', (0.67, 0.67, 0.67, 1), None),
            ('frameColor', (0, 0, 0, 1), None)
            )
        # Merge keyword options with default options
        self.defineoptions(kw, optiondefs)

        # Initialize superclasses
        DirectScrolledFrame.__init__(self, parent)

        # Call option initialization functions
        self.initialiseoptions(Terminal)

        font = loader.load_font(self['font'])
        self.terminalText = self.createcomponent(
            'terminalText', (), 'terminalText',
            DirectLabel,
            (self.canvas,),
            text='',
            text_wordwrap=self['terminalWidth'],
            text_font=font,
            text_fg=self['fontColor'],
            text_align=TextNode.ALeft,
            frameColor=(0, 0, 0, 0),
            scale=self['fontSize'],
            pos=(0, 0, -self['fontSize']))

        self.update_canvas()

        self.process = process

        self.update_task = None
        if self.process:

            self.linebuffer = []

            self.update_task = taskMgr.add(
                self.update_terminal_process,
                f"terminal_update_process-{id(self.process)}")

            self.update_task.thread = Thread(
                target=self.enqueue_output,
                args=(self.process.stdout, self.linebuffer))
            self.update_task.thread.daemon=True
            self.update_task.thread.start()

        self.callbackEvent = callbackEvent


    def enqueue_output(self, stdout, line_buffer):
        while True:
            line = stdout.readline()
            if line:
                line_buffer.append(line.decode('utf-8'))
            else:
                break

    def close_terminal(self):
        if self.update_task:
            taskMgr.remove(self.update_task)

        if self.callbackEvent:
            base.messenger.send(self.callbackEvent)

    def update_canvas(self):
        self["canvasSize"] = (
            0, DGH.getRealRight(self.terminalText),
            DGH.getRealHeight(self.terminalText), 0
        )

    def update_terminal_process(self, task):
        if self.linebuffer:
            self.terminalText['text'] += self.linebuffer.pop(0)
        return task.cont
