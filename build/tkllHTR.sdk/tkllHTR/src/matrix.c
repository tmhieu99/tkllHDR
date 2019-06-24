/*
 * matrix.c
 *
 *  Created on: Jun 16, 2019
 *      Author: dangn
 */

#include <stdlib.h>
#include "xil_printf.h"
#include "matrix.h"

Matrix new_matrix(int row, int col){
    Matrix m;
    m.row = row;
    m.col = col;
	m.at = (double**) malloc(row*sizeof(double*));
	for (int i = 0 ; i < row ; ++i)
        m.at[i] = (double*) malloc(col*sizeof(double));
	return m;
}

Matrix add(Matrix a, Matrix b){
    Matrix c;
	if (a.row != b.row || a.col != b.col){
		xil_printf("Error: Matrices dimensions mismatch.\n\r");
		return c; // return NULL
	}

	c = new_matrix(a.row, a.col);

	for (int i = 0 ; i < c.row ; ++i)
		for (int j = 0 ; j < c.col ; ++j)
			c.at[i][j] = a.at[i][j] + b.at[i][j];

	return c;
}

Matrix mul(Matrix a, Matrix b){
    Matrix c;
	if (a.col != b.row){
		xil_printf("Error: Matrices dimensions mismatch.\n\r");
		return c; // return NULL
	}

	c = new_matrix(a.row, b.col);

	for (int i = 0; i < c.row ; i++)
	    for (int k = 0; k < c.col ; k++)
	        for (int j = 0; j < b.row ; j++)
	            c.at[i][j] += a.at[i][k] * b.at[k][j];

	return c;
}