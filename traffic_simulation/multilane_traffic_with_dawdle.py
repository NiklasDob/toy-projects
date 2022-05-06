from __future__ import print_function, division
import random, time, os
import platform
import copy


class Game:
    def __init__(self, width=80, height=5):
        self.width = width
        self.height = height
        self.generation = 0
        plat = platform.system().lower()
        self.clearCommand = (
            lambda: os.system("cls") if plat == "windows" else os.system("clear")
        )
        spawnRate = float(input("Traffic spawn rate (0,1): "))
        self.map = [
            [
                Car(random.randint(0, 5), (y, x), width, height, random.random())
                if random.random() < spawnRate
                else "-"
                for x in range(0, self.width)
            ]
            for y in range(0, self.height)
        ]
        self.newMap = [
            ["-" for x in range(0, self.width)] for y in range(0, self.height)
        ]

    def start(self):
        self.render()
        while True:
            self.update()
            time.sleep(0.1)
            self.clearCommand()
            self.generation += 1

    def update(self):
        '''
        Update the map, by applying the rules layed out for each car in the map.
        We have an instance of the old map state and a copy, which is going to become the new map state.
        The old map is used for calculating distances / allowed speeds for the cars, which then determine the 
        new position in the new map.
        '''
        oldMap = copy.deepcopy(self.map) 
        for y in range(self.height):
            for x in range(self.width):
                if type(self.map[y][x]) != str:
                    self.map[y][x].update(oldMap, self.newMap)

        self.map = copy.deepcopy(self.newMap)
        avgVel = self.calcAvgVel()
        self.newMap = [
            ["-" for x in range(0, self.width)] for y in range(0, self.height)
        ]

        self.render(avgVel)

    def calcAvgVel(self):
        '''
        Calculate the average velocity per lane
        '''
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

    def render(self, avgVel=None):
        '''
        Draws the cars on the screen
        '''
        
        # Nice for debugging, if you accidentally delete a car
        count = 0
        for y in range(self.height):
            for x in range(self.width):
                count += 1 if isinstance(self.map[y][x], Car) else 0
             
        
        if avgVel == None:
            print("Generation", self.generation, f"Count: {count}")
            for y in range(self.height):
                for x in range(self.width):
                    print(self.map[y][x], end="")
                print()
        else:
            print("Generation", self.generation, f"Count: {count}")
            for y in range(self.height):
                for x in range(self.width):
                    print(self.map[y][x], end="")
                print("Avg:", round(avgVel[y],3))


class Car:
    def __init__(self, vel, position, width, height, p):
        self.vel = vel
        self.oldVel = 0
        self.position = position
        self.width = width
        self.height = height
        self.p = p

        self.maxSpeed = 5
        self.dwadleChance = 0.15

    def applyRule1(self):
        '''
        Increment the velocity
        '''
        self.vel += 1
        if self.vel > self.maxSpeed:
            self.vel = self.maxSpeed

    def applyRule2(self, oldMap, newMap):
        '''
        Determine the speed you can move, without hitting a car
        '''
        myY, myX = self.position
        for p in range(1, self.vel + 1):
            if isinstance(oldMap[myY % self.height][(myX + p) % self.width], Car):
                self.oldVel = self.vel

                self.vel = p - 1
                return
        
        self.oldVel = self.vel

    def applyRule3(self):
        '''
        By random chance slow down by one speed unit
        '''
        if random.random() < self.dwadleChance and self.vel > 1:
            self.vel -= 1

    def applyRule4(self, oldMap, newMap):
        '''
        Move the car to the new position
        '''

        y, x = self.position
        
        newY = (y) % self.height
        newX = (x + self.vel) % self.width

        self.position = (newY, newX)
        newMap[newY][newX] = self

    # Die Zelle mutiert nach den angegebenen Regeln
    def applyRules(self, oldMap, newMap):
        '''
        Apply all rules to the car
        '''
        # accelerate
        self.applyRule1()
        # break
        self.applyRule2(oldMap, newMap)
        # dwadle
        self.applyRule3()
        # move
        self.applyRule4(oldMap, newMap)


    def update(self, oldMap, newMap):
        '''
        Update the cells with the rules 1-5
        '''
        self.applyRules(oldMap, newMap)

    def __repr__(self):
        return str(self.vel)


if __name__ == "__main__":
    g = Game()
    g.start()
