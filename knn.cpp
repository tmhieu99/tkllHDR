#include <bits/stdc++.h>
using namespace std;

const string IMAGES_DATA = "images.txt";
const string LABELS_DATA = "labels.txt";

int images[10000][28*28];
int labels[10000];

void readData(){
    ifstream img_in(IMAGES_DATA);
    ifstream lbl_in(LABELS_DATA);

    for (int n = 0 ; n < 10000 ; ++n){
        for (int i = 0 ; i < 28*28 ; ++i){
            img_in >> images[n][i];
        }
        lbl_in >> labels[n];
    }

    img_in.close();
    lbl_in.close();
}
void KNN(){
    int K = 9;
    int ntest = 10;
    double distance = 0;
    pair<double, int> result[K]; // <distance, label> 
    
    for (int n = 9000 ; n < 9000 + ntest; ++n){
        // Init 
        for (int i = 0 ; i < K ; ++i){
            result[i] = {255*255 + 1, -1};
        }

        // Print digit image
        for (int i = 0 ; i < 28 ; ++i){
            for (int j = 0 ; j < 28 ; ++j){
                cout << setw(3) << left << images[n][i*28 + j];
            }
            cout << endl;
        }

        // Calculate distances from current digit to other labels
        for (int k = 0 ; k < 9000 ; ++k){
            for (int i = 0 ; i < 28*28 ; ++i){
                distance += pow(images[n][i] - images[k][i], 2); 
            }
            distance = sqrt(distance);

            // Record K nearest neighbours
            int i;
            for (i = 0 ; i < K ; ++i){
                if (distance < result[i].first)
                    break;
            }
            if (i < K){
                for (int j = K-1 ; j > i ; --j){
                    result[j] = result[j-1];
                }
                result[i] = {distance, labels[k]};
            }
        }

        // Print prediction result
        cout << K << " nearest neighbours" << endl;
        cout << "(" << result[0].second;
        for (int i = 1 ; i < K ; ++i){
            cout << ", " << result[i].second; 
        }
        cout << ")" << endl;

        // Print exact result
        cout << "Exact result: " << labels[n] << endl;
        cout << endl;
    }
}
int main(){
    readData();
    KNN();
    return 0;
}
