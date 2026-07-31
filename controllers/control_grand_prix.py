from models.circuit import Circuit
from models.formula_car import FormulaCar
from models.grand_prix import GrandPrix
from views.main_window import MainWindow

class ControlGrandPrix:
    def __init__(self, main_window):
        self.main_window = main_window

    def run_race(self):
        opt = self.main_window.get_circuit_choice()
        
        if opt.lower() == "monza":
            monza = Circuit(5793,11,4)
            monza.cornersInfo()
            monza.straigthsInfo()
            redBull = FormulaCar(20,20,"Hard")
            monzaGP = GrandPrix(redBull,monza,False)
            monzaGP.freePractice()   