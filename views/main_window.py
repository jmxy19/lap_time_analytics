from models.formula_car import FormulaCar

class MainWindow:
    def __init__(self):
        self.formulaCar = None
        self.circuit = None
        self.sprint = False
        self.circuitsList = ["monza"]

    def get_formula_car_info(self):
        hp = float(input("Enter maximum horsepower (HP): "))
        torque = float(input("Enter maximum torque (Nm): "))
        tyre_compound = input("Enter tyre compound (Soft, Medium, Hard, Intermediate, Full Wet): ").strip().lower()
        self.formulaCar = FormulaCar(hp,torque,tyre_compound)
        return self.formulaCar

    def get_circuit_choice(self):        
            for i in self.circuitsList:
                print(i)
            opt = input("Type the name of the circuit ").strip()

            while True:
                sprint = input("is there a free practice? (yes or no): ").strip().lower()
                if sprint == "yes":
                    self.sprint = True
                    break
                elif sprint == "no":
                    self.sprint = False
                    break
                else:
                    print("Erro in the input data, try again")

            return opt

    def freePractice(self): #simulation of free practice
            while True:
                try:
                    lapsNumber = int(input("Enter the number of laps that you're gonna test: "))
                    lapsRestore = lapsNumber
                    tyreWear = 0
                    break
                except:
                    print("Error in the input data")
    
            if self.sprint == False: # if there isn't sprint race
                sesion = 1
                print(f'\n------------Starting with free practice simulation, sesion {sesion} ------------\n')
    
                while lapsNumber > 0 and sesion <= 3 : # until there aren't laps and sesions remaining
                    print(f'\n------------Laps Remaining {lapsNumber}------------\n')
    
                    if self.formulaCar.tiresType == "soft":
                        tyreWear += 8
                        print(f'the current tyre wear is: {tyreWear}')
    
                        if tyreWear > 100:# if tyre's wear is over 100% the car will be retired and pass to the next practice sesion
                            print(f'retiring the car, since the current tyre wear is: {tyreWear} over the limit')
                            print(f'sesion number {sesion} finished, changing to the next one')
                            sesion +=1
                            lapsNumber = lapsRestore
                            tyreWear = 0
                            print(f'\n------------Starting with free practice simulation, sesion {sesion} ------------\n')
                            continue
                        lapsNumber -= 1
    
                    elif self.formulaCar.tiresType == "medium":
                        tyreWear += 5
                        print(f'the current tyre wear is: {tyreWear}')
    
                        if tyreWear > 100:# if tyre's wear is over 100% the car will be retired and pass to the next practice sesion
                            print(f'retiring the car, since the current tyre wear is: {tyreWear} over the limit')
                            print(f'sesion number {sesion} finished, changing to the next one')
                            sesion +=1
                            lapsNumber = lapsRestore
                            tyreWear = 0
                            print(f'\n------------Starting with free practice simulation, sesion {sesion} ------------\n')
                            continue
                        lapsNumber -= 1
    
                    elif self.formulaCar.tiresType == "hard":
                        tyreWear += 3
                        print(f'the current tyre wear is: {tyreWear}')
    
                        if tyreWear > 100:# if tyre's wear is over 100% the car will be retired and pass to the next practice sesion
                            print(f'retiring the car, since the current tyre wear is: {tyreWear} over the limit')
                            print(f'sesion number {sesion} finished, changing to the next one')
                            sesion +=1
                            lapsNumber = lapsRestore
                            tyreWear = 0
                            print(f'\n------------Starting with free practice simulation, sesion {sesion} ------------\n')
                            continue
                        lapsNumber -= 1
    
                    elif self.formulaCar.tiresType == "intermediate":
                        tyreWear += 3
                        print(f'the current tyre wear is: {tyreWear}')
    
                        if tyreWear > 100:# if tyre's wear is over 100% the car will be retired and pass to the next practice sesion
                            print(f'retiring the car, since the current tyre wear is: {tyreWear} over the limit')
                            print(f'sesion number {sesion} finished, changing to the next one')
                            sesion +=1
                            lapsNumber = lapsRestore
                            tyreWear = 0
                            print(f'\n------------Starting with free practice simulation, sesion {sesion} ------------\n')
                            continue
                        lapsNumber -= 1
    
                    elif self.formulaCar.tiresType == "full wet":
                        tyreWear += 2
                        print(f'the current tyre wear is: {tyreWear}')
    
                        if tyreWear > 100:# if tyre's wear is over 100% the car will be retired and pass to the next practice sesion
                            print(f'retiring the car, since the current tyre wear is: {tyreWear} over the limit')
                            print(f'sesion number {sesion} finished, changing to the next one')
                            sesion +=1
                            lapsNumber = lapsRestore
                            tyreWear = 0
                            print(f'\n------------Starting with free practice simulation, sesion {sesion} ------------\n')
                            continue
                        lapsNumber -= 1
    
                    else:
                        print('type of tire nor found')
    
    
                    if lapsNumber == 0 :#when there aren't laps remaining it changes to the nex sesion
                        print(f'sesion number {sesion} finished, changing to the next one')
                        sesion +=1
                        lapsNumber = lapsRestore
                        tyreWear = 0
                        print(f'\n------------Starting with free practice simulation, sesion {sesion} ------------\n')
    
            else:
                sesion = 1
    
                print(f'\n------------Starting with free practice simulation, sesion {sesion} ------------\n')
    
                while lapsNumber > 0 and sesion <= 2 : # until there aren't laps and sesions remaining
    
                    print(f'\n------------Laps Remaining {lapsNumber}------------\n')
    
                    if self.formulaCar.tiresType == "soft":
                        tyreWear += 8
                        print(f'the current tyre wear is: {tyreWear}')
    
                        if tyreWear > 100:# if tyre's wear is over 100% the car will be retired and pass to the next practice sesion
                            print(f'retiring the car, since the current tyre wear is: {tyreWear} over the limit')
                            print(f'sesion number {sesion} finished, changing to the next one')
                            sesion +=1
                            lapsNumber = lapsRestore
                            tyreWear = 0
                            print(f'\n------------Starting with free practice simulation, sesion {sesion} ------------\n')
                            continue
                        lapsNumber -= 1
    
                    elif self.formulaCar.tiresType == "medium":
                        tyreWear += 5
                        print(f'the current tyre wear is: {tyreWear}')
    
                        if tyreWear > 100:# if tyre's wear is over 100% the car will be retired and pass to the next practice sesion
                            print(f'retiring the car, since the current tyre wear is: {tyreWear} over the limit')
                            print(f'sesion number {sesion} finished, changing to the next one')
                            sesion +=1
                            lapsNumber = lapsRestore
                            tyreWear = 0
                            print(f'\n------------Starting with free practice simulation, sesion {sesion} ------------\n')
                            continue
                        lapsNumber -= 1
    
                    elif self.formulaCar.tiresType == "hard":
                        tyreWear += 3
                        print(f'the current tyre wear is: {tyreWear}')
    
                        if tyreWear > 100:# if tyre's wear is over 100% the car will be retired and pass to the next practice sesion
                            print(f'retiring the car, since the current tyre wear is: {tyreWear} over the limit')
                            print(f'sesion number {sesion} finished, changing to the next one')
                            sesion +=1
                            lapsNumber = lapsRestore
                            tyreWear = 0
                            print(f'\n------------Starting with free practice simulation, sesion {sesion} ------------\n')
                            continue
                        lapsNumber -= 1
    
                    elif self.formulaCar.tiresType == "intermediate":
                        tyreWear += 3
                        print(f'the current tyre wear is: {tyreWear}')
    
                        if tyreWear > 100:# if tyre's wear is over 100% the car will be retired and pass to the next practice sesion
                            print(f'retiring the car, since the current tyre wear is: {tyreWear} over the limit')
                            print(f'sesion number {sesion} finished, changing to the next one')
                            sesion +=1
                            lapsNumber = lapsRestore
                            tyreWear = 0
                            print(f'\n------------Starting with free practice simulation, sesion {sesion} ------------\n')
                            continue
                        lapsNumber -= 1
    
                    elif self.formulaCar.tiresType == "full wet":
                        tyreWear += 2
                        print(f'the current tyre wear is: {tyreWear}')
    
                        if tyreWear > 100:# if tyre's wear is over 100% the car will be retired and pass to the next practice sesion
                            print(f'retiring the car, since the current tyre wear is: {tyreWear} over the limit')
                            print(f'sesion number {sesion} finished, changing to the next one')
                            sesion +=1
                            lapsNumber = lapsRestore
                            tyreWear = 0
                            print(f'\n------------Starting with free practice simulation, sesion {sesion} ------------\n')
                            continue
                        lapsNumber -= 1
    
                    else:
                        print('type of tire nor found')
    
    
                    if lapsNumber == 0 :#when there aren't laps remaining it changes to the nex sesion
                        print(f'sesion number {sesion} finished, changing to the next one')
                        sesion +=1
                        lapsNumber = lapsRestore
                        tyreWear = 0
                        
                        print(f'\n------------Starting with free practice simulation, sesion {sesion} ------------\n')
    
         