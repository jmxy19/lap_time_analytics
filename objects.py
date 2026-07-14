class Circuit(): #keeps importaant circuit's info
    def __init__(self, distance, numCorners, numStraights):
        self.distance = distance
        self.numCorners = numCorners
        self.numStraights = numStraights
        self.cornersDistance = []
        self.cornersAngle = []
        self.straightsDistance = []

    def cornersInfo(self): # generate corners's information
        counter = self.numCorners 

        for i in range(counter): #ask for every single corner's distance and angle, depending on the number given
            turnDistance, turnAngle = input(f'Enter distance (Km), and turn angle of the corner numer {i+1} split by (,): ').split(",")

            self.cornersDistance.append(float(turnDistance.strip()))
            self.cornersAngle.append(float(turnAngle.strip()))

    def straigthsInfo(self): #generate straights's information
        counter = self.numStraights 

        for i in range(counter): #ask for every single straights's distance depending on the number given
            straightDistance = input(f'Enter the distance of straight number {i+1} : ')

            self.straightsDistance.append(float(straightDistance.strip()))

class FormulaCar(): #keeps a formula's car info
    def __init__(self, horsePower, maxTorque, tiresType):
        self.horsePower = horsePower
        self.maxTorque = maxTorque
        self.tiresType = tiresType
    
class GrandPrix(): #receives a car and a circuit to start the grand prix 
    def __init__(self, formulaCar, circuit, sprint):
        self.formulaCar = formulaCar
        self.circuit = circuit
        self.sprint = sprint
        
    def freePractice(self): #simulation of free practice

        lapsNumber = int(input("Enter the number of laps that you're gonna test: "))
        lapsRestore = lapsNumber
        tyreWear = 0
        
        if self.sprint == False: # if there isn't sprint race
            sesion = 1
            print(f'\n------------Starting with free practice simulation, sesion {sesion} ------------\n')

            while lapsNumber > 0 and sesion <= 3 : # until there aren't laps and sesions remaining
                print(f'\n------------Laps Remaining {lapsNumber}------------\n')

                if self.formulaCar.tiresType == "Soft":
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

                elif self.formulaCar.tiresType == "Medium":
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

                elif self.formulaCar.tiresType == "Hard":
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

                elif self.formulaCar.tiresType == "Intermediate":
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

                elif self.formulaCar.tiresType == "Full Wet":
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

                if self.formulaCar.tiresType == "Soft":
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

                elif self.formulaCar.tiresType == "Medium":
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

                elif self.formulaCar.tiresType == "Hard":
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

                elif self.formulaCar.tiresType == "Intermediate":
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

                elif self.formulaCar.tiresType == "Full Wet":
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
                



redBullRing = Circuit(5.2, 3, 2)
redBullRing.cornersInfo()
redBullRing.straigthsInfo()

redBull = FormulaCar(850, 720, "Soft")

gp_test1 = GrandPrix(redBull,redBullRing,False)
gp_test1.freePractice()