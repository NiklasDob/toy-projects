class Cell:
    def __init__(self, state, position):
        self.state = state
        self._position = position

    def getAliveNeighbourCount(self, oldMap):
        """
        Get the alive neighbour count of the cell
        """
        neighbourCount = 0
        for y in range(self._position[0] - 1, self._position[0] + 2):
            for x in range(self._position[1] - 1, self._position[1] + 2):
                if (
                    (x > -1 and y > -1)
                    and (x < len(oldMap) and y < len(oldMap))
                    and not (x == self._position[1] and y == self._position[0])
                ):
                    neighbourCount += oldMap[y][x].state

        return neighbourCount

    def applyRules(self, neighbourCount):
        """
        Apply the standard game of life rules.
        A cell with
            - <= 1 or >= 4 alive neighbour lets the cell die
            - 0 or 3 alive neighbour lets the cell become active

        """
        if neighbourCount <= 1 or neighbourCount >= 4:
            self.state = 0
        elif self.state == 0 and neighbourCount == 3:
            self.state = 1

    def update(self, oldMap):
        """
        Update the cell with the rules supplied in 'applyRules'
        """
        neighbourCount = self.getAliveNeighbourCount(oldMap)
        self.applyRules(neighbourCount)

    def __str__(self):
        """
        Show the cells
        """
        if self.state:
            return "X"
        return "."
