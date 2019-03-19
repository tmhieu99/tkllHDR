#include <bits/stdc++.h>
using namespace std;

int main(){
    ifstream lbl("../labels.txt"), knn("KNN_Manhattan_output.txt");    
    int error = 0;
    int a, b;

    for (int i = 0 ; i < 1000 ; ++i){
        lbl >> a;
        knn >> b;
        error += a != b;
    }
    cout << 1 - error/1000.0 << endl; 
    return 0;
}
