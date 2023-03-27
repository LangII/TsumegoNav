
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle

import util

class BoardOptions(BoxLayout, util.Helper):
    def __init__(self):
        super(BoardOptions, self).__init__()
        self.orientation = 'horizontal'
        # self.orientation = 'vertical'
        self.size_hint = [1.0, None]
        self.height = 80

        self.padding_outer = util.PAD_V_MAIN_TOP
        self.padding_inner = util.PAD_MAIN_ALL
        self.padding = [self.padding_outer[i] + self.padding_inner[i] for i in range(4)]

        # self.padding = util.PAD_V_MAIN_TOP

        self.spacing = util.SPC_MAIN

        self.setAndAddCanvasBeforeObjs()



        from kivy.uix.button import Button

        self.button_1 = Button()
        self.button_1.size_hint = [None, 1.0]
        # self.button_1.width = self.button_1.height
        # self.button_1.width = 40
        # self.button_1.height = 40
        # self.button_1.padding = util.PAD_H_MAIN_LEFT
        # self.button_1.size = [200, 200]
        self.add_widget(self.button_1)

        # self.button_2 = Button()
        # self.button_2.size_hint = [None, 1.0]
        # self.button_2.width = self.button_2.height
        # self.button_2.padding = util.PAD_H_MAIN_MID
        # self.add_widget(self.button_2)

        # self.button_3 = Button()
        # self.add_widget(self.button_3)
        
        self.updateDisplay()
        self.bind(pos=self.updateDisplay, size=self.updateDisplay)

    def setAndAddCanvasBeforeObjs(self) -> None:
        with self.canvas.before:
            self.rect_color = Color(*util.CLR_DARK_PRISMARINE)
            self.rect = Rectangle()

    def updateDisplay(self, *args) -> None:

        """
        TURNOVER NOTES:
        2023-03-26
        - Need to update rect.pos with pos, also considering padding.  Same for size.
        - Also think about turning this into a util func.  I'll likely need to use this again in
        the future.
        """



        self.rect.pos = [
            self.pos[0] + self.padding_outer[0],
            self.pos[1] + self.padding_outer[3]
        ]
        self.rect.size = [
            self.size[0] - self.padding_outer[1] - self.padding_outer[0],
            self.size[1] - self.padding_outer[2] - self.padding_outer[3]
        ]

        self.button_1.width = self.button_1.height

        # self.rect.pos = self.pos
        # self.rect.size = self.size