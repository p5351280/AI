#include <iostream>
#include <vector>
#include <map>
#include <cstdlib>
#include <ctime>
#include <algorithm>

using namespace std;

const int MAX_INT(2147483647);
map<vector<int>, int> attack;

int checkForAttack(vector<int>){

}

vector<int> mapGenerate(int n){
	vector<int> map;
	for(int i=1; i<=n; i++){
		int temp = rand()%n + 1;
		while(find(map.begin(), map.end(), temp) != map.end())
			temp = rand()%n + 1;
		map.push_back(temp);
	}
	return map;
}

vector<int> HC_calc(vector<int> curr){
	vector<int> temp, next;
	while(1){
		int minAtk = MAX_INT;
		for(int i=0; i<temp.size()-1; i++)
			for(int j=i; j<temp.size(); j++){
				temp = curr;
				swap(temp[i], temp[j]);
				int tempAtk = checkForAttack(temp);
				if(tempAtk < minAtk){
					next = temp;
					minAtk = tempAtk; 
				}
			}
		if(checkForAttack(next) >= checkForAttack(curr))
			return curr;
		else
			curr = next;
	}
}

bool HC(int n, int &countAtk){
	vector<int> map = mapGenerate(n);
	vector<int> sol = HC_calc(map);
	if(!checkForAttack(sol)){
		cout << "Success!\n";
		return true;
	}
	else{
		cout << "Fail!\n";
		countAtk += attack[sol];
		return false;
	}
}

bool GA(int n, int &countAtk){

}

int main(){
	srand(time(NULL));
	int n, mode, countOpt=0, countAtk=0, times=30;
	cout << "Input n : ";
	cin >> n;
	cout << "Input mode (HC 1, GA 2) : ";
	cin >> mode;
	while(times--){
		if(mode == 1)
			if(HC(n, countAtk))	countOpt++;
		else
			if(GA(n, countAtk))	countOpt++;
	}
	
	cout << "Succedd rate : " << (double)countOpt/times * 100 << "%\n";
	cout << "Average attacks : " << (double)countAtk/times << endl;

}
