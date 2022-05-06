from __future__ import print_function, division
import random, time, os
import copy
import platform

from cell import Cell


class Game:

    MAPS_PATH = os.path.join(os.path.dirname(__file__), "maps")

    def __init__(self, size):
        self.size = size
        self.generation = 0
        self.map = [
            [
                Cell(1 if random.random() < 0.5 else 0, (y, x))
                for x in range(0, self.size)
            ]
            for y in range(0, self.size)
        ]

        plat = platform.system().lower()
        self.clearCommand = (
            lambda: os.system("cls") if plat == "windows" else os.system("clear")
        )

    def start(self):
        self.saveMap()

        self.render()
        while True:
            try:
                self.update()
                time.sleep(0.5)
                self.clearCommand()
                self.generation += 1
            except KeyboardInterrupt:
                print("Bye!")
                break
            except Exception as e:
                print(f"Got error while doing simulation: {e}")
                break

    def update(self):
        """
        We update the map, by looking at the previous state
        and applying the rules for each cell.
        """
        oldMap = copy.deepcopy(self.map)
        for x in range(self.size):
            for y in range(self.size):
                self.map[x][y].update(oldMap)

        self.render()

    def render(self):
        """
        Prints the current map to the console
        """
        print("Generation", self.generation)
        for x in range(self.size):
            for y in range(self.size):
                print(self.map[x][y], end="")
            print("\n", end="")

    def levelEditor(self):
        """
        Opens up the level editor, which allows you to place the cells manually at start
        """
        self.render()
        inp = ""
        while True:
            inp = input("x,y: ")
            try:
                inp = tuple(inp.split(","))
                x = int(inp[0])
                y = int(inp[1])

                if x >= self.size or x < 0 or y >= self.size or y < 0:
                    print(f"Invalid! The inputs must be in range (0,{self.size-1})!")
                    continue
                # The map is indexed by the row (or the y coordinate)
                self.map[y][x].state = 1 if self.map[y][x].state == 0 else 0
                self.clearCommand()
                self.render()
            except Exception:
                break

    def saveMap(self):
        if not os.path.exists(self.MAPS_PATH):
            os.makedirs(self.MAPS_PATH)

        with open(os.path.join(self.MAPS_PATH, "random.map"), "w") as f:
            for row in self.map:
                for cell in row:
                    f.write(str(cell.state))
                f.write("\n")

    @staticmethod
    def fromMapFile(filepath: str):
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"File with path {filepath} not found!")

        gameMap = []
        with open(filepath, "r") as f:
            for y, row in enumerate(f.readlines()):
                row = row.replace("\n", "").replace(" ", "").replace("\t", "")
                cells = [Cell(int(state), (y, x)) for x, state in enumerate(row)]
                gameMap.append(cells)

        game = Game(len(gameMap))
        game.map = gameMap

        return game


def startGameWithSize():
    size = int(input("N: "))
    g = Game(size)
    if input("Random?(J/n): ") == "n":
        g.map = [
            [Cell(1 if random.random() < 0 else 0, (y, x)) for x in range(0, g.size)]
            for y in range(0, g.size)
        ]
        g.levelEditor()

    g.start()


def main():
    if os.path.exists(Game.MAPS_PATH):

        files = [
            f
            for f in os.listdir(Game.MAPS_PATH)
            if os.path.isfile(os.path.join(Game.MAPS_PATH, f)) and f.endswith("map")
        ]
        if len(files) == 0:
            startGameWithSize()

        print("You have saved maps! Do you want to load any?")
        print(", ".join(files))
        resp = input(f"Load ({files[0]}) or (n)o: ") or files[0]
        if resp == "n":
            startGameWithSize()

        for f in files:
            if f == resp:
                fp = os.path.join(Game.MAPS_PATH, f)
                game = Game.fromMapFile(fp)
                game.start()
                break

    else:
        startGameWithSize()


if __name__ == "__main__":
    main()
