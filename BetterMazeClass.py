from random import randint as rd
from random import shuffle, choice
import numpy as np


def HexToRGB(Nbr):
    Nbr = int(Nbr, 16)
    R = Nbr >> 4
    G = (Nbr >> 2) - (R << 2)
    B = (Nbr) - (G << 2) - (R << 4)
    return R, G, B

class Maze:
    def __init__(self, _x, _y) -> None:
        self.X = _x
        self.Y = _y
        self.Max = _x*_y
        self.Dir = [-_x, 1, _x, -1]
        
        self.Hashes = list(range(1, self.Max+1))
        shuffle(self.Hashes)
        self.Hashes = np.array(self.Hashes)
        
        self.Cols = np.zeros(self.Max)
        
        self.Walls = np.array([15 for y in range(_y) for x in range(_x)])
        
    # Done   
    def __SameNumber(self):
        First = self.Hashes[0]
        for x in self.Hashes:
            if not First == x:
                return True
        return False

    def CreateWalls(self):
        while len(np.unique(self.Hashes)) != 1:
            idx = rd(0, self.Max-1)
            Hash = self.Hashes[idx]
            self.BreakWall(idx, Hash)
        # return t
        # self.__RandomEntry()

    def BreakWall(self, Idx, Hash):
        Neighbors = [self.__GetWalls(Idx, index) for index in range(4)]
        Neighbors = list(filter(lambda x: x != None and x[0] != Hash, Neighbors))
        if not Neighbors: return
        
        NewTile, Dx = choice(Neighbors)
        self.__NewNumber(Hash, NewTile)
        
        if Dx < -1:
            F = 0
        elif Dx == 1:
            F = 1
        elif Dx > 1:
            F = 2
        else:
            F = 3
        
        self.Walls[Idx] -= 2 ** F
        self.Walls[Dx] -= 2 ** (4-F)
        
        
    def __GetWalls(self, idx, Idx):
        Dx = idx + self.Dir[Idx]
        if not 0 <= Dx < self.Max or abs(Dx%self.X - idx%self.X) > 1:
                return
        return self.Hashes[Dx], Dx
        
    # Done
    def __NewNumber(self, First, Second):
        C1, C2 = np.count_nonzero(self.Hashes == First), np.count_nonzero(self.Hashes == Second)    
        
        if C1 > C2:
            Max = First
            Min = Second
        else:
            Max = Second
            Min = First
        
        self.Hashes[self.Hashes == Min] = Max    
    
    
    def ConvertCol(self):
        self.Cols = np.array(map(lambda x: HexToRGB(x*16777215/self.Max), self.Hashes))
    
    # Done
    def __RandomEntry(self):
        for i in range(2):
            Place = rd(0, 1)
            if Place:
                X = choice([0, self.X-1])
                Y = rd(0, self.Y-1)
            else:
                X = rd(0, self.X-1)
                Y = choice([0, self.Y-1])
            
            Idx = Y * self.X + X
            
            if X == 0:
                self.Walls[Idx] = 0
            elif X == len(self.Tiles) - 1:
                self.__DestroyWall(X, Y, 1)
            if Y == 0:
                self.__DestroyWall(X, Y, 0)
            elif Y == len(self.Tiles[X]) - 1:
                self.__DestroyWall(X, Y, 2)
    
    # Done
    def __DestroyWall(self, x, y, idx):
        self.Tiles[x][y].Walls[idx] = 0


if __name__ == "__main__":
    Maze(50, 50).CreateWalls()