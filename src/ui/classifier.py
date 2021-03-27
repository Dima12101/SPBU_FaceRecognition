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
import os, glob

from src.configs import DATA_DIR, DATABASE_CONF, ALL_METHODS, METHODS_PARAM
from src.core.classifier import recognition
from src.core import features


class MainBox(BoxLayout):

    def __init__(self, **kwargs):
        super(MainBox, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = 10
        self.fs = 10

        self.method = 'scale'
        self.database = 'ORL'

        with self.canvas:
            Color(.2, .3, .5, 1)
            self.bg = Rectangle(source = os.path.join(DATA_DIR, 'bg.jpg'), pos = self.pos, size = self.size)
            self.bind(pos = self.update_bg, size = self.update_bg)

        ''' 1. Tools BOX ================================ '''
        self.box_tools = BoxLayout(orientation='horizontal', size_hint=(1, 0.15), spacing = 10)

        ''' 1.1 Control img BOX ================================ '''
        
        self.index_group = 1
        self.index_img =  1

        self.box_control_img = BoxLayout(orientation='vertical', size_hint=(.4, 1), spacing = 0)
        
        self.box_bth_group = BoxLayout(orientation='horizontal', size_hint=(1,.1))
        self.bth_group_left = Button(text='<- группа', on_press=self.group_left, background_color = (.2, .5, 1, 1))
        self.bth_group_right = Button(text='группа ->', on_press=self.group_right, background_color = (.2, .5, 1, 1))
        self.box_bth_group.add_widget(self.bth_group_left)
        self.box_bth_group.add_widget(self.bth_group_right)

        self.box_bth_img = BoxLayout(orientation='horizontal', size_hint=(1,.1))
        self.bth_img_left = Button(text='<- изображение', on_press=self.img_left, background_color = (.2, .7, 1, 1))
        self.bth_img_right = Button(text='изображение ->', on_press=self.img_right, background_color = (.2, .7, 1, 1))
        self.box_bth_img.add_widget(self.bth_img_left)
        self.box_bth_img.add_widget(self.bth_img_right)

        self.box_control_img.add_widget(self.box_bth_group)
        self.box_control_img.add_widget(self.box_bth_img)

        ''' 1.2 Control DB search BOX ================================ '''
        self.box_control_db_search = BoxLayout(orientation='vertical', size_hint=(.1, .95), spacing = 0)
        self.box_control_db_search_title = Label(text='База поиска', size_hint=(1,0.1))
        
        self.box_group = BoxLayout(orientation='horizontal', size_hint=(1,.45), spacing = 0)
        self.group_border_left = TextInput(text='1', size_hint=(1, 0.5),
            multiline=False, input_type='number', input_filter='int', pos_hint={"center_y":.5})
        self.group_border_right = TextInput(text=str(DATABASE_CONF[self.database]['number_group']), size_hint=(1, 0.5),
            multiline=False, input_type='number', input_filter='int', pos_hint={"center_y":.5})
        self.box_group.add_widget(self.group_border_left)
        self.box_group.add_widget(self.group_border_right)

        self.box_index = BoxLayout(orientation='horizontal', size_hint=(1,.45), spacing = 0)
        self.index_border_left = TextInput(text='1', size_hint=(1, 0.5),
            multiline=False, input_type='number', input_filter='int', pos_hint={"center_y":.5})
        self.index_border_right = TextInput(text=str(DATABASE_CONF[self.database]['number_img']), size_hint=(1, 0.5),
            multiline=False, input_type='number', input_filter='int', pos_hint={"center_y":.5})
        self.box_index.add_widget(self.index_border_left)
        self.box_index.add_widget(self.index_border_right)

        self.box_control_db_search.add_widget(self.box_control_db_search_title)
        self.box_control_db_search.add_widget(self.box_group)
        self.box_control_db_search.add_widget(self.box_index)

        ''' 1.3 Control methods BOX ================================ '''

        self.box_control_methos = BoxLayout(orientation='horizontal', size_hint=(0.4, 1), spacing = 5)

        # Runs
        self.box_runs = BoxLayout(orientation='vertical', size_hint=(0.2, 1), spacing = 0)
        self.bth_run_method = Button(text='Расчёт', on_press=self.run_method,
            background_color = (.5, 1, 1, 1), size_hint = (1, 0.5))
        self.bth_run_recognition = Button(text='Распознать', on_press=self.run_recognition,
            background_color = (.4, 1, .2, 1), size_hint = (1, 0.5))
        self.box_runs.add_widget(self.bth_run_method)
        self.box_runs.add_widget(self.bth_run_recognition)

        # List of methods
        self.dropdown_methods = DropDown()
        for method in ALL_METHODS: 
            btn = Button(
                text = method, on_press=self.set_method, 
                size_hint_y = None, height = 30, 
                background_color = (.6, .9, 1, .7)) 
            btn.bind(on_release = lambda btn: self.dropdown_methods.select(btn.text)) 
            self.dropdown_methods.add_widget(btn) 
        self.list_methods = Button(text ='Методы', size_hint=(.6, 1), background_color = (.6, .9, 1, 1))
        self.list_methods.bind(on_release = self.dropdown_methods.open)
        self.dropdown_methods.bind(on_select = lambda instance, x: setattr(self.list_methods, 'text', x))

        self.method_param_name = Label(text=METHODS_PARAM[self.method]['name'], 
            size_hint=(.05,0.5), pos_hint={"center_y":.5})
        self.method_param = TextInput(text=METHODS_PARAM[self.method]['default'],
            size_hint=(.15, 0.5), pos_hint={"center_y":.5},
            multiline=False, input_type='number', input_filter='int')

        self.box_control_methos.add_widget(self.box_runs)
        self.box_control_methos.add_widget(self.list_methods)
        self.box_control_methos.add_widget(self.method_param_name)
        self.box_control_methos.add_widget(self.method_param)

        self.box_tools.add_widget(self.box_control_img)
        self.box_tools.add_widget(self.box_control_db_search)
        self.box_tools.add_widget(self.box_control_methos)

        ''' 2. Workspace BOX ================================ '''

        self.box_workspace = BoxLayout(orientation='vertical', size_hint=(1, 0.85), spacing = 0)
        
        self.box_input = BoxLayout(orientation='horizontal', size_hint=(1, 0.5), spacing = 0)
        self.input_img = FigureCanvasKivyAgg(plt.figure(1))
        self.input_features = FigureCanvasKivyAgg(plt.figure(2))
        self.box_input.add_widget(self.input_img)
        self.box_input.add_widget(self.input_features)
        
        self.box_output = BoxLayout(orientation='horizontal', size_hint=(1, 0.5), spacing = 0)
        self.output_img = FigureCanvasKivyAgg(plt.figure(3)) ; plt.title('Результат распознавания', fontsize=self.fs)
        self.output_features = FigureCanvasKivyAgg(plt.figure(4)); plt.title('Признаки результата', fontsize=self.fs)
        self.box_output.add_widget(self.output_img)
        self.box_output.add_widget(self.output_features)

        self.box_workspace.add_widget(self.box_input)
        self.box_workspace.add_widget(self.box_output)

        self.add_widget(self.box_tools)
        self.add_widget(self.box_workspace)

        self._update_img()

    def update_bg(self, *args): 
        self.bg.pos = self.pos ; self.bg.size = self.size

    def _update_img(self):
        if self.database == 'ORL':
            self.img_path = DATABASE_CONF['ORL']['img_path'].format(g=self.index_group, im=self.index_img)
            source_img = cv2.imread(self.img_path, -1)
        else:
            name_group = self.index_group if self.index_group >= 10 else f'0{self.index_group}'
            self.img_path = list(glob.glob(DATABASE_CONF['Yale_faces']['img_path'].format(g=name_group)))[self.index_img-1]
            source_img = imageio.imread(self.img_path)
        # placeholder_img = cv2.imread(os.path.join(DATA_DIR, 'default-placeholder.png'), -1)
        self.box_input.remove_widget(self.input_img)
        self.box_input.remove_widget(self.input_features)        

        self.input_img = FigureCanvasKivyAgg(plt.figure(1))
        self.box_input.add_widget(self.input_img)
        plt.figure(1)
        plt.clf() ; plt.cla()
        plt.imshow(source_img, cmap='gray')
        plt.title("Изображение ( {im_i}/{im_n} | {g_i}/{g_n} )".format(
            im_i=self.index_img,
            im_n=DATABASE_CONF[self.database]['number_img'],
            g_i=self.index_group,
            g_n=DATABASE_CONF[self.database]['number_group']
        ), fontsize=self.fs)
        
        self.input_features = FigureCanvasKivyAgg(plt.figure(2))
        self.box_input.add_widget(self.input_features)
        plt.figure(2)
        plt.title('Признаки изображения', fontsize=self.fs)

    def group_left(self, instance):
        if self.index_group != 1:
            self.index_group -= 1 ; self.index_img = 1
            self._update_img()
            
    def group_right(self, instance):
        if self.index_group != DATABASE_CONF[self.database]['number_group']:
            self.index_group += 1 ; self.index_img = 1
            self._update_img()

    def img_left(self, instance):
        if self.index_img != 1:
            self.index_img -= 1 ; self._update_img()

    def img_right(self, instance):
        if self.index_img != DATABASE_CONF[self.database]['number_img']:
            self.index_img += 1 ; self._update_img()

    def set_method(self, instance):
        self.method = instance.text
        self.method_param_name.text = METHODS_PARAM[self.method]['name']
        self.method_param.text = METHODS_PARAM[self.method]['default']

    def run_method(self, instance):        
        ''' ============== INPUT ============== '''
        # Load source image
        if self.database == 'ORL':
            source_img = cv2.imread(self.img_path, -1)
        else:
            source_img = imageio.imread(self.img_path)

        method_param = int(self.method_param.text)
        if method_param < 0: return

        source_img_features, _ = features.HANDLER[self.method](source_img, method_param)

        self.box_input.remove_widget(self.input_features)
        self.input_features = FigureCanvasKivyAgg(plt.figure(2))
        self.box_input.add_widget(self.input_features)
        plt.figure(2)
        plt.clf() ; plt.cla()
        if self.method == 'hist':
            x, h = source_img_features
            plt.bar(x, h)
        elif self.method == 'grad':
            x, y = source_img_features
            plt.plot(x, y)
        else:
            plt.imshow(source_img_features, cmap='gray')
        plt.title('Признаки изображения', fontsize=self.fs)

    def run_recognition(self, instance):        
        ''' ============== INPUT ============== '''
        # Load source image
        if self.database == 'ORL':
            source_img = cv2.imread(self.img_path, -1)
        else:
            source_img = imageio.imread(self.img_path)

        method_param = int(self.method_param.text)
        if method_param < 0: return

        g_left = int(self.group_border_left.text)
        g_right = int(self.group_border_right.text)
        i_left = int(self.index_border_left.text)
        i_right = int(self.index_border_right.text)
        g_range = list(range(1, DATABASE_CONF[self.database]['number_group'] + 1))
        i_range = list(range(1, DATABASE_CONF[self.database]['number_img'] + 1))
        if not (g_left in g_range and g_right in g_range and i_left in i_range and i_right in i_range):
            return

        source_img_features, rec_img, rec_img_features = recognition(
            source_img, self.method, method_param, self.database, (g_left-1, g_right), (i_left-1, i_right))

        self.box_input.remove_widget(self.input_features)
        self.input_features = FigureCanvasKivyAgg(plt.figure(2))
        self.box_input.add_widget(self.input_features)
        plt.figure(2)
        plt.clf() ; plt.cla()
        if self.method == 'hist':
            x, h = source_img_features
            plt.bar(x, h)
        elif self.method == 'grad':
            x, y = source_img_features
            plt.plot(x, y)
        else:
            plt.imshow(source_img_features, cmap='gray')
        plt.title('Признаки изображения', fontsize=self.fs)

        self.box_output.remove_widget(self.output_img)
        self.box_output.remove_widget(self.output_features)

        self.output_img = FigureCanvasKivyAgg(plt.figure(3))
        self.box_output.add_widget(self.output_img)
        plt.figure(3)
        plt.clf() ; plt.cla()
        plt.imshow(rec_img, cmap='gray')
        plt.title('Результат распознавания', fontsize=self.fs)

        self.output_features = FigureCanvasKivyAgg(plt.figure(4))
        self.box_output.add_widget(self.output_features)
        plt.figure(4)
        plt.clf() ; plt.cla()
        if self.method == 'hist':
            x, h = rec_img_features
            plt.bar(x, h)
        elif self.method == 'grad':
            x, y = rec_img_features
            plt.plot(x, y)
        else:
            plt.imshow(rec_img_features, cmap='gray')
        plt.title('Признаки результата', fontsize=self.fs)
