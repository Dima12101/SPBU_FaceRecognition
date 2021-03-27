import kivy
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.relativelayout import RelativeLayout 
from kivy.graphics import Color, Rectangle

import os

from src.ui.classifier import MainBox as CL_MainBox
from src.configs import DATA_DIR

class MainBox(BoxLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'

        with self.canvas:
            Color(.2, .3, .5, 1)
            self.bg = Rectangle(source = os.path.join(DATA_DIR, 'bg.jpg'), pos = self.pos, size = self.size)
            self.bind(pos = self.update_bg, size = self.update_bg)

        self.current_mainbox = None
        self.cl_mainbox = CL_MainBox()
        self.sp_mainbox = None

        self.bth_to_menu  = Button(text='Меню', on_press=self.open_menu,
            size_hint = (0.1, 0.05), background_color = (.6, .9, 1, 1))

        ''' ============== Menu of main boxes ============== '''        
        self.list_submainboxes = RelativeLayout()
        bth_classifier_mainbox = Button(text ="Классификатор", on_press=self.open_submain,
            size_hint = (0.2, 0.05), pos_hint={"center_x":.5, "center_y":.55}, background_color = (.6, .9, 1, 1)            )
        bth_search_params_mainbox = Button(text ="Поиск параметров", on_press=self.open_submain,
            size_hint = (0.2, 0.05), pos_hint={"center_x":.5, "center_y":.45}, background_color = (.6, .9, 1, 1))
        self.list_submainboxes.add_widget(bth_classifier_mainbox)
        self.list_submainboxes.add_widget(bth_search_params_mainbox)

        self.add_widget(self.bth_to_menu)
        self.add_widget(self.list_submainboxes)

    def update_bg(self, *args): 
        self.bg.pos = self.pos ; self.bg.size = self.size

    def open_submain(self, instance):
        self.bg.source = ""
        self.remove_widget(self.list_submainboxes)
        
        if instance.text == "Классификатор": self.current_mainbox = self.cl_mainbox
        if instance.text == "Поиск параметров": self.current_mainbox = self.sp_mainbox
        self.add_widget(self.current_mainbox)

    def open_menu(self, instance):
        if self.current_mainbox is not None:
            self.bg.source = os.path.join(DATA_DIR, 'bg.jpg')
            self.remove_widget(self.current_mainbox) ; self.current_mainbox = None
            self.add_widget(self.list_submainboxes)


class MainApp(App):
    title = 'Detection program'

    def build(self):
        Window.maximize()
        return MainBox()
