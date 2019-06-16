/*
 * matrix.c
 *
 *  Created on: Jun 16, 2019
 *      Author: dangn
 */

#include <stdlib.h>

int** new_matrix(int row, int col){
	int** a = malloc(row*sizeof(*a));
	for (int i = 0 ; i < row ; ++i) a[i] = malloc(col*sizeof(a[i]));
	return a;
}

void del_matrix(int** a, int a_row){
	for (int i = 0 ; i < a_row ; ++i) free(a[i]);
	free(a);
}

int** add(int** a, int** b, int a_row, int a_col, int b_row, int b_col){
	if (a_row != b_row || a_col != b_col){
		xil_printf("ERROR: Matrices dimensions mismatch.\n\r");
		return 0; // return NULL
	}

	int** c = new_matrix(a_row, a_col);

	for (int i = 0 ; i < a_row ; ++i){
		for (int j = 0 ; j < a_col ; ++j){
			c[i][j] = a[i][j] + b[i][j];
		}
	}

	return c;
}


int** mul(int** a, int** b, int a_row, int a_col, int b_row, int b_col){

}
