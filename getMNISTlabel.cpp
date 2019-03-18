#include <bits/stdc++.h>
using namespace std;

const string FILE_INP = "train-labels-idx1-ubyte";
const string FILE_OUT = "labels.txt";

ifstream inp(FILE_INP, ios::binary);
ofstream out(FILE_OUT);
int magic, n;
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

    // Read MNIST data
    data = new unsigned char [n];
    inp.read((char*)data, sizeof(unsigned char)*n);

    for (int i = 0 ; i < 10000 ; ++i){
        out << (int)(data[i]) << endl;
    }
    return 0;
}
