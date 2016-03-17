from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.config import Config

# GUI: https://kivy.org/#home
Config.set('graphics', 'height', '330')

class MainApp(App):
    """GUI"""
    title = 'Campos Finitos'
    def __init__(self, gen, do, alpha):
        super(MainApp, self).__init__()
        self.gen = gen
        self.do = do
        self.alpha = alpha
    def build(self):
        return Controller(self.gen, self.do, self.alpha)

class Controller(GridLayout):
    operations = ["+", "*", "ia", "im", "**"]
    current_operation = 0
    def __init__(self, gen, do, alpha):
        super(Controller, self).__init__()
        self.gen = gen
        self.do = do
        self.alpha = alpha
        self.elements = []

    def generate_field(self):
        self.elements = self.gen(self.ids.prime_inpt.text, self.ids.exp_inpt.text, self.ids.fx_inpt.text)
        self.ids.elements_field.item_strings = [str(self.elements[0])]
        for j in range(len(self.elements) - 1):
            self.ids.elements_field.item_strings.append("α^" + str(j) + ": " + str(self.elements[j + 1])) 

    def do_operation(self):
        r = self.do(self.ids.poly1.text, self.ids.poly2.text, Controller.current_operation)
        self.ids.result.text = str(r)

    def ifrom_alpha(self):
        ia, im = self.alpha(self.ids.alpha.text)
        self.ids.iadd.text = str(ia)
        self.ids.imult.text = str(im)

    def select(self):
        Controller.current_operation = (Controller.current_operation + 1)%5
        self.ids.operation.text = Controller.operations[Controller.current_operation]
