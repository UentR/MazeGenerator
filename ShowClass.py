import pygame

class Screen:
    def __init__(self, x=1920, y=1080, /, *, CellSize=40, Fullscreen=False):
        pygame.init()
        if Fullscreen:
            self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN, pygame.NOFRAME)
            self.x, self.y = self.screen.get_size()    
        else:
            self.screen = pygame.display.set_mode((x, y), pygame.NOFRAME)
            self.x, self.y = x, y
        
        self.Border=(0,0,0)
        self.Crossed=(0,0,70)
        self.CellSize=CellSize
        
        self.Nv_Coeff = 3
        self.Delta = CellSize/2/self.Nv_Coeff
        self.Adjust = CellSize/5/self.Nv_Coeff
        
    def Update(self, CurrentState):
        for _ in CurrentState:
            for i in _:
                x, y = i.Pos
        