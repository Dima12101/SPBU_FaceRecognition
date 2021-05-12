from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown 
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.graphics import Color

import matplotlib.pyplot as plt

from src.configs import ALL_DATABASES, DATABASE_CONF, ALL_METHODS, METHODS_PARAM
from src import data
from src.core.classifier import research_parallel_system, research_parallel_system_new

import time

class MainBox(BoxLayout):

    def __init__(self, **kwargs):
        super(MainBox, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = 10
        self.fs = 10

        self.method = 'scale'
        self.database = 'ORL'
        self.database_data = None

        with self.canvas:
            Color(0, 0, 0, 0)

        ''' 1. Tools BOX ================================ '''
        self.box_tools = BoxLayout(orientation='horizontal', size_hint=(1, 0.05), spacing = 1)

        ''' 1.1 List databases ================================ '''
        self.dropdown_databases = DropDown()
        for database in ALL_DATABASES: 
            btn = Button(
                text = database, on_press=self.set_database, 
                size_hint_y = None, height = 30, 
                background_color = (.6, .9, 1, .7)) 
            btn.bind(on_release = lambda btn: self.dropdown_databases.select(btn.text)) 
            self.dropdown_databases.add_widget(btn) 
        self.list_databases = Button(text ='Базы', size_hint=(.5, 1), background_color = (.6, .9, 1, 1))
        self.list_databases.bind(on_release = self.dropdown_databases.open)
        self.dropdown_databases.bind(on_select = lambda instance, x: setattr(self.list_databases, 'text', x))
        
        ''' 1.2 RUN ================================ '''
        self.bth_run_research = Button(text='Расчёт', size_hint=(.4, 1), on_press=self.run_research, background_color = (.5, 1, 1, 1))
        
        self.box_L = BoxLayout(orientation='horizontal', size_hint=(.1, 1), spacing = 1)
        L_name = Label(text="L", size_hint=(.4, 1))
        self.L = TextInput(
            text='5', 
            size_hint=(.6, 1), multiline=False, input_type='number', input_filter='int')
        self.box_L.add_widget(L_name)
        self.box_L.add_widget(self.L)

        self.box_tools.add_widget(self.list_databases)
        self.box_tools.add_widget(self.bth_run_research)
        self.box_tools.add_widget(self.box_L)

        ''' 2. Research BOX ================================ '''

        self.research_box = BoxLayout(orientation='vertical', size_hint=(.75, .95), pos_hint={"center_x":.5}, spacing = 10)

        ''' 2.1 Methods ================================ '''
        self.methods = BoxLayout(orientation='horizontal', size_hint=(1, .05), pos_hint={"center_x":.5}, spacing = 1)
        self.methods_params = {}
        for method in ALL_METHODS:
            box_mathod = BoxLayout(orientation='horizontal', size_hint=(.1, 1), spacing = 1)
            method_name = Label(text=f"{method}({METHODS_PARAM[method]['name']}):", size_hint=(.4, 1))
            self.methods_params[method] = TextInput(
                text=METHODS_PARAM[method]['default'], 
                size_hint=(.6, 1), multiline=False, input_type='number', input_filter='int')
            box_mathod.add_widget(method_name)
            box_mathod.add_widget(self.methods_params[method])
            self.methods.add_widget(box_mathod)
        
        ''' 2.2 Result ================================ '''
        self.box_result = BoxLayout(orientation='horizontal', size_hint=(1, 1), spacing = 1)
        self.result = FigureCanvasKivyAgg(plt.figure(8)) ; plt.title('Результат параллельной системы L/N-L', fontsize=self.fs)
        self.box_result.add_widget(self.result)

        self.research_box.add_widget(self.methods)
        self.research_box.add_widget(self.box_result)

        self.add_widget(self.box_tools)
        self.add_widget(self.research_box)

        self._update_database()

    def _update_database(self):
        self.database_data = data.load(self.database)

    def set_database(self, instance):
        self.database = instance.text
        self._update_database()
        self.research_box.set_database(self.database, self.database_data)

    def run_research(self, instance):
        params = {}
        for method in ALL_METHODS:
            params[method] = int(self.methods_params[method].text)

        L = int(self.L.text)

        number_classes = DATABASE_CONF[self.database]['number_group']
        number_img = DATABASE_CONF[self.database]['number_img']

        scores = research_parallel_system_new(self.database_data, self.database, params, L)
        number_img = DATABASE_CONF[self.database]['number_img']
        # x = [im for im in range(1, (number_img-L)*number_classes+1)]
        x = list(range(1, (number_img-L)*number_classes+1))
        self.box_result.remove_widget(self.result)
        self.result = FigureCanvasKivyAgg(plt.figure(8))
        self.box_result.add_widget(self.result)
        plt.figure(8)
        plt.clf() ; plt.cla()
        plt.plot(x, scores)
        plt.ylabel("Точность, %")
        plt.xlabel(f"Кол-во тестовых изображений (L={L})")
        plt.title(f"Результаты параллельной системы", fontsize=self.fs)

        # for scores in research_parallel_system_new(self.database_data, self.database, params):
        #     x = [f'{im*number_classes}' for im in range(1, len(scores)+1)]

        #     self.box_result.remove_widget(self.result)
        #     self.result = FigureCanvasKivyAgg(plt.figure(8))
        #     self.box_result.add_widget(self.result)
        #     plt.figure(8)
        #     plt.clf() ; plt.cla()
        #     plt.plot(x, scores)
        #     plt.ylabel("Точность, %")
        #     plt.xlabel(f"Кол-во тестовых изображений (L={L})")
        #     plt.title(f"Результаты параллельной системы", fontsize=self.fs)

        #     time.sleep(3)
