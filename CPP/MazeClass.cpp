#include "MazeClass.h"
#include "TileClass.h"
#include <cstdlib>
#include <algorithm>
#include <ctime>
#include <iostream>
#include <fstream>
#include <vector>
#include <tuple>
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
	UpdateHashes();
}

void Maze::UpdateHashes() {
	PrintHash();
	Hashes.clear();
	for (std::vector<Tile> i : Tiles) {
		for (Tile Current : i) {
			std::cout << Current.Hash << ", ";
			Hashes.push_back(Current.Hash);
		}
	}
	std::cout << "\n\n";
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

void Maze::DestroyWall(int x, int y, int idx) {
	Tiles[x][y].Walls[idx] = 0;
}




void Maze::CreateWalls() {
	int DX, DY;
	Tile Current;
	ofstream File ("Test.txt");
	for (int X : Hashes) {
		File << X << ", ";
	}
	File.close();
	srand(time(0));
	while (SameNumber()) {
		DX = rand() % MX;
		DY = rand() % MY;
		Current = Tiles[DX][DY];
		BreakWall(Current);
		// std::cout << ", " << Tiles[DX][DY].Hash << "\n";
	}
	// RandomEntry();
}

int Maze::BreakWall(Tile Current) {
	int x = Current.Pos[0];
	int y = Current.Pos[1];
	int Hash = Current.Hash;
	// std::cout << Hash << ", ";
	
	std::vector<std::tuple<Tile, int, int>> Neighbors;
	std::tuple<Tile,int,int> Tamp;
	for (int idx=0; idx<4; idx++) {
		Tamp = GetWalls(x, y, idx);
		if (std::get<1>(Tamp)!=-2) {
			if (std::get<0>(Tamp).Hash != Hash) {
				Neighbors.push_back(Tamp);
			}
		}
	}

	if (Neighbors.size()==0) { return 1; }

	int Idx = rand() % Neighbors.size();
	Tile NewTile;
	int Dx, Dy;
	std::tie(NewTile, Dx, Dy) = Neighbors[Idx];
	NewNumber(Current, NewTile);

	int DP = 2*Dx - Dy;
	Idx = abs(DP) + abs(DP)/DP;
	Current.Walls[Idx-2] = 0;
	NewTile.Walls[Idx] = 0;
	Tiles[x][y] = Current;
	Tiles[x+Dx][y+Dy] = NewTile;
	return 1;
	
}



std::tuple<Tile, int, int> Maze::GetWalls(int x, int y, int idx) {
	int Tx = x + Dir[idx][0];
	int Ty = y + Dir[idx][1];
	if ((0>Tx)||(Tx>=MX)||(0>Ty)||(Ty>=MY)) {
		return std::make_tuple(Tile(), -2, -1);
	}
	return std::make_tuple(Tiles[Tx][Ty], Dir[idx][0], Dir[idx][1]);
}



void Maze::NewNumber(Tile First, Tile Last) {
	int C1, C2;
	Tile Max, Min;

	C1 = count(Hashes.begin(), Hashes.end(), First.Hash);
	C2 = count(Hashes.begin(), Hashes.end(), Last.Hash);

	Max = C1 > C2 ? First : Last;
	Min = C1 > C2 ? Last : First;

	// PrintHash();

	for (std::vector<Tile> Col : Tiles) {
		for (Tile I : Col) {
			if (I.Hash == Min.Hash) {
				I.Hash = Min.Hash;
				std::cout << I.Hash << ", ";
			}
		}
	}
	UpdateHashes();
	// PrintHash();
}

void Maze::PrintHash() {
	for (int X : Hashes) {
		std::cout << X << ", ";
	}
	std::cout << "\n";
}