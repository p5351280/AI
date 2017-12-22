#include <iostream>
#include <vector>
#include <map>
#include <cstdlib>
#include <ctime>
#include <algorithm>
#include <cstring>
#include <queue>

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

vector<int> HC_calc(int size){
	vector<int> curr = mapGenerate(size);
	vector<int> temp, next;
	while(1){
		int minAtk = MAX_INT;
		for(int i=0; i<size-1; i++){	// swap each column is a kind of neighbor
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

bool checkInMap(vector<int> mp, int target, int start, int end){	// function for crossover to use
	for(int i=start; i<=end; i++)
		if(mp[i] == target)    return true;
	return false;
}

vector<int> crossover(vector<int> p1, vector<int> p2){	// PMX
	/*
	   for(int j=0; j<9; j++)
	   cout<<p1[j]<<" ";
	   cout<<endl;
	   for(int j=0; j<9; j++)
	   cout<<p2[j]<<" ";
	   cout<<endl;
	 */
	int size = p1.size();
	int start = rand() % size, end = rand() % size;	// choose substring random
	if(start > end)	swap(start, end);
	//cout<<start<<" "<<end<<endl;
	int mapList[10000] = {0}, i;
	for(i=start; i<=end; i++)
		mapList[p1[i]] = p2[i];
	vector<int> child = p2;
	for(i=start; i<=end; i++)
		child[i] = p1[i];
	/*
	   for(int j=0; j<9; j++)
	   cout<<child[j]<<" ";
	   cout<<endl;
	 */
	for(i=0; i<start; i++){
		if(mapList[child[i]]){
			int target = mapList[child[i]];
			while(checkInMap(child, target, start, end))
				target = mapList[target];
			child[i] = target;
		}
	}
	for(i=end+1; i<child.size(); i++){
		if(mapList[child[i]]){
			int target = mapList[child[i]];
			while(checkInMap(child, target, start, end))
				target = mapList[target];
			child[i] = target;
		}
	}
	/*
	   for(int j=0; j<9; j++)
	   cout<<child[j]<<" ";
	   cout<<endl<<endl;
	 */
	return child;
}

vector<int> mutation(vector<int> curr){	// random choose two, and do swap
	int a = rand() % curr.size();
	int b = rand() % curr.size();
	swap(curr[a], curr[b]);
	return curr;
}

struct comp{
	bool operator() (const vector<int> x, const vector<int> y){
		return checkForAttack(x) > checkForAttack(y);
	}
};

vector<int> GA_calc(int size, int countGroup = 100, int round = 250){	// population size = 100, do 250 rounds
	priority_queue<vector<int>, vector<vector<int> >, comp> group, newGroup;
	for(int i=0; i<countGroup; i++){
		vector<int> temp = mapGenerate(size);
		group.push(temp);
	}

	for(int i=0; i<round; i++){
		while(!newGroup.empty())	newGroup.pop();	// clear
		for(int j=0; j<countGroup-1; j++){
			vector<int> a = group.top();	// parent is choose by (0, 1), (1, 2), (2, 3)...
			newGroup.push(a);
			group.pop();
			vector<int> b = group.top();
			vector<int> child = crossover(a, b);
			child = mutation(child);
			newGroup.push(child);
		}
		if(checkForAttack(newGroup.top()) == 0)
			break;
		else
			group = newGroup;
	}

	return newGroup.top();
}

int main(int argc, char* argv[]){

	srand(time(NULL));
	int n, mode, countOpt(0), countAtk(0), time(30);
	if(argc == 1){
		cout << "Input n : ";
		cin >> n;
		cout << "Input mode (HC 1, GA 2) : ";
		cin >> mode;
	}
	else{
		n = atoi(argv[1]);	// for time test, can just use arg
		mode = atoi(argv[2]);
	}
	for(int i=0; i<time; i++){
		if(mode == 1){
			vector<int> sol = HC_calc(n);
			int atk = checkForAttack(sol);
			if(!atk){
				cout << "Success!\n";
				countOpt++;
			}
			else{
				cout << "Fail!\n";
				countAtk += atk;
			}
		}
		else{
			vector<int> sol = GA_calc(n);
			int atk = checkForAttack(sol);
			if(!atk){
				cout << "Success!\n";
				countOpt++;
			}
			else{
				cout << "Fail\n";
				countAtk++;
			}
		}
		//cout<<countAtk<<endl;
	}
	cout << "Success rate : " << (double)countOpt/time * 100 << "%\n";
	cout << "Average attacks : " << (double)countAtk/time << endl;
	/*
	   for(int i=0; i<100; i++){
	   vector<int> mp1 = mapGenerate(9);
	   vector<int> mp2 = mapGenerate(9);
	   vector<int> mp3 = crossover(mp1, mp2);
	   }
	 */
}
