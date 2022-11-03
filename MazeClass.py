from dataclasses import dataclass, field
from random import choice, randint
from time import perf_counter_ns as pf
from numpy import mean

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
    Continue: bool = field(default=True)
    Dir: list[tuple[int]] = field(default_factory=lambda: [(0, -1), (1, 0), (0, 1), (-1, 0)])
    Tiles: list = field(default_factory=list, init=False)
    Hashes: list[int] = field(default_factory=list, init=False)
    
    Times0: list[float] = field(default_factory=list)
    Times1: list[float] = field(default_factory=list)
    Times2: list[float] = field(default_factory=list)

    # Done
    def __post_init__(self):
        Total = list(range(self.X*self.Y))
        for x in range(self.X):
            Colone = list()
            for y in range(self.Y):
                Idx = Total.pop(randint(0, len(Total)-1))
                Colone.append(Tile((x, y), Idx, self))
            self.Tiles.append(Colone)
        [self.Hashes.extend(list(map(lambda x: x.Hash, I))) for I in self.Tiles]
     
    # Done   
    def SameNumber(self):
        First = self.Hashes[0]
        for x in self.Hashes[1:]:
            if not First == x:
                return True
        return False


    def CreateWalls(self):
        while self.SameNumber():
            Current = choice(choice(self.Tiles))
            self.BreakWall(Current)
            
        self.RandomEntry()

    def BreakWall(self, Current):
        Pos = Current.Pos
        Hash = Current.Hash
        
        Neighbors = [self.GetWalls(*Pos, index) for index in range(4)]
        Neighbors = list(filter(lambda x: x != None and x[0].Hash != Hash, Neighbors))
        if not any(Neighbors): return
        
        NewTile, x, y = choice(Neighbors)
        self.NewNumber(Current, NewTile)
        
        DP = 2*x - y
        Idx = abs(DP) + abs(DP)//DP
        Current.Walls[Idx-2] = 0
        NewTile.Walls[Idx] = 0
        

    def GetWalls(self, x, y, Idx):
        Tx, Ty = x+self.Dir[Idx][0], y+self.Dir[Idx][1]
        if not (0 <= Tx < self.X and 0 <= Ty < self.Y):
            return
        return self.Tiles[Tx][Ty], *self.Dir[Idx]
        
    # Done
    def NewNumber(self, First, Second):
        D = pf()
        
        N1, N2 = First.Hash, Second.Hash
        C1, C2 = self.Hashes.count(N1), self.Hashes.count(N2)
        
        Max = First if C1 > C2 else Second
        Min = Second if C1 > C2 else First
        
        for _ in self.Tiles:
            for i in _:
                if i.Hash == Min.Hash:
                    i(*Max)
        Fin = pf() - D
        
        D = pf()
        self.Hashes = list()
        for _ in self.Tiles:
            self.Hashes.extend(map(lambda x: x.Hash, _))
        
        # Min = Min.Hash
        # Max = Max.Hash
        # for idx, i in enumerate(self.Hashes):
        #     if i == Min:
        #         self.Hashes[idx] = Max
        
        Fin = pf() - D
        return Fin
        
    # Done
    def RandomEntry(self):
        for i in range(2):
            Place = randint(0, 1)
            if Place:
                X = choice([0, self.X-1])
                Y = randint(0, self.Y-1)
            else:
                X = randint(0, self.X-1)
                Y = choice([0, self.Y-1])
            
            if X == 0:
                self.DestroyWall(X, Y, 3)
            elif X == len(self.Tiles) - 1:
                self.DestroyWall(X, Y, 1)
            if Y == 0:
                self.DestroyWall(X, Y, 0)
            elif Y == len(self.Tiles[X]) - 1:
                self.DestroyWall(X, Y, 2)
    
    # Done
    def DestroyWall(self, x, y, idx):
        self.Tiles[x][y].Walls[idx] = 0
        
@dataclass
class Tile:
    Pos: tuple[int]
    Hash: int
    ParentObject: Maze = field(repr=False)
    Walls: list[int] = field(default_factory=lambda: [1]*4)
    Color: tuple[int] = field(init=False, repr=False)
    PathColor: map = field(init=False, repr=False)
    
    def __post_init__(self):
        self.Color = NmToRGB((self.Hash*400)/TOTAL+380)
        self.PathColor = map(lambda x: 255-x, self.Color)
    
    def __call__(self, Hash, Color, SubColor):
        self.Hash = Hash
        self.Color = Color
        self.PathColor = SubColor

    def __iter__(self):
        return iter((self.Hash, self.Color, self.PathColor))


NBR = 2
MX, MY = 48*NBR, 27*NBR
TOTAL = MX*MY
T = Maze(MX,MY)

deb = pf()
T.CreateWalls()
print((pf()-deb)/(10**9))
with open('Out.txt', 'w') as X:
    print(T.Tiles, file=X)