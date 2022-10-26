from dataclasses import dataclass, field
from random import choice, randint


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

@dataclass
class Maze(repr=False):
    X: int = field(repr=True)
    Y: int = field(repr=False)
    Continue: bool = field(default=True, repr=False)
    Dir: list[tuple[int]] = field(default_factory=[(0, -1), (1, 0), (0, 1), (-1, 0)], repr=False)
    Tiles: list = field(default_factory=list, repr=False, init=False)

    def __post_init__(self):
        Total = range(self.X*self.Y)
        for x in range(self.X):
            Colone = list()
            for y in range(self.Y):
                Idx = Total.pop(randint(0, len(Total)))
                Colone.append(Tile((x, y), Idx, self))
            self.Tiles.append(Colone)
        
    def SameNumber(self):
        pass


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
    
    def BreakWall(self, y):
        Neighbors = [self.ParentObject.GetWalls(*self.Pos, index) for index in range(4)]
        if not len(Neighbors): return
        Neighbors = filter(lambda x: x.Hash != self.Hash, Neighbors)
        
        NewTile = choice(Neighbors)
        self.ParentObject.NewNumber(self, NewTile)
        
        Dx = NewTile.Pos[0] - self.Pos[0]
        Dy = NewTile.Pos[1] - self.Pos[1]
        DP = 2*Dx - Dy
        Idx = abs(DP) + abs(DP)//DP
        self.Walls[Idx-2] = 0
        NewTile.wall[Idx] = 0       
        
    def NewHash(self, Nbr):
        self.Hash = Nbr
        self.Color = NmToRGB((self.Hash*400)/TOTAL+380)
        self.PathColor = map(lambda x: 255-x, self.Color)


TOTAL = 190

T = Maze()
print(T)