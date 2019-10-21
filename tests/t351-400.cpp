#include<bits/stdc++.h>

const int maxgrid=32;//32;
const int mingrid=32;
const int maxwords=1000;//1000;
const int minwords=1000;
const int maxwordsize=10; // 10
const int minwordsize=10;

int main(int argc, char **argv){
	int type;
	int seed;
	std::cin >> type;
	std::cin >> seed;

	srand(seed);

	std::ofstream grid(argv[1]);
	std::ofstream dict(argv[2]);

	if (type == 0){ // single line in grid
		int n = mingrid+rand() % (maxgrid - mingrid + 1);
		int w = minwords+rand() % (maxwords - minwords + 1);
		for (int i=0; i < n; i++){
			grid << (char)('a' + (rand()%26));
		} grid << "\n";
		for (int i=0; i < w; i++){
			int ws = minwordsize+rand() % (maxwordsize-minwordsize+1);
			for (int j=0; j < ws; j++){
				dict << (char)('a' + (rand()%26));
			}
			dict << "\n";
		}
	}else{
		int n = mingrid+rand() % (maxgrid-mingrid+1);
		int m = mingrid+rand() % (maxgrid-mingrid+1);
		int w = minwords+rand() % (maxwords-minwords+1);
		for (int i=0; i < n; i++){
			for (int j =0 ; j < m; j++){
				grid << (char)('a' + (rand()%26));
			}
			grid << "\n";
		}
		for (int i=0; i < w; i++){
			int ws = minwordsize+rand() % (maxwordsize-minwordsize+1);
			for (int j=0; j < ws; j++){
				dict << (char)('a' + (rand()%26));
			}
			dict << "\n";
		}
		
	}

	grid.close();
	dict.close();
}
