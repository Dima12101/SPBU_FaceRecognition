from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label

import matplotlib.pyplot as plt

from src.configs import METHODS_PARAM
from src.core.classifier import research_1_N


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
        self.bth_run_research = Button(text='Расчёт', size_hint=(.1, .05), on_press=self.run_research, background_color = (.5, 1, 1, 1))

        '''2. RESULT BOX'''
        self.box_result = BoxLayout(orientation='horizontal', size_hint=(1, .95), spacing = 5)
        '''2.1 param/mean_score BOX'''
        self.box_param_score = BoxLayout(size_hint=(.6, 1), spacing = 0)
        self.param_score = FigureCanvasKivyAgg(plt.figure(5)) ; plt.title('Подбор параметра', fontsize=self.fs)
        self.box_param_score.add_widget(self.param_score)

        '''2.2 CV param BOX'''
        self.box_CV = BoxLayout(orientation='vertical', size_hint=(.4, 1), spacing = 0)
        
        '''2.2.1 param setting'''
        self.box_param = BoxLayout(orientation='horizontal', size_hint=(.3, .05), spacing = 2)
        self.method_param_name = Label(size_hint=(.05, 1))
        self.method_param = TextInput(size_hint=(.1, 1), multiline=False, input_type='number', input_filter='int')
        self.bth_view = Button(text='Показать', size_hint=(.15, 1), on_press=self.view_CV, background_color = (.5, 1, 1, 1))
        self.box_param.add_widget(self.method_param_name)
        self.box_param.add_widget(self.method_param)
        self.box_param.add_widget(self.bth_view)

        '''2.2.2 CV'''
        self.param_CV = FigureCanvasKivyAgg(plt.figure(6)) ; plt.title('CV для параметра', fontsize=self.fs)

        self.box_CV.add_widget(self.box_param)
        self.box_CV.add_widget(self.param_CV)
        
        self.box_result.add_widget(self.box_param_score)
        self.box_result.add_widget(self.box_CV)

        self.add_widget(self.bth_run_research)
        self.add_widget(self.box_result)

    def _clear(self):
        self.box_param_score.remove_widget(self.param_score)
        self.param_score = FigureCanvasKivyAgg(plt.figure(5))
        self.box_param_score.add_widget(self.param_score)
        plt.figure(5)
        plt.clf() ; plt.cla()
        plt.title(f"Подбор параметра для '{self.method}'", fontsize=self.fs)

        self.box_CV.remove_widget(self.param_CV)
        self.param_CV = FigureCanvasKivyAgg(plt.figure(6))
        self.box_CV.add_widget(self.param_CV)
        plt.figure(6)
        plt.clf() ; plt.cla()
        plt.title(f"CV для параметра '{self.method_param_name.text}'", fontsize=self.fs)

        self.param_CV_scores = None


    def set_database(self, database, data):
        self.database = database
        self.database_data = data
        self._clear()

    def set_method(self, method):
        self.method = method
        self.method_param_name.text = METHODS_PARAM[self.method]['name']
        self.method_param.text = METHODS_PARAM[self.method]['default']
        range_param = METHODS_PARAM[self.method]['range']
        self.values_param = list(range(*range_param))
        self._clear()

    def view_CV(self, instance):
        if self.param_CV_scores is None: return

        choose_param_val = int(self.method_param.text)
        if choose_param_val not in self.values_param: return
        param_val_i = self.values_param.index(choose_param_val)

        self.box_CV.remove_widget(self.param_CV)
        self.param_CV = FigureCanvasKivyAgg(plt.figure(6))
        self.box_CV.add_widget(self.param_CV)
        plt.figure(6)
        plt.clf() ; plt.cla()
        CV_scores = self.param_CV_scores[param_val_i]
        plt.plot(list(range(1, len(CV_scores)+1)), CV_scores)
        plt.ylabel("Точность")
        plt.xlabel("Номер эксперимента")
        plt.title(f"CV для параметра '{self.method_param_name.text}'({self.values_param[param_val_i]})", fontsize=self.fs)

    def run_research(self, instance):
        param_mean_scores, self.param_CV_scores = research_1_N(self.database_data, self.database, self.method)

        self.box_param_score.remove_widget(self.param_score)
        self.param_score = FigureCanvasKivyAgg(plt.figure(5))
        self.box_param_score.add_widget(self.param_score)
        plt.figure(5)
        plt.clf() ; plt.cla()
        plt.plot(self.values_param, param_mean_scores)
        plt.ylabel("Точность")
        plt.xlabel(f"Значение параметра '{self.method_param_name.text}'")
        plt.title(f"Подбор параметра для '{self.method}'", fontsize=self.fs)

        best_score = 0
        best_param_val_i = None
        for i, mean_score in enumerate(param_mean_scores):
            if mean_score > best_score:
                best_score = mean_score ; best_param_val_i = i
        
        self.box_CV.remove_widget(self.param_CV)
        self.param_CV = FigureCanvasKivyAgg(plt.figure(6))
        self.box_CV.add_widget(self.param_CV)
        plt.figure(6)
        plt.clf() ; plt.cla()
        CV_scores = self.param_CV_scores[best_param_val_i]
        plt.plot(list(range(1, len(CV_scores)+1)), CV_scores)
        plt.ylabel("Точность")
        plt.xlabel("Номер эксперимента")
        plt.title(f"CV для параметра '{self.method_param_name.text}'({self.values_param[best_param_val_i]})", fontsize=self.fs)
        self.method_param.text = str(self.values_param[best_param_val_i])
