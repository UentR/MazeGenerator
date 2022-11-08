import pygame
from MazeClass import Maze
import multiprocessing
from time import perf_counter_ns as pf

class Screen:
    def __init__(self, SizeX: int, SizeY: int, /, *, x:int = None, y:int = None, CellSize:int = None, Fullscreen:bool = None) -> None:
        pygame.init()
        size = (1920, 1080)
        if not CellSize: CellSize = 30
        
        if Fullscreen:
            self.screen = pygame.display.set_mode(size, pygame.FULLSCREEN, pygame.NOFRAME)
        else:
            self.screen = pygame.display.set_mode(size, pygame.NOFRAME)
        
        self.Border=(0,0,0)
        
        self.CellSize=CellSize
        self.BorderSize = CellSize/5
        self.SubBorderSize = self.BorderSize/3
        self.Sub = CellSize>=15
          
    def __call__(self, CurrentState):
        self.screen.fill((0, 0, 0))
        for _ in CurrentState:
            for i in _:
                self.__ShowPixel(i)
        self.__Show()
    
    def __ShowPixel(self, Tile):
        x, y = Tile.Pos
        PathColor = CalcSub(Tile.Color)
        pygame.draw.rect(self.screen, Tile.Color, [x*self.CellSize, y*self.CellSize, self.CellSize, self.CellSize])
        pygame.draw.rect(self.screen, PathColor, [x*self.CellSize+self.BorderSize*2, y*self.CellSize+self.BorderSize*2, self.BorderSize, self.BorderSize])


        pygame.draw.rect(self.screen, self.Border, [x*self.CellSize, y*self.CellSize, self.BorderSize, self.BorderSize])
        pygame.draw.rect(self.screen, self.Border, [x*self.CellSize+self.BorderSize*4, y*self.CellSize, self.BorderSize, self.BorderSize])
        pygame.draw.rect(self.screen, self.Border, [x*self.CellSize, y*self.CellSize+self.BorderSize*4, self.BorderSize, self.BorderSize])
        pygame.draw.rect(self.screen, self.Border, [x*self.CellSize+self.BorderSize*4, y*self.CellSize+self.BorderSize*4, self.BorderSize, self.BorderSize])
        
        if Tile.Walls[0]:
            pygame.draw.rect(self.screen, self.Border, [x*self.CellSize, y*self.CellSize, self.CellSize, self.BorderSize])
        elif self.Sub:
            pygame.draw.rect(self.screen, PathColor, [x*self.CellSize+self.BorderSize*2+self.SubBorderSize, y*self.CellSize+self.SubBorderSize, self.SubBorderSize, self.SubBorderSize])
            pygame.draw.rect(self.screen, PathColor, [x*self.CellSize+self.BorderSize*2+self.SubBorderSize, y*self.CellSize+self.BorderSize+self.SubBorderSize, self.SubBorderSize, self.SubBorderSize])
        if Tile.Walls[1]:
            pygame.draw.rect(self.screen, self.Border, [x*self.CellSize+self.BorderSize*4, y*self.CellSize, self.BorderSize, self.CellSize])
        elif self.Sub:
            pygame.draw.rect(self.screen, PathColor, [x*self.CellSize+self.BorderSize*3+self.SubBorderSize, y*self.CellSize+self.BorderSize*2+self.SubBorderSize, self.SubBorderSize, self.SubBorderSize])
            pygame.draw.rect(self.screen, PathColor, [x*self.CellSize+self.BorderSize*4+self.SubBorderSize, y*self.CellSize+self.BorderSize*2+self.SubBorderSize, self.SubBorderSize, self.SubBorderSize])
        if Tile.Walls[2]:
            pygame.draw.rect(self.screen, self.Border, [x*self.CellSize, y*self.CellSize+self.BorderSize*4, self.CellSize, self.BorderSize])
        elif self.Sub:
            pygame.draw.rect(self.screen, PathColor, [x*self.CellSize+self.BorderSize*2+self.SubBorderSize, y*self.CellSize+self.BorderSize*3+self.SubBorderSize, self.SubBorderSize, self.SubBorderSize])
            pygame.draw.rect(self.screen, PathColor, [x*self.CellSize+self.BorderSize*2+self.SubBorderSize, y*self.CellSize+self.BorderSize*4+self.SubBorderSize, self.SubBorderSize, self.SubBorderSize])
        if Tile.Walls[3]:
            pygame.draw.rect(self.screen, self.Border, [x*self.CellSize, y*self.CellSize, self.BorderSize, self.CellSize])
        elif self.Sub:
            pygame.draw.rect(self.screen, PathColor, [x*self.CellSize+self.SubBorderSize, y*self.CellSize+self.BorderSize*2+self.SubBorderSize, self.SubBorderSize, self.SubBorderSize])
            pygame.draw.rect(self.screen, PathColor, [x*self.CellSize+self.BorderSize+self.SubBorderSize, y*self.CellSize+self.BorderSize*2+self.SubBorderSize, self.SubBorderSize, self.SubBorderSize])
        
    def __Show(self):
        pygame.display.update()


CalcSub = lambda x: tuple(map(lambda t: 255-t, x))

# Display = Screen(5, 5)

List = multiprocessing.Manager().list()
L = Maze(5, 5, List)
L.CreateWalls()
P = multiprocessing.Process(target=L.CreateWalls)
P.start()

with open('Out.txt', 'a') as X:
    while P.is_alive():
        Display(List)
        print(List,file=X)
        pygame.time.delay(1000)
    print(List, file=X)
    Display(List)