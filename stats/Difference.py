import sys
sys.path.append('/home/quentin/Programmation/PythonGit/MazeGenerator/')

from BetterMazeClass import Maze as M2
from MazeClass import Maze as M1

if __name__ == '__main__':
    Nbr = int(input('Nbr max x/y:\n'))
    NBR = int(input('Nbr repeat:\n'))
    Final = [{'T': {str(x*y): [] for y in range(1, Nbr) for x in range(1, Nbr)},'O': {str(x*y): [] for y in range(1, Nbr) for x in range(1, Nbr)}},
             {'T': {str(x*y): [] for y in range(1, Nbr) for x in range(1, Nbr)},'O': {str(x*y): [] for y in range(1, Nbr) for x in range(1, Nbr)}}]
    Copy = [{'T': {str(x*y): [] for y in range(1, Nbr) for x in range(1, Nbr)},'O': {str(x*y): [] for y in range(1, Nbr) for x in range(1, Nbr)}},
             {'T': {str(x*y): [] for y in range(1, Nbr) for x in range(1, Nbr)},'O': {str(x*y): [] for y in range(1, Nbr) for x in range(1, Nbr)}}]
    Pos = [M1, M2]
    
    from time import perf_counter_ns as pf
    R = pf()
    for repeat in range(NBR):
        C = pf()
        print('---------------')
        print(f"Start of {repeat = }")
        for _x in range(1, Nbr):
            for _y in range(1, Nbr):
                for index in range(2):
                    D = pf()
                    T = Pos[index](_x, _y)
                    O = T.CreateWalls()
                    T = pf() - D
                    Final[index]['T'][str(_x*_y)].append(T)
                    Final[index]['O'][str(_x*_y)].append(O)    
            print(_x)
        print((pf()-C)/(10**9))
        
        from numpy import median
        for index in range(2):
            for Key, Value in Final[index].items():
                for key, value in Value.items():
                    Copy[index][Key][key] = round(median(value), 3)
        
        import json
        for index in range(2):
            for L in ['T', 'O']:
                with open(f'data/Out{index}{L}.json', 'w') as X:
                    json.dump(Copy[index][L], X, indent=3)
    print(pf()-R)