#include "TileClass.h"
#include <vector>
#include <tuple>
#ifndef MAZECLASS_H
#define MAZECLASS_H

class Maze {
	public:
		void Startup(int MX, int MY);
		std::vector<std::vector<Tile>> Tiles;
		std::vector<int> Hashes;
		int MX, MY;
		std::tuple<Tile, int, int> GetWalls(int x, int y, int idx);
		void NewNumber(Tile First, Tile Last);
		void UpdateHashes();
		bool SameNumber();
		void DestroyWall(int x, int y, int idx);
		void RandomEntry();
		void CreateWalls();
		int BreakWall(Tile Current);
		void PrintHash();
		int Dir[4][2] = {{0,-1},{1,0},{0,1},{-1,0}};
};

#endif