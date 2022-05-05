import random, time,os

class Game:
    def __init__(self,size):
        self.size = size
        self.generation = 0
        self.map = [[Cell(1 if random.random() < 0.5 else 0 ,(y,x)) for x in range(0,self.size)] for y in range(0,self.size)]

        if raw_input("Random?(j/n): ") == "n":
            self.map = [[Cell(1 if random.random() < 0 else 0 ,(y,x)) for x in range(0,self.size)] for y in range(0,self.size)]
            self.levelEditor()

    def start(self):
        self.render()
        while True:
            self.update()
            time.sleep(0.2)
            os.system("cls")
            self.generation += 1

    #Kopiert die existierende Map, mit neuen Objekten
    def copyMap(self):
        copied = []
        for x in range(self.size):
            copied.append([])
            for y in range(self.size):
                copied[x].append(Cell(self.map[x][y].state,self.map[x][y].position))

        return copied

    #Update die Map, dazu wird zuerst eine Kopie erstellt, damit die Existierende nicht veraendert wird und damit die
    #Mutation von der Zellen beeintraechtigt wird
    #Dannach wird die Karte neu gerendert
    def update(self):
        oldMap = self.copyMap()
        for x in range(self.size):
            for y in range(self.size):
                self.map[x][y].update(oldMap)

        self.render()

    #Rendert die Karte zur Konsole
    def render(self):
        print ("Generation",self.generation)
        for x in range(self.size):
            for y in range(self.size):
                print self.map[x][y],
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
            os.system("cls")
            self.render()
            inp = raw_input("x,y: ")


class Cell:

    def __init__(self,state,position):
        self.state = state
        self.position = position

    #Die Zelle checkt die Anzahl von Nachbarn
    def checkNeigbours(self, oldMap):
        count = 0
        for y in range(self.position[0]-1,self.position[0]+2):
            for x in range(self.position[1]-1,self.position[1]+2):
                if (x > -1 and y > -1) and (x < len(oldMap) and y < len(oldMap)) and not (x == self.position[1] and y == self.position[0]):
                    count += oldMap[y][x].state

        return count

    #Die Zelle mutiert nach den angegebenen Regeln
    def applyRules(self,count):
        if count <= 1 or count >= 4:
            self.state = 0
        elif self.state == 0 and count == 3:
            self.state = 1

    #Die Zelle updated ihren State nach den Regeln
    def update(self, oldMap):
        count = self.checkNeigbours(oldMap)
        self.applyRules(count)

    #Damit die Zelle dargestellt werden kann
    def __str__(self):
        if self.state:
            return "X"
        return "."

if __name__ == "__main__":
    g = Game(int(input("N: ")))
    g.start()
