from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown 
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle

import matplotlib.pyplot as plt
import cv2
import imageio
import os

from src.ui.configs import DATA_DIR, ALL_METHODS, METHODS_PARAM
from src.ui.base import MatrixWidget, ImgBox

from src.core import features


class MainBox(BoxLayout):

    def __init__(self, **kwargs):
        super(MainBox, self).__init__(**kwargs)
        self.orientation = 'horizontal'
        self.spacing = 20

        self.method = 'scale'
        default_database = 'ORL'

        with self.canvas:
            Color(.2, .3, .5, 1)
            self.bg = Rectangle(source = os.path.join(DATA_DIR, 'bg.jpg'), pos = self.pos, size = self.size)
            self.bind(pos = self.update_bg, size = self.update_bg)

        ''' ================ Source Img BOX ================ '''
        self.source = ImgBox(database=default_database, name="'Source' изображение", size_hint=(.5, 1))

        ''' ================ Feature BOX ================ '''
        self.feature_box = BoxLayout(orientation='vertical', size_hint=(.5, 0.92), spacing = 10)

        self.box_methods = BoxLayout(orientation='horizontal', size_hint=(1, .1), spacing = 5)
        # Run mathod
        self.bth_run_method = Button(text='RUN', on_press=self.run_method,
            background_normal = os.path.join(DATA_DIR, 'normal.png'), 
            background_down = os.path.join(DATA_DIR, 'down.png'),
            border = (30, 30, 30, 30),                    
            size_hint = (.2, 1))

        # List of methods
        dropdown_methods = DropDown()
        for method in ALL_METHODS: 
            btn = Button(
                text = method, on_press=self.set_method, 
                size_hint_y = None, height = 30, 
                background_color = (.6, .9, 1, .5)) 
            btn.bind(on_release = lambda btn: dropdown_methods.select(btn.text)) 
            dropdown_methods.add_widget(btn) 
        list_methods = Button(text ='Методы', size_hint=(.6, 1), background_color = (.6, .9, 1, 1))
        list_methods.bind(on_release = dropdown_methods.open)
        dropdown_methods.bind(on_select = lambda instance, x: setattr(list_methods, 'text', x))

        self.method_param_name = Label(text=METHODS_PARAM[self.method]['name'], 
            size_hint=(.05,0.5), pos_hint={"center_y":.5})
        self.method_param = TextInput(text=METHODS_PARAM[self.method]['default'],
            size_hint=(.15, 0.5), pos_hint={"center_y":.5},
            multiline=False, input_type='number', input_filter='int')

        self.box_methods.add_widget(self.bth_run_method)
        self.box_methods.add_widget(list_methods)
        self.box_methods.add_widget(self.method_param_name)
        self.box_methods.add_widget(self.method_param)

        # self.feature_res = ImgWidget()
        #  = MatrixWidget()
        
        self.feature_res = FigureCanvasKivyAgg(plt.gcf())

        self.feature_box.add_widget(self.box_methods)
        self.feature_box.add_widget(self.feature_res)

        self.add_widget(self.source)
        self.add_widget(self.feature_box)

    def update_bg(self, *args): 
        self.bg.pos = self.pos ; self.bg.size = self.size

    def set_method(self, instance):
        self.method = instance.text
        self.method_param_name.text = METHODS_PARAM[self.method]['name']
        self.method_param.text = METHODS_PARAM[self.method]['default']

    def run_method(self, instance):        
        ''' ============== INPUT ============== '''
        # Load source image
        if self.source.database == 'ORL':
            source_img = cv2.imread(self.source.img_path, -1)
        else:
            source_img = imageio.imread(self.source.img_path)

        method_param = int(self.method_param.text)
        if method_param < 0: return

        feature, _ = features.HANDLER[self.method](source_img, method_param)

        plt.clf()
        self.feature_box.remove_widget(self.feature_res)
        self.feature_res = FigureCanvasKivyAgg(plt.gcf())
        self.feature_box.add_widget(self.feature_res)
        if self.method == 'hist':
            x, h = feature
            plt.bar(x, h)
        elif self.method == 'grad':
            x, y = feature
            plt.plot(x, y)
        else:
            plt.imshow(feature, cmap='gray')
