#include <bits/stdc++.h>
using namespace std;

const string IMAGES_DATA    = "../images.txt";
const string LABELS_DATA    = "../labels.txt";
const string FILE_OUT       = "KNN_output.txt";
const int MAXN              = 10000;
const int S_TEST            = 0;
const int T_TEST            = 1000;
const int S_TRAINING        = 1000;
const int T_TRAINING        = MAXN;
const int INF               = 255*255 + 1;

ofstream out(FILE_OUT);

int images[MAXN][28*28];
int labels[MAXN];

void readData(){
    ifstream img_in(IMAGES_DATA);
    ifstream lbl_in(LABELS_DATA);

    for (int n = 0 ; n < MAXN ; ++n){
        for (int i = 0 ; i < 28*28 ; ++i){
            img_in >> images[n][i];
        }
        lbl_in >> labels[n];
    }

    img_in.close();
    lbl_in.close();
}
void showImage(int n){
    for (int i = 0 ; i < 28 ; ++i){
        for (int j = 0 ; j < 28 ; ++j){
            out << setw(3) << left << images[n][i*28 + j];
        }
        out << endl;
    }
}
void KNN(){
    int K = 5; // K as of K-nearest neighbour
    int N = 10; // Number of test
    int occurrence[10];
    int predict;
    double distance;
    pair<double, int> nearest[K]; // <distance, label> 
    


    for (int n = S_TEST ; n < T_TEST ; ++n){
        // Init 
        memset(occurrence, 0, sizeof(occurrence));
        for (int i = 0 ; i < K ; ++i) nearest[i] = {INF, -1};


        // Find K nearest neighbours
        for (int k = S_TRAINING ; k < T_TRAINING ; ++k){
            // Calculate distance from images[n] to images[k]
            distance = 0;
            for (int i = 0 ; i < 28*28 ; ++i) distance += pow(images[n][i] - images[k][i], 2); 
            distance = sqrt(distance);
            cout << distance << endl;

            // If images[k] is nearer, add it to the list
            for (int i = 0 ; i < K ; ++i){
                if (distance < nearest[i].first){
                    occurrence[labels[k]]++; 
                    for (int j = K-1 ; j > i ; j--){
                        if (j == K-1 && nearest[j].first != INF){
                            occurrence[nearest[j].second]--;
                        }
                        nearest[j] = nearest[j-1];
                    }
                    nearest[i] = {distance, labels[k]};
                    break; 
                }
            }
        }


        // Print prediction 
        int omax = occurrence[0];
        predict = 0;
        for (int i = 1 ; i < 10 ; ++i){
            if (occurrence[i] > omax){
                omax = occurrence[i];
                predict = i;
            }
        }
        out << predict << endl;
    }
}
int main(){
    readData();
    KNN();
    return 0;
}
