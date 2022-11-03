#ifndef TILECLASS_H
#define TILECLASS_H
#include <string.h>

class Tile {
	public:
		Tile() { }
		Tile(int x, int y, int Idx) {
			int Coords[2] = {x,y};
			memcpy(Pos, Coords, 2*sizeof(int));
			NewHash(Idx);
		}
		int Pos[2];
		int Hash;
		int Walls[4] = { 1, 1, 1, 1 };
		void NewHash(int Nbr) { Hash = Nbr; }
};

#endif