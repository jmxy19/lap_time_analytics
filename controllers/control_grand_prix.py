from models.formula_car import FormulaCar
from views.main_window import MainWindow
from models.monza import Monza

class ControlGrandPrix:
    def __init__(self, main_window):
        self.main_window = main_window

    def run_race(self):
        opt = self.main_window.get_circuit_choice()
        
        if opt.lower() == "monza":
            monza = Monza()
            redBull = self.main_window.get_formula_car_info()
            self.main_window.freePractice() 