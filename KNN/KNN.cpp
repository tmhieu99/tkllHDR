#include <bits/stdc++.h>
using namespace std;

const string IMAGES_DATA = "../images.txt";
const string LABELS_DATA = "../labels.txt";
const string FILE_OUT = "KNN_output.txt";

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
    ofstream out(FILE_OUT);
    int K = 9; // K-nearest neighbour
    int N = 10; // Number of test
    double distance = 0;
    pair<double, int> result[K]; // <distance, label> 
    
    for (int n = 9000 ; n < 9000 + N; ++n){
        // Init 
        for (int i = 0 ; i < K ; ++i){
            result[i] = {255*255 + 1, -1};
        }

        // Print digit image
        for (int i = 0 ; i < 28 ; ++i){
            for (int j = 0 ; j < 28 ; ++j){
                out << setw(3) << left << images[n][i*28 + j];
            }
            out << endl;
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
        out << K << " nearest neighbours" << endl;
        out << "(" << result[0].second;
        for (int i = 1 ; i < K ; ++i)
            out << ", " << result[i].second; 
        out << ")" << endl;

        // Print exact result
        out << "Exact result: " << labels[n] << endl << endl;
    }
}
int main(){
    readData();
    KNN();
    return 0;
}
