#include <iostream>
#include <algorithm>
#include <ctime>
#include <vector>
#include <cstdlib>
#include <tuple>
#include <bits/stdc++.h>
#include <math.h>
#include <fstream>
using namespace std;


int check(const int a[][2], int n) {   
    while(--n>0 && a[n]==a[0]);
    return n!=0;
}

bool Continue(int *Arr, int Max) {
	int First = -1;
	for (int i=0; i<Max; i++) {
		if (First == -1) { First = Arr[i]; }
		else if (First != Arr[i]) { return true; }
	}
	return false;
}

vector<tuple<int, int>> GetWalls(int *Hashes, int Idx, int *Dir, int Max, int X) {
	vector<tuple<int, int>> Neighbors;
	for (int i=0; i<4; i++) {
		int Dx = Idx + Dir[i];
		if (Dx>=0 && Dx<Max && abs(Dx%X-Idx%X)<=1) {
			Neighbors.push_back(make_tuple(Hashes[Dx], Dx));
		}
	}
	return Neighbors;
}

void NewNumber(int *Hashes, int Hash, int NewTile, int n) {
	unordered_map<int, int> mp;
	for (int i = 0; i<n; i++) {
		mp[Hashes[i]]++;
	}
	int C1 = mp[Hash];
	int C2 = mp[NewTile];

	int Min, Max;
	if (C1 > C2) {
		Max = Hash;
		Min = NewTile;
	} else {
		Max = NewTile;
		Min = Hash;
	}

	for (int i=0; i<Max; i++) {
		if (Hashes[i]==Min) { Hashes[i] = Max; }
	}

}

void BreakWall(int Idx, int Hash, int *Walls, int *Hashes, int *Dir, int Max, int X) {
	vector<tuple<int, int>> Neighbors;
	Neighbors = GetWalls(Hashes, Idx, Dir, Max, X);
	for (auto i: Neighbors) {
		cout << "(" << get<0>(i) << ", " << get<1>(i) << "), ";
	}
	cout << "\n";

	if (Neighbors.size()==0){ return; }

	int idx = rand()%Neighbors.size();
	int NewTile, Dx;
	tie(NewTile, Dx) = Neighbors[idx];

	NewNumber(Hashes, Hash, NewTile, Max);

	int F = (Dx<-1) ? 0 : (Dx==1) ? 1 : (Dx>1) ? 2 : 3;
	Walls[Idx] -= pow(2, F);
	Walls[Dx] -= pow(2, 4-F);
}

int* CreateWalls(int *Walls, int *Hashes, int Max, int *Dir, int X) {
	srand(time(0));
	int T = 0;
	ofstream File ("Test.txt");
	while (Continue(Hashes, Max)) {
		int idx = rand() % Max;
		File << idx << " : \t";
		int Hash = Hashes[idx];
		BreakWall(idx, Hash, Walls, Hashes, Dir, Max, X);
		
		for (int i=0; i<Max; i++) {
			File << Hashes[i] << ", ";
		}
		File << "\n";
		T++;
	}
	return Walls;
}

int Create(int x, int y) {
	srand(time(0));
	int Max = x*y;
	int Dir[4] = {-x, 1, x, -1};

	int Hashes[Max];
	for (int i=0; i<Max; i++) {
		Hashes[i] = i;
	}
	
	int Walls[Max];
	fill_n(Walls, Max, 15);
	
	int* NWalls = CreateWalls(Walls, Hashes, Max, Dir, x);

	for (int i=0; i<Max; i++) {
		cout << Hashes[i] << ", " << Walls[i] << ", " << NWalls[i] << "\n";
	}

	return 0;
}

int main() {
	Create(3, 3);
	return 0;
}