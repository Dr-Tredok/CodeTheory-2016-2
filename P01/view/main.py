from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.config import Config

# GUI: https://kivy.org/#home
Config.set('graphics', 'height', '300')

class MainApp(App):
    """GUI"""
    title = 'Campos Finitos'
    def __init__(self, gen, do):
        super(MainApp, self).__init__()
        self.gen = gen
        self.do = do

    def build(self):
        return Controller(self.gen, self.do)

class Controller(GridLayout):
    operations = ["+", "*", "ia", "im", "**"]
    current_operation = 0
    def __init__(self, gen, do):
        super(Controller, self).__init__()
        self.gen = gen
        self.do = do
        self.elements = []

    def generate_field(self):
        self.elements = self.gen(self.ids.prime_inpt.text, self.ids.exp_inpt.text, self.ids.fx_inpt.text)
        self.ids.elements_field.item_strings = [str(i) for i in self.elements]

    def do_operation(self):
        r = self.do(self.ids.poly1.text, self.ids.poly2.text, Controller.current_operation)
        self.ids.result.text = str(r)

    def select(self):
        Controller.current_operation = (Controller.current_operation + 1)%5
        self.ids.operation.text = Controller.operations[Controller.current_operation]
