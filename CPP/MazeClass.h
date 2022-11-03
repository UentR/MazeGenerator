#include "TileClass.h"
#include <vector>
#ifndef MAZECLASS_H
#define MAZECLASS_H

class Maze {
	public:
		void Startup(int MX, int MY);
		std::vector<std::vector<Tile>> Tiles;
		std::vector<int> Hashes;
		int MX, MY;
		Tile GetWalls(int x, int y, int idx);
		void NewNumber(Tile First, Tile Last);
		void UpdateHashes();
		bool SameNumber();
		void DestroyWall(int x, int y, int idx);
		void RandomEntry();
		void CreateWalls();

	private:
		bool Continue = true;
		int Dir[4][2] = {{0,-1},{1,0},{0,1},{-1,0}};
		int Total;
};

#endif