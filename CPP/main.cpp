#include <iostream>
using namespace std;
#include "MazeClass.h"

int main() {
	int Nbr = 2;
	Maze T;
	T.Startup(2, 4);
	// cout << "OUI";
	T.CreateWalls();
	for (std::vector<Tile> Tamp : T.Tiles) {
		for (Tile X : Tamp) {
			std::cout << X.Hash << "\n";
		}
	}
	return 0;
}