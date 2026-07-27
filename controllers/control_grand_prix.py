from models.circuit import Circuit
from models.formula_car import FormulaCar
from models.grand_prix import GrandPrix

class ControlGrandPrix:
    def __init__(self):
        self.circuitsList = ["monza"]

    def run_race(self):        
        for i in self.circuitsList:
            print(i)
        opt = input("Type the name of the circuit ").strip()

        if opt.lower() == "monza":
            monza = Circuit(5793,11,4)
            monza.cornersInfo()
            monza.straigthsInfo()
            redBull = FormulaCar(20,20,"Hard")
            monzaGP = GrandPrix(redBull,monza,False)
            monzaGP.freePractice() 