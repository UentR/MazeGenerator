from ast import Index
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
    Tiles: list = field(default_factory=list, init=False)
    
    Times0: list[float] = field(default_factory=list)
    Times1: list[float] = field(default_factory=list)
    Times2: list[float] = field(default_factory=list)

    def __post_init__(self):
        Total = self.X*self.Y
        for Idx in range(Total):
            x, y = divmod(Idx, self.Y)
            self.Tiles.append(HashGroup((x,y), Idx, self))
        
    def CreateWalls(self):
        while len(self.Tiles) > 1:	
            Group = choice(self.Tiles)
            H1, H2 = Group.BreakWall()
            
            if (H1, H2) != (-1, -1):
                if H1 < H2:
                    H2(*H1)
                    self.Tiles.remove(H1)
                else:
                    H1(*H2)
                    self.Tiles.remove(H2)
                
        # self.Tiles[0].RandomEntry()

    def GetWalls(self, x, y, Idx):
        Tx, Ty = x+self.Dir[Idx][0], y+self.Dir[Idx][1]
        if not (0 <= Tx < self.X and 0 <= Ty < self.Y):
            return
        return self.Tiles[Tx][Ty]

    def Seek(self, Neighbors):
        Tamp = self.Tiles[:]
        while not (P:=Tamp.pop(randint(0, len(Tamp)-1))).Find(Neighbors): pass
        return P

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
        
        self.Hashes = list()
        for _ in self.Tiles:
            self.Hashes.extend(map(lambda x: x.Hash, _))
        return pf() - D
        
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


@dataclass(repr=False)
class HashGroup:
    Pos: tuple[int]
    Hash: int
    Parent: Maze
    Dir: list[tuple[int]] = field(default_factory=lambda: [(0,-1), (1,0), (0,1), (-1,0)])
    Cells: list = field(init=False, default_factory=list)
    Coords: list[tuple[int]] = field(init=False)
    Done: list = field(default_factory=list)
    
    def __post_init__(self):
        self.Cells.append(Tile(self.Pos, self))
        self.Coords = [self.Pos]
        
    def BreakWall(self):
        Cell = choice(self.Cells)
        x, y = Cell.Pos
        NeighborsPos = list()
        for Dx, Dy in self.Dir:
            Nx, Ny = x+Dx, y+Dy
            if 0 <= Nx < MX and 0 <= Ny < MY:
                NeighborsPos.append((Nx,Ny))
        NeighborsPos = list(filter(lambda x: x not in self.Coords, NeighborsPos))
        
        if not NeighborsPos:
            self.Cells.remove(Cell)
            self.Done.append(Cell)
            return -1, -1
        
        OtherGroup = self.Parent.Seek(NeighborsPos)
        NeighborCell = OtherGroup.Which(NeighborsPos)
        
        Dx = NeighborCell[0] - Cell[0]
        Dy = Cell[1] - NeighborCell[1]
        DP = 2*Dx - Dy
        Idx = abs(DP) + abs(DP)//DP
        Cell.Walls[Idx-2] = 0
        NeighborCell.Walls[Idx] = 0
        return self, OtherGroup
        
    def Which(self, List):
        Tamp = self.Cells[:]
        while (P:=Tamp.pop(randint(0, len(Tamp)-1))).Pos not in List: pass
        return P
        
    def Find(self, List):
        return len(set(self.Coords).union(set(List))) < len(self.Coords)+len(List)

    def __call__(self, Coords, Cells, Done):
        self.Coords.extend(Coords)
        self.Cells.extend(Cells)
        self.Done.extend(Done)
    
    def __iter__(self):
        return iter((self.Coords, self.Cells, self.Done))

    def __lt__(self, other):
        return len(self.Coords) < len(other.Coords)
    
    
@dataclass
class Tile:
    Pos: tuple[int]
    ParentObject: HashGroup = field(repr=False)
    Walls: list[int] = field(default_factory=lambda: [1]*4)
    
    def BreakWall(self):
        Neighbors = [self.ParentObject.GetWalls(*self.Pos, index) for index in range(4)]
        Neighbors = list(filter(lambda x: x != None and x.Hash != self.Hash, Neighbors))
        if not any(Neighbors): return -1
        
        D = pf()
        NewTile = choice(list(Neighbors))
        Fin = self.ParentObject.NewNumber(self, NewTile)	
        

        Dx = NewTile.Pos[0] - self.Pos[0]
        Dy = NewTile.Pos[1] - self.Pos[1]
        DP = 2*Dx - Dy
        Idx = abs(DP) + abs(DP)//DP
        self.Walls[Idx-2] = 0
        NewTile.Walls[Idx] = 0
        return Fin
        
    def NewHash(self, Nbr):
        self.Hash = Nbr
        self.Color = NmToRGB((self.Hash*400)/TOTAL+380)
        self.PathColor = map(lambda x: 255-x, self.Color)

    def __getitem__(self, __name: int):
        return self.Pos[__name]

NBR = 3
MX, MY = 48*NBR, 27*NBR
TOTAL = MX*MY
T = Maze(MX,MY)

deb = pf()
T.CreateWalls()
print((pf()-deb)/(10**9))
print(mean(T.Times0))
print(mean(list(filter(lambda x: x>=0, T.Times1))))
# print(mean(T.Times2))
with open('Out.txt', 'w') as X:
    print(T.Tiles, file=X)