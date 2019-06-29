/*
 * operations.h
 *
 *  Created on: Jun 16, 2019
 *      Author: dangn
 */

#ifndef SRC_OPERATIONS_H_
#define SRC_OPERATIONS_H_

#include "xil_printf.h"
#include <math.h>

#define LEN(a) (sizeof(a)/sizeof(a[0]))

#define ADD(c, a, b) {																						\
    if (!(LEN(a) == LEN(b) && LEN(a) == LEN(c) && LEN(a[0]) == LEN(b[0]) && LEN(a[0]) == LEN(c[0]))){		\
        xil_printf("Error: Matrices dimensions mismatch.\n");												\
    } else {																								\
        for (int i = 0 ; i < LEN(c) ; ++i)																	\
            for (int j = 0 ; j < LEN(c) ; ++j)																\
                c[i][j] = a[i][j] + b[i][j];																\
    }																										\
}

#define MUL(c, a, b) {																						\
    if (LEN(a[0]) != LEN(b) || (LEN(c) != LEN(a)) || (LEN(c[0]) != LEN(b[0]))){								\
        xil_printf("Error: Matrices dimensions mismatch.\n");												\
    } else {																								\
	    for (int i = 0; i < LEN(c) ; i++)																	\
	        for (int k = 0; k < LEN(c[0]) ; k++)															\
	            for (int j = 0; j < LEN(b) ; j++)															\
	                c[i][j] += a[i][k] * b[k][j];															\
    }																										\
}

#define RELU(a) {																							\
    for (int i = 0 ; i < LEN(a) ; ++i)																		\
        for (int j = 0 ; j < LEN(a[0]) ; ++j)																\
            a[i][j] = (a[i][j] > 0 ? a[i][j] : 0);															\
}

#define SOFTMAX(a) {																						\
    double sum = 0;																							\
	for(int i = 0 ; i < LEN(a) ; i++)																		\
    	for (int j = 0 ; j < LEN(a[0]) ; j++)																\
            sum += (a[i][j] = exp(a[i][j]));																\
	for(int i = 0 ; i < LEN(a) ; i++)																		\
    	for (int j = 0 ; j < LEN(a[0]) ; j++)																\
    		a[i][j] /= sum;																					\
}

#endif /* SRC_OPERATIONS_H_ */
