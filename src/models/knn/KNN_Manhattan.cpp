// K-Nearest Neighbor using Euclidean distance on digit recognition
// Dataset used: MNIST dataset

#include <bits/stdc++.h>
using namespace std;



// Global constants
#define IMAGES_DATA     "train-images-idx3-ubyte"
#define LABELS_DATA     "train-labels-idx1-ubyte"
#define RESULT_OUT      "result_M.txt"
#define DETAILS_OUT     "details_M.txt"
#define MAXN            10000                   // Size of the dataset 
#define TRAIN_SET_SIZE  ((int)(MAXN*0.9))       // 90% of the dataset
//#define TEST_SET_SIZE   MAXN - TRAIN_SET_SIZE   // The rest
#define TEST_SET_SIZE   10
#define S_TEST          0
#define T_TEST          TEST_SET_SIZE
#define S_TRAINING      TEST_SET_SIZE
#define T_TRAINING      TEST_SET_SIZE + TRAIN_SET_SIZE
#define INF             65026                   // = 255*255 + 1



// Global variables
ofstream out(RESULT_OUT);
ofstream details(DETAILS_OUT);
unsigned char* images;
unsigned char* labels;
int correct = 0;



// Prototypes
void readData();                        // readData: Load data from MNIST dataset
void showImage(ostream &out, int n);    // showImage: Print greyscale matrix of the n-th image
int  showLabel(int n);                  // showLabel: Print the corresponding label of the n-th image
void KNN();                             // KNN: Main K-nearest neighbor algorithm
void reportResult(ostream &out);        // reportResult: Show statistical result



void readData(){
    // Open images and labels data files
    ifstream iinp(IMAGES_DATA, ios::binary);
    ifstream linp(LABELS_DATA, ios::binary);

    // Skip over MNIST headers
    iinp.seekg(sizeof(int)*4);
    linp.seekg(sizeof(int)*2);

    // Read MNIST data
    images = new unsigned char [MAXN*28*28];
    labels = new unsigned char [MAXN];
    iinp.read((char*)images, sizeof(unsigned char)*MAXN*28*28);
    linp.read((char*)labels, sizeof(unsigned char)*MAXN);
}

void showImage(ostream &out, int n){
    for (int i = 0 ; i < 28 ; ++i){
        for (int j = 0 ; j < 28 ; ++j){
            out << setw(3) << left << (int)images[n*28*28 + i*28 + j];
        }
        out << endl;
    }
}

int showLabel(int n){
    return (int)labels[n];; 
}

void showProgress(int n){
    if (n % (TEST_SET_SIZE / 10) == 0)
        cout << n / (TEST_SET_SIZE / 10) * 10 << "%" << endl;
}

void KNN(ostream &out){
    int K = 5; // K as of K-nearest neighbour
    int occurrence[10];
    int predict;
    double distance;
    pair<double, int> nearest[K]; // <distance, label> 
    


    for (int n = S_TEST ; n < T_TEST ; ++n){
        // Show Image
        //showImage(out, n);
        
        // Show progress
        //showProgres(n);

        // Init 
        memset(occurrence, 0, sizeof(occurrence));
        for (int i = 0 ; i < K ; ++i) nearest[i] = {INF, -1};


        // Find K nearest neighbours
        for (int k = S_TRAINING ; k < T_TRAINING ; ++k){
            // Calculate distance from images[n] to images[k]
            distance = 0;
            for (int i = 0 ; i < 28*28 ; ++i) 
                distance += abs(images[n*28*28+i] - images[k*28*28+i]); 

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
        out << "Predict: " << setw(8) << left << predict << "Result: " << (predict == showLabel(n) ? "Correct" : "Wrong") << "\n\n";
        correct += predict == showLabel(n);
    }
}

void reportResult(ostream &out){
    out << "No. of correct: " << correct << '/' << TEST_SET_SIZE << endl;
    out << "Error rate: " << 1 - correct*1.0/TEST_SET_SIZE << endl;
}

int main(){
    readData();
    KNN(details);
    reportResult(out);
    cout << "DONE" << endl;
    return 0;
}
