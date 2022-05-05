import random, time,os

class Game:
    def __init__(self,width = 70,height = 1):
        self.width = width
        self.height = height
        self.generation = 0
        self.map = [[Car(random.randint(0,5),(y,x),width,height) if random.random() < 0.6 else "-" for x in range(0,self.width)] for y in range(0,self.height)]
        self.newMap = [[ "-" for x in range(0,self.width)] for y in range(0,self.height)]

    def start(self):
        self.render()
        while True:
            self.update()
            time.sleep(0.5)
            # os.system("clear")
            self.generation += 1

    #Kopiert die existierende Map, mit neuen Objekten
    def copyMap(self):
        copied = []
        for x in range(self.height):
            copied.append([])
            for y in range(self.width):
                if type(self.map[x][y]) != str:
                    copied[x].append(Car(self.map[x][y].vel,self.map[x][y].position, self.width,self.height))
                else:
                    copied[x].append("-")
        return copied

    def copyNewMap(self):
        copied = []
        for x in range(self.height):
            copied.append([])
            for y in range(self.width):
                if type(self.newMap[x][y]) != str:
                    copied[x].append(Car(self.newMap[x][y].vel,self.newMap[x][y].position,self.width,self.height))
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

        self.map = self.copyNewMap()
        self.newMap = [[ "-" for x in range(0,self.width)] for y in range(0,self.height)]

        self.render()

    #Rendert die Karte zur Konsole
    def render(self):
        # print "Generation",self.generation
        for y in range(self.height):
            for x in range(self.width):
                print self.map[y][x],
            print



    def levelEditor(self):
        self.render()
        inp = raw_input("x,y: ")
        if inp == "end":
            return

        while inp != "end":
            inp = tuple(inp.split(","))
            # if(inp[0] < len(self.map) and inp[1] < len(self.map)):
            self.map[int(inp[1])][int(inp[0])].state = 1 if self.map[int(inp[1])][int(inp[0])].state == 0 else 0
            os.system("clear")
            self.render()
            inp = raw_input("x,y: ")

class Car:

    def __init__(self,vel,position, width, height):
        self.vel = vel
        self.position = position
        self.width = width
        self.height = height

    def applyRule1(self):
        self.vel += 1
        if self.vel > 5:
            self.vel = 5


    def applyRule2(self,oldMap):
        myY,myX = self.position
        for p in range(1,self.vel+1):
            if type(oldMap[myY][(myX+p)%self.width]) != str:
                self.vel = p - 1
                break


    def applyRule3(self,newMap):
        y,x = self.position
        self.position = (y%self.height,(x+self.vel)%self.width)
        y,x = self.position
        newMap[y][x] = self

    #Die Zelle mutiert nach den angegebenen Regeln
    def applyRules(self,oldMap,newMap):
        #beschleunigen
        self.applyRule1()
        #bremsen
        # print "Apply Rule2"
        self.applyRule2(oldMap)
        #bewegen
        self.applyRule3(newMap)
    #Die Zelle updated ihren State nach den Regeln
    def update(self, oldMap,newMap):
        self.applyRules(oldMap,newMap)

    #Damit die Zelle dargestellt werden kann
    def __str__(self):
        return str(self.vel)

if __name__ == "__main__":
    g = Game()
    g.start()
