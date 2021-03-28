from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown 
from kivy.graphics import Color

from src.configs import ALL_DATABASES, ALL_METHODS
from src import data
from src.ui.research.research_1_N import ResearchBox as ResearchBox_1_N
from src.ui.research.research_L_NL import ResearchBox as ResearchBox_L_NL


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
            # Color(.2, .3, .5, 1)
            # self.bg = Rectangle(source = os.path.join(DATA_DIR, 'bg.jpg'), pos = self.pos, size = self.size)
            # self.bind(pos = self.update_bg, size = self.update_bg)

        ''' 1. Tools BOX ================================ '''
        self.box_tools = BoxLayout(orientation='horizontal', size_hint=(1, 0.05), spacing = 10)

        ''' 1.1 List databases ================================ '''
        self.dropdown_databases = DropDown()
        for database in ALL_DATABASES: 
            btn = Button(
                text = database, on_press=self.set_database, 
                size_hint_y = None, height = 30, 
                background_color = (.6, .9, 1, .7)) 
            btn.bind(on_release = lambda btn: self.dropdown_databases.select(btn.text)) 
            self.dropdown_databases.add_widget(btn) 
        self.list_databases = Button(text ='Базы', size_hint=(.1, 1), background_color = (.6, .9, 1, 1))
        self.list_databases.bind(on_release = self.dropdown_databases.open)
        self.dropdown_databases.bind(on_select = lambda instance, x: setattr(self.list_databases, 'text', x))

        ''' 1.2 List methods ================================ '''
        self.dropdown_methods = DropDown()
        for method in ALL_METHODS: 
            btn = Button(
                text = method, on_press=self.set_method, 
                size_hint_y = None, height = 30, 
                background_color = (.6, .9, 1, .7)) 
            btn.bind(on_release = lambda btn: self.dropdown_methods.select(btn.text)) 
            self.dropdown_methods.add_widget(btn) 
        self.list_methods = Button(text ='Методы', size_hint=(.1, 1), background_color = (.6, .9, 1, 1))
        self.list_methods.bind(on_release = self.dropdown_methods.open)
        self.dropdown_methods.bind(on_select = lambda instance, x: setattr(self.list_methods, 'text', x))

        ''' 1.3 List researches ================================ '''
        self.dropdown_researches = DropDown()
        for research in ['1/N-1', 'L/N-L']: 
            btn = Button(
                text = research, on_press=self.set_research, 
                size_hint_y = None, height = 30, 
                background_color = (.6, .9, 1, .7)) 
            btn.bind(on_release = lambda btn: self.dropdown_researches.select(btn.text)) 
            self.dropdown_researches.add_widget(btn) 
        self.list_researches = Button(text ='Исследования', size_hint=(.1, 1), background_color = (.6, .9, 1, 1))
        self.list_researches.bind(on_release = self.dropdown_researches.open)
        self.dropdown_researches.bind(on_select = lambda instance, x: setattr(self.list_researches, 'text', x))

        self.box_tools.add_widget(self.list_databases)
        self.box_tools.add_widget(self.list_methods)
        self.box_tools.add_widget(self.list_researches)

        ''' 2. Research BOX ================================ '''

        self.research_box_1_N = ResearchBox_1_N(size_hint=(.95, .95), pos_hint={"center_x":.5})
        self.research_box_L_NL = ResearchBox_L_NL(size_hint=(.95, .95), pos_hint={"center_x":.5})
        self.research_box = self.research_box_1_N

        self.add_widget(self.box_tools)
        self.add_widget(self.research_box)

        self._update_database()
        self.research_box.set_database(self.database, self.database_data)
        self.research_box.set_method(self.method)


    # def update_bg(self, *args): 
        # self.bg.pos = self.pos ; self.bg.size = self.size

    def _update_database(self):
        self.database_data = data.load(self.database)

    def set_database(self, instance):
        self.database = instance.text
        self._update_database()
        self.research_box.set_database(self.database, self.database_data)

    def set_method(self, instance):
        self.method = instance.text
        self.research_box.set_method(self.method)

    def set_research(self, instance):
        self.remove_widget(self.research_box)
        
        if instance.text == "1/N-1": self.research_box = self.research_box_1_N
        if instance.text == "L/N-L": self.research_box = self.research_box_L_NL
        self.add_widget(self.research_box)

        if self.research_box.method != self.method: self.research_box.set_method(self.method)
        if self.research_box.database != self.database: self.research_box.set_database(self.database, self.database_data)
