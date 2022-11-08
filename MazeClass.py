from dataclasses import dataclass, field
from random import choice, randint
from time import perf_counter_ns as pf
from time import sleep
import json
from numpy import mean
from multiprocessing import Manager

def NmToRGB(W):
    R2 = -(W - 440) / (440 - 380) if 380 <= W < 440 else 0 if 440 <= W < 510 or not 510 <= W < 781 else 1
    G2 = (W - 440) / (490 - 440) if 440 <= W < 490 else -(W - 645) / (
                645 - 580) if 510 <= W < 645 else 1 if 490 <= W < 510 else 0
    B2 = -(W - 510) / (510 - 490) if 490 <= W < 510 else 1 if 380 <= W < 490 else 0

    F2 = .3
    F2 += .7 * (W - 380) / (420 - 380) if 380 <= W < 420 else .7 if 420 <= W < 701 else .7 * (780 - W) / (
                780 - 700) if 701 <= W < 781 else -.3
    R = max(min(int(round(255 * (R2 * F2) ** .8, 0)), 255), 0)
    G = max(min(int(round(255 * (G2 * F2) ** .8, 0)), 255), 0)
    B = max(min(int(round(255 * (B2 * F2) ** .8, 0)), 255), 0)
    return R, G, B

@dataclass(repr=False)
class Maze:
    X: int
    Y: int
    # Tiles: Manager().list
    Tiles: list = field(default_factory=list)
    Continue: bool = field(default=True)
    Dir: list[tuple[int]] = field(default_factory=lambda: [(0, -1), (1, 0), (0, 1), (-1, 0)], init=False)
    Hashes: list[int] = field(default_factory=list, init=False)

    # Done
    def __post_init__(self):
        Total = list(range(self.X*self.Y))
        for x in range(self.X):
            Colone = list()
            for y in range(self.Y):
                Idx = Total.pop(randint(0, len(Total)-1))
                Colone.append(Tile((x, y), Idx, self.X*self.Y))
            self.Tiles.append(Colone)
        [self.Hashes.extend(list(map(lambda x: x.Hash, I))) for I in self.Tiles]
     
    # Done   
    def __SameNumber(self):
        First = self.Hashes[0]
        for x in self.Hashes[1:]:
            if not First == x:
                return True
        return False

    def CreateWalls(self):
        T = 0
        while self.__SameNumber():
            Current = choice(choice(self.Tiles))
            self.__BreakWall(Current)
            T += 1
        # self.__RandomEntry()
        return T

    def __BreakWall(self, Current):
        Pos = Current.Pos
        Hash = Current.Hash
        Neighbors = [self.__GetWalls(*Pos, index) for index in range(4)]
        Neighbors = list(filter(lambda x: x != None and x[0].Hash != Hash, Neighbors))
        if not any(Neighbors): return
        
        NewTile, x, y = choice(Neighbors)
        self.__NewNumber(Current, NewTile)
        
        DP = 2*x - y
        Idx = abs(DP) + abs(DP)//DP
        Current.Walls[Idx-2] = 0
        NewTile.Walls[Idx] = 0
        
    def __GetWalls(self, x, y, Idx):
        Tx, Ty = x+self.Dir[Idx][0], y+self.Dir[Idx][1]
        if not (0 <= Tx < self.X and 0 <= Ty < self.Y):
            return
        return self.Tiles[Tx][Ty], *self.Dir[Idx]
        
    # Done
    def __NewNumber(self, First, Second):
        N1, N2 = First.Hash, Second.Hash
        C1, C2 = self.Hashes.count(N1), self.Hashes.count(N2)
        
        Max = First if C1 > C2 else Second
        Min = Second if C1 > C2 else First
        for j in self.Tiles:
            for i in j:
                if i.Hash == Min.Hash:
                    i(*Max)
            
        self.Hashes = list()
        for _ in self.Tiles:
            self.Hashes.extend(map(lambda x: x.Hash, _))
            
    # Done
    def __RandomEntry(self):
        for i in range(2):
            Place = randint(0, 1)
            if Place:
                X = choice([0, self.X-1])
                Y = randint(0, self.Y-1)
            else:
                X = randint(0, self.X-1)
                Y = choice([0, self.Y-1])
            
            if X == 0:
                self.__DestroyWall(X, Y, 3)
            elif X == len(self.Tiles) - 1:
                self.__DestroyWall(X, Y, 1)
            if Y == 0:
                self.__DestroyWall(X, Y, 0)
            elif Y == len(self.Tiles[X]) - 1:
                self.__DestroyWall(X, Y, 2)
    
    # Done
    def __DestroyWall(self, x, y, idx):
        self.Tiles[x][y].Walls[idx] = 0
        
@dataclass
class Tile:
    Pos: tuple[int]
    Hash: int
    Total: int = field(repr=False)
    Walls: list[int] = field(default_factory=lambda: [1]*4)
    Color: hex = field(init=False, repr=False)
    
    def __post_init__(self):
        self.Color = NmToRGB((self.Hash*400)/self.Total+380)
    
    def __call__(self, Hash, Color):
        self.Hash = Hash
        self.Color = Color

    def __iter__(self):
        return iter((self.Hash, self.Color))


def Test(x, y, Final):
    T = Maze(x, y)
    d = pf()
    T.CreateWalls()
    Final[str(x*y)].append(pf()-d)
    

if __name__ == "__main__":
    
    # t = Maze(10, 10)
    # D = pf()
    # t.CreateWalls()
    # print(pf()-D)
    
    Nbr = int(input('Nbr max x/y:\n'))
    NBR = int(input('Nbr repeat:\n'))
    Final = {str(x*y): [] for y in range(1, Nbr) for x in range(1, Nbr)}
    R = pf()
    
    for _x in range(1, Nbr):
        for _y in range(1, Nbr):
            for outer in range(NBR):
                T = Maze(_x,_y)
                Fin = T.CreateWalls()
                Final[str(_x*_y)].append(Fin)
        print(_x)
    print((pf()-R)/(10**9))
    for Key, Value in Final.items():
        Final[Key] = mean(Value)
    with open('Out.json', 'w') as X:
        json.dump(Final, X, indent=3)