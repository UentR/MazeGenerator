from dataclasses import dataclass, field
from random import choice, randint
from time import perf_counter_ns as pf

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

    def __post_init__(self):
        Total = list(range(self.X*self.Y))
        for x in range(self.X):
            Colone = list()
            for y in range(self.Y):
                Idx = Total.pop(randint(0, len(Total)-1))
                Colone.append(Tile((x, y), Idx, self))
            self.Tiles.append(Colone)
        [self.Hashes.extend(list(map(lambda x: x.Hash, I))) for I in self.Tiles]
        
    def SameNumber(self):
        First = self.Hashes[0]
        for x in self.Hashes[1::]:
            if not x == First:
                return
        self.Continue = False

    def CreateWalls(self):
        while self.Continue:
            x, y = choice(choice(self.Tiles)).Pos
            self.Tiles[x][y].BreakWall()
            self.SameNumber()
            T += 1
        print(T)
        self.RandomEntry()

    def GetWalls(self, x, y, Idx):
        Tx, Ty = x+self.Dir[Idx][0], y+self.Dir[Idx][1]
        if not (0 <= Tx < self.X and 0 <= Ty < self.Y):
            return
        return self.Tiles[Tx][Ty]

    def NewNumber(self, First, Second):
        N1, N2 = First.Hash, Second.Hash
        C1, C2 = self.Hashes.count(N1), self.Hashes.count(N2)
        Tamp = list(self.Tiles)
        
        Max = First if C1 > C2 else Second
        Min = Second if C1 > C2 else First
        
        for _ in self.Tiles:
            for i in _:
                if i.Hash == Min.Hash:
                    i.Hash = Max.Hash
                    i.Color = Max.Color
                    i.PathColor = Max.PathColor
        self.Hashes = list()
        [self.Hashes.extend(list(map(lambda x: x.Hash, I))) for I in self.Tiles]
        
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
    
    def BreakWall(self):
        Neighbors = [self.ParentObject.GetWalls(*self.Pos, index) for index in range(4)]
        Neighbors = list(filter(lambda x: x != None and x.Hash != self.Hash, Neighbors))
        if not len(Neighbors): return
        
        NewTile = choice(Neighbors)
        self.ParentObject.NewNumber(self, NewTile)
        
        Dx = NewTile.Pos[0] - self.Pos[0]
        Dy = NewTile.Pos[1] - self.Pos[1]
        DP = 2*Dx - Dy
        Idx = abs(DP) + abs(DP)//DP
        self.Walls[Idx-2] = 0
        NewTile.Walls[Idx] = 0  
        
    def NewHash(self, Nbr):
        self.Hash = Nbr
        self.Color = NmToRGB((self.Hash*400)/TOTAL+380)
        self.PathColor = map(lambda x: 255-x, self.Color)


MX, MY = 96, 54
TOTAL = MX*MY
T = Maze(MX,MY)

deb = pf()
T.CreateWalls()
print((pf()-deb)/(10**9))
