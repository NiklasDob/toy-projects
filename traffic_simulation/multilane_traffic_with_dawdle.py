import random, time,os

class Game:
    def __init__(self,width = 70,height = 5):
        self.width = width
        self.height = height
        self.generation = 0
        spawnRate = float(raw_input("Verkehr (0,1): "))
        self.map = [[Car(random.randint(0,5),(y,x),width,height, random.random()) if random.random() < spawnRate else "-" for x in range(0,self.width)] for y in range(0,self.height)]
        self.newMap = [[ "-" for x in range(0,self.width)] for y in range(0,self.height)]

    def start(self):
        self.render()
        while True:
            self.update()
            time.sleep(0.5)
            os.system("cls")
            self.generation += 1

    #Kopiert die existierende Map, mit neuen Objekten
    def copyMap(self):
        copied = []
        for x in range(self.height):
            copied.append([])
            for y in range(self.width):
                if type(self.map[x][y]) != str:
                    copied[x].append(Car(self.map[x][y].vel,self.map[x][y].position, self.width,self.height,self.map[x][y].p))
                else:
                    copied[x].append("-")
        return copied

    def copyNewMap(self):
        copied = []
        for x in range(self.height):
            copied.append([])
            for y in range(self.width):
                if type(self.newMap[x][y]) != str:
                    copied[x].append(Car(self.newMap[x][y].vel,self.newMap[x][y].position,self.width,self.height,self.newMap[x][y].p))
                else:
                    copied[x].append("-")
        return copied

    #Update die Map, dazu wird zuerst eine Kopie erstellt, damit die Existierende nicht veraendert wird und damit die
    #Mutation von der Zellen beeintraechtigt wird
    #Dannach wird die Karte neu gerendert
    def update(self):
        oldMap = self.copyMap()
        for y in range(self.height):
            for x in range(self.width):
                if type(self.map[y][x]) != str:
                    self.map[y][x].update(oldMap,self.newMap)

        for y in range(self.height):
            for x in range(self.width):
                if type(self.map[y][x]) != str:
                    self.map[y][x].applyRule4(oldMap,self.newMap)

        self.map = self.copyNewMap()
        avgVel = self.calcAvgVel()
        self.newMap = [[ "-" for x in range(0,self.width)] for y in range(0,self.height)]

        self.render(avgVel)

    def calcAvgVel(self):
        avgVel = []
        for y in range(self.height):
            avgVel.append(0)
            counter = 0
            cars = 0
            for x in range(self.width):
                if type(self.map[y][x]) != str:
                    counter += self.map[y][x].vel
                    cars += 1

            if cars > 0:
                avgVel[y] = float(counter) / float(cars)

        return avgVel
    #Rendert die Karte zur Konsole
    def render(self,avgVel = None):
        if avgVel == None:
            print "Generation",self.generation
            for y in range(self.height):
                for x in range(self.width):
                    print self.map[y][x],
                print
        else:
            print "Generation",self.generation
            for y in range(self.height):
                for x in range(self.width):
                    print self.map[y][x],
                print "Avg:",avgVel[y],"\n"
class Car:

    def __init__(self,vel,position, width, height,p):
        self.vel = vel
        self.oldVel = 0
        self.position = position
        self.width = width
        self.height = height
        self.p = p

    def applyRule1(self):
        self.vel += 1
        if self.vel > 5 :
            self.vel = 5

    def applyRule2(self,oldMap,newMap):
        myY,myX = self.position
        for p in range(1,self.vel+1):
            if type(oldMap[myY%self.height][(myX+p)%self.width]) != str:
                self.oldVel = self.vel
                    # if self.applyRule4(oldMap,newMap):
                    #     print "Spurgewechselt",myY,myX
                    #     return
                self.vel = p - 1
                break
            self.oldVel = self.vel

    def applyRule3(self):
        if random.random() < 0.15  and self.vel > 1:
            self.vel -= 1

    def applyRule4(self,oldMap,newMap):

        if(self.vel == 0 and self.position[0] != 0):
            if(random.random() <= 0.2 and newMap[(self.position[0]-1)%self.height][(self.position[1])%self.width] == "-"):
                # print "zero switching"
                newMap[self.position[0]][self.position[1]] = "-"
                self.position = (self.position[0]-1,self.position[1])
                self.applyRule5(oldMap,newMap)
                return

        if (((self.oldVel+self.vel)/2. > 3. or self.vel > self.oldVel) and self.position[0] != 0 ) and newMap[(self.position[0]-1)%self.height][(self.position[1]+self.oldVel)%self.width] == "-" :
            # print "WechselLinks",self.position[0],self.position[1]
            # print "newpos",(self.position[0]-1)%self.height,(self.position[1]+self.oldVel)%self.width
            newMap[self.position[0]][self.position[1]] = "-"
            self.position = (self.position[0]-1,self.position[1])
            if self.vel < self.oldVel:
                self.vel = self.oldVel
            self.applyRule5(oldMap,newMap)

        elif((((self.oldVel+self.vel)/2. < 1.5) or self.vel < self.oldVel) and self.position[0] != self.height-1 ) and newMap[(self.position[0]+1)%self.height][(self.position[1]+self.oldVel)%self.width] == "-" :
            # print "WechselRechts",self.position[0],self.position[1]
            # print "newpos",(self.position[0]+1)%self.height,(self.position[1]+self.oldVel)%self.width
            newMap[self.position[0]][self.position[1]] = "-"
            self.position = (self.position[0]+1,self.position[1])
            if self.vel < self.oldVel:
                self.vel = self.oldVel
            self.applyRule5(oldMap,newMap)

    def applyRule5(self,oldMap,newMap):
        y,x = self.position
        newY = (y)%self.height
        newX = (x+self.vel)%self.width

        self.position = (newY,newX)

        y,x = self.position
        newMap[y][x] = self

    #Die Zelle mutiert nach den angegebenen Regeln
    def applyRules(self,oldMap,newMap):
        #beschleunigen
        self.applyRule1()
        #bremsen
        # print "Apply Rule2"
        self.applyRule2(oldMap,newMap)
        #troedeln
        self.applyRule3()
        #spur wechseln
        # self.applyRule4(oldMap, newMap)
        #bewegen
        self.applyRule5(oldMap,newMap)
    #Die Zelle updated ihren State nach den Regeln
    def update(self, oldMap,newMap):
        self.applyRules(oldMap,newMap)

    #Damit die Zelle dargestellt werden kann
    def __str__(self):
        return str(self.vel)
        # return "C"

if __name__ == "__main__":
    g = Game()
    g.start()
