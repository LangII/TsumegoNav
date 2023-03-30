
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle

import util

class BoardOptions(BoxLayout, util.Helper):
    def __init__(self):
        super(BoardOptions, self).__init__()
        self.orientation = 'horizontal'

        self.size_hint = [1.0, None]
        # self.size_hint = [None, None]
        # self.size_hint = [1.0, 1.0]

        self.height = 80
        self.padding_outer = util.PAD_V_MAIN_TOP
        self.padding_inner = util.PAD_MAIN_ALL
        self.padding = [self.padding_outer[i] + self.padding_inner[i] for i in range(4)]
        self.spacing = util.SPC_MAIN
        self.setAndAddCanvasBeforeObjs()

        from kivy.uix.button import Button

        self.cur_next_stone_options = CurNextStoneOptions()
        self.add_widget(self.cur_next_stone_options)



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

    # def getWidth(self) -> float:
    #     return (self.button_1.height * 2) + (util.SPC_MAIN * 5)

    def setAndAddCanvasBeforeObjs(self) -> None:
        with self.canvas.before:
            self.rect_color = Color(*util.CLR_DARK_PRISMARINE)
            self.rect = Rectangle()

    def updateDisplay(self, *args) -> None:


        """
        TURNOVER NOTES:

        2023-03-26
        DONE
        - Need to update rect.pos with pos, also considering padding.  Same for size.
        - Also think about turning this into a util func.  I'll likely need to use this again in
        the future.

        2023-03-27
        - Next to do:
            - The 1st 2 buttons of Board Options will be Widgets with ButtonBehavior like
            BoardButtons.  That way they will look like like stones.
            - The 1st 2 buttons will also be "encased" in their own "boarder".  Just like
            ButtonOptions got its own boarder of DARK_PRISMARINE, these 1st 2 buttons (because
            they're related), get their own boarder encasing.  Use PRISMARINE.
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

        # self.width = self.getWidth()

        # self.rect.pos = self.pos
        # self.rect.size = self.size


class CurNextStoneOptions(BoxLayout, util.Helper):
    def __init__(self):
        super(CurNextStoneOptions, self).__init__()
        self.orientation = 'horizontal'
        self.spacing = util.SPC_MAIN

        # self.padding_outer = util.PAD_V_MAIN_TOP
        # self.padding_inner = util.PAD_MAIN_ALL
        # self.padding = [self.padding_outer[i] + self.padding_inner[i] for i in range(4)]

        self.padding = util.PAD_MAIN_ALL

        self.size_hint = [None, 1.0]
        self.setAndAddCanvasBeforeObjs()

        from kivy.uix.button import Button

        self.button_1 = Button()
        self.button_1.size_hint = [None, 1.0]
        self.add_widget(self.button_1)
        self.button_2 = Button()
        self.button_2.size_hint = [None, 1.0]
        self.add_widget(self.button_2)

        self.width = self.getWidth()

        self.updateDisplay()
        self.bind(pos=self.updateDisplay, size=self.updateDisplay)

    def getWidth(self) -> float:
        return (self.button_1.height * 2) + (util.SPC_MAIN * 3)

    def setAndAddCanvasBeforeObjs(self) -> None:
        with self.canvas.before:
            self.rect_color = Color(*util.CLR_PRISMARINE)
            self.rect = Rectangle()

    def updateDisplay(self, *args) -> None:
        self.rect.pos = self.pos
        self.rect.size = self.size
        self.button_1.width = self.button_1.height
        self.button_2.width = self.button_2.height

        self.width = self.getWidth()






























