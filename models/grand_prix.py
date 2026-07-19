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