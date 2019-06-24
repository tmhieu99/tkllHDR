#include <stdio.h>
#include <math.h>

double** new_matrix(int row, int col);
void del_matrix(double** a);
double** add(double** a, double** b);
double** mul(double** a, double** b);

double** ReLU(double** input){
    int row = sizeof(input)/sizeof(double);
    double** result = new_matrix(row, 1);
    for(int i=0; i<row; i++)
        result[i][0] = input[i][0] >= 0 ? input[i][0]:0;
    return result;
}

double SoftMax(double** input){
    int row = sizeof(input)/sizeof(double);
    double** exponential = new_matrix(row, 1);
    for(int i=0; i<row; i++)
        exponential[i][0] = exp(input[i][0]);
    double sum = 0;
    for(int i=0; i<row; i++)
        sum += exponential[i][0];
    for(int i=0; i<row; i++)
        exponential[i][0] /= sum;
    int maxIndex = 0;
    for(int i=1; i<row; i++)
        if (exponential[i][0] > exponential[maxIndex][0])
            maxIndex = i;
    return input[maxIndex][0];
}

double** coeff_1;
double** coeff_2;
double** bias_1;
double** bias_2;

double MLP(double** INPUT){
    double** HIDDEN = new_matrix(1, 64);
    double** OUPUT = new_matrix(1, 10);
    double result;
    
    HIDDEN = ReLU(add(mul(INPUT, coeff_1), bias_1));
    OUPUT  = ReLU(add(mul(HIDDEN, coeff_2), bias_2));
    return result = SoftMax(OUPUT);
}
