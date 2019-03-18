#include <bits/stdc++.h>
using namespace std;

const string FILE_INP = "train-images-idx3-ubyte";
const string FILE_OUT = "images.txt";

ifstream inp(FILE_INP, ios::binary);
ofstream out(FILE_OUT);
int magic, n, nrow, ncol;
int amount;
unsigned char* data;

int read32(){
    int n;
    inp.read((char*)&n, sizeof(n));
    // Convert from high-endian to low-endian
    n = (n >>  8) & 0x00ff00ff | (n <<  8) & 0xff00ff00;
    n = (n >> 16) & 0x0000ffff | (n << 16) & 0xffff0000;
    return n;
}

int main(){
    // Read MNIST header
    magic   = read32();
    n       = read32();
    nrow    = read32();
    ncol    = read32();

    // Read MNIST data
    data = new unsigned char [n*nrow*ncol];
    inp.read((char*)data, sizeof(unsigned char)*n*nrow*ncol);

    for (int t = 0 ; t < 10000 ; ++t){
        for (int i = 0 ; i < nrow ; ++i){
            for (int j = 0 ; j < ncol ; ++j){
                out << setw(4) << left << (int)(data[nrow*ncol*t + i*ncol + j]);
            }
            out << endl;
        }
        out << endl;
    }
    return 0;
}
