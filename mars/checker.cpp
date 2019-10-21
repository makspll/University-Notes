#include <bits/stdc++.h>

std::vector<std::string> out1;
std::vector<std::string> out2;

int main(int argc, char **argv){
	std::ifstream o1(argv[1]);
	std::ifstream o2(argv[2]);

	std::string line;

	while (std::getline(o1, line)){
		out1.push_back(line);
	}
	while (std::getline(o2, line)){
		out2.push_back(line);
	}
	if (out2.size() != out1.size()){
		std::cout << "False\n";
		return 0;
	}

	std::sort(out1.begin(), out1.end());
	std::sort(out2.begin(), out2.end());

	for (int i=0 ; i < out1.size(); i++){
		if (out1[i] != out2[i]){
			std::cout << "False\n";
			return 0;
		}
	}
	std::cout << "True\n";
	return 0;
}
