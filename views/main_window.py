from models.circuit import Circuit
from models.formula_car import FormulaCar
from models.grand_prix import GrandPrix

class MainWindow:
    def __init__(self):
        self.circuitsList = ["monza"]

    def get_circuit_choice(self):        
            for i in self.circuitsList:
                print(i)
            opt = input("Type the name of the circuit ").strip()

            return opt
    
            