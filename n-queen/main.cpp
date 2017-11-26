#include <iostream>
#include <vector>
#include <map>
#include <cstdlib>
#include <ctime>
#include <algorithm>
#include <cstring>

using namespace std;

const int MAX_INT(2147483647);
map<vector<int>, int> attack;

int checkForAttack(vector<int> mp){
	if(attack[mp] != 0){
		if(attack[mp] < 0)
			return 0;
		else
			return attack[mp];
	}
	int size = mp.size();
	bool maze[size+2][size+2];
	memset(maze, false, sizeof(maze));
	for(int i=1; i<=size; i++)
		maze[mp[i-1]][i] = true;
	int cnt = 0;
	for(int i=1; i<=size; i++){
		int y = i;
		int x = mp[i-1];
		for(int j=1; j<size; j++){
			if(x+j<=size && y+j<=size && maze[x+j][y+j])	cnt++;
			if(x+j<=size && y-j>=1 && maze[x+j][y-j])	cnt++;
			if(x-j>=1 && y+j<=size && maze[x-j][y+j])	cnt++;
			if(x-j>=1 && y-j>=1 && maze[x-j][y-j])	cnt++;
		}
	}
	/*
	for(int i=0; i<size; i++)
		cout<<mp[i];
	cout<<endl;
	for(int i=1; i<=size; i++){
		for(int j=1; j<=size; j++)
			if(maze[i][j])	cout<<"1";	else	cout<<"0";
		cout << endl;
	}
	*/
	if(!cnt){
		attack[mp] = -1;
		return 0;
	}
	else{
		attack[mp] = cnt;
	//	cout<<cnt<<endl;
	//	exit(0);
		return cnt;
	}
}

vector<int> mapGenerate(int n){
	vector<int> mp;
	for(int i=1; i<=n; i++){
		int temp = rand()%n + 1;
		while(find(mp.begin(), mp.end(), temp) != mp.end())
			temp = rand()%n + 1;
		mp.push_back(temp);
	}
	return mp;
}

vector<int> HC_calc(vector<int> curr){
	vector<int> temp, next;
	while(1){
		int minAtk = MAX_INT;
		int size = curr.size();
		for(int i=0; i<size-1; i++){
			for(int j=i+1; j<size; j++){
				temp = curr;
				swap(temp[i], temp[j]);
				int tempAtk = checkForAttack(temp);
				if(tempAtk < minAtk){
					next.clear();
					next = temp;
					minAtk = tempAtk;
				}
			}
		}
		if(checkForAttack(next) >= checkForAttack(curr))
			return curr;
		else
			curr = next;
	}
	exit(-1);
}

bool HC(int n, int &countAtk){
	vector<int> mp = mapGenerate(n);
	attack.clear();
	vector<int> sol = HC_calc(mp);
	if(checkForAttack(sol) == 0){
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
	int n, mode, countOpt(0), countAtk(0), time(30);
	cout << "Input n : ";
	cin >> n;
	cout << "Input mode (HC 1, GA 2) : ";
	cin >> mode;
	for(int i=0; i<time; i++){
		if(mode == 1){
			if(HC(n, countAtk))	
				countOpt++;
		}
		else{
			if(GA(n, countAtk))	
				countOpt++;
		}
		//cout<<countAtk<<endl;
	}
	cout << "Succedd rate : " << (double)countOpt/time * 100 << "%\n";
	cout << "Average attacks : " << (double)countAtk/time << endl;

}
