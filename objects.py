class Circuit():
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


barcelona = Circuit(8,2,2)
barcelona.cornersInfo()
barcelona.straigthsInfo()

print(barcelona.cornersDistance[0])