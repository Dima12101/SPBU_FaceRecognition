from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label

import matplotlib.pyplot as plt

from src.configs import METHODS_PARAM, DATABASE_CONF
from src.core.classifier import research_L_NL


class ResearchBox(BoxLayout):

    def __init__(self, **kwargs):
        super(ResearchBox, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = 10
        self.fs = 10

        self.method = None
        self.database = None
        self.database_data = None

        '''1. RUN'''
        self.box_run_research = BoxLayout(orientation='horizontal', size_hint=(.3, .05), spacing = 2)
        self.bth_run_research = Button(text='Расчёт', size_hint=(.15, 1), on_press=self.run_research, background_color = (.5, 1, 1, 1))
        self.method_param_name = Label(size_hint=(.05, 1))
        self.method_param = TextInput(size_hint=(.1, 1), multiline=False, input_type='number', input_filter='int')
        self.box_run_research.add_widget(self.bth_run_research)
        self.box_run_research.add_widget(self.method_param_name)
        self.box_run_research.add_widget(self.method_param)

        '''2. RESULT BOX'''
        self.box_result = BoxLayout(orientation='horizontal', size_hint=(1, .95), spacing = 5)
        self.L_score = FigureCanvasKivyAgg(plt.figure(7)) ; plt.title('Результат L/N-L', fontsize=self.fs)
        self.box_result.add_widget(self.L_score)

        self.add_widget(self.box_run_research)
        self.add_widget(self.box_result)

    def _clear(self):
        self.box_result.remove_widget(self.L_score)
        self.L_score = FigureCanvasKivyAgg(plt.figure(7))
        self.box_result.add_widget(self.L_score)
        plt.figure(7)
        plt.clf() ; plt.cla()
        plt.title("Результаты L/N-L", fontsize=self.fs)

    def set_database(self, database, data):
        self.database = database
        self.database_data = data
        self._clear()

    def set_method(self, method):
        self.method = method
        self.method_param_name.text = METHODS_PARAM[self.method]['name']
        self.method_param.text = METHODS_PARAM[self.method]['default']
        self._clear()

    def run_research(self, instance):
        param_val = int(self.method_param.text)
        if param_val not in list(range(*METHODS_PARAM[self.method]['range'])): return

        scores = research_L_NL(self.database_data, self.database, self.method, param_val)

        number_classes = DATABASE_CONF[self.database]['number_group']
        number_img = DATABASE_CONF[self.database]['number_img']

        x = [f'{im}/{number_img-im}\n{im*number_classes}/{(number_img-im)*number_classes}' for im in range(1, number_img)]

        self.box_result.remove_widget(self.L_score)
        self.L_score = FigureCanvasKivyAgg(plt.figure(7))
        self.box_result.add_widget(self.L_score)
        plt.figure(7)
        plt.clf() ; plt.cla()
        plt.plot(x, scores)
        plt.ylabel("Точность")
        plt.xlabel("Значение 'L' (кол-во эталонов / кол-во тестов)")
        plt.title(f"Результаты L/N-L ('{self.method}';{self.method_param_name.text}={param_val})", fontsize=self.fs)
