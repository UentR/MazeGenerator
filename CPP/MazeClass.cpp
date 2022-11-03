#include "MazeClass.h"
#include "TileClass.h"
#include <cstdlib>
#include <ctime>
#include <iostream>
#include <vector>
#include <functional>
using namespace std;

void Maze::Startup(int x, int y) {
	MX = x;
	MY = y;
	int M = MX*MY;
	vector<int> Total;
	for (int idx=0; idx<M; idx++) { 
		Total.push_back(idx);	
	}
	srand(time(0));
	int L, IDX, idx;
	vector<Tile> Colone;
	for (int x=0; x<MX; x++) {
		Colone.clear();
		for (int y=0; y<MY; y++) {
			L = Total.size();
			IDX = rand() % L;
			idx = Total[IDX];
			Total.erase(Total.begin()+IDX);
			Colone.push_back(Tile(x, y, idx));
		}
		Tiles.push_back(Colone);
	}
}

void Maze::UpdateHashes() {
	Hashes.clear();
	for (std::vector<Tile> i : Tiles) {
		for (Tile Current : i) {
			Hashes.push_back(Current.Hash);
		}
	}
}

bool Maze::SameNumber() {
	int First = Hashes[0];
	for (int x=1; x<Hashes.size(); x++) {
		if (First != Hashes[x]) {
			return true;
		}
	}
	return false;
}

void Maze::RandomEntry() {
	for (int i=0; i<2; i++) {
		bool Place = rand() % 2;
		int DX, DY;
		if (Place) {
			DX = rand() % MX;
			DY = (rand() % 2) * (MY-1);
		} else {
			DX = (rand() % 2) * (MX-1);
			DY = rand() % MY;
		}
		if (DX == 0) {
			DestroyWall(DX, DY, 3);
		} else if (DX == MX-1) {
			DestroyWall(DX, DY, 1);
		}
		if (DY == 0) {
			DestroyWall(DX, DY, 0);
		} else if (DY == MY-1) {
			DestroyWall(DX, DY, 2);
		}
	}
}

void Maze::CreateWalls() {
	while (SameNumber()) {
		int DX = rand() % MX;
		int DY = rand() % MY;
		Tile Current = Tiles[DX][DY];
		Current.BreakWall();
	}
	RandomEntry();
}



// ----------------------------------------
// Unfinished


void Maze::DestroyWall(int x, int y, int idx) {
	Tiles[x][y].Walls[idx] = 0;
}




Tile Maze::GetWalls(int x, int y, int idx) { 
	Tile Current = Tiles[0][0];
	return Current;
}

void Maze::NewNumber(Tile First, Tile Last) {

}