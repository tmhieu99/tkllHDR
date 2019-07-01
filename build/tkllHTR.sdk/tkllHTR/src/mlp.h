/*
 * mlp.h
 *
 *  Created on: Jun 16, 2019
 *      Author: tienanh
 */

#ifndef SRC_MLP_H_
#define SRC_MLP_H_

#include <math.h>
#include "xil_printf.h"
#include "operations.h"
#include "params.h"

// Number of units in each layer
#define UNIT_LAYER_INPUT	196
#define UNIT_LAYER_1		64
#define UNIT_LAYER_OUTPUT	10

#define MLP(input) {												\
	xil_printf("Inside MLP\n");										\
    double w0[UNIT_LAYER_INPUT][UNIT_LAYER_1] = WEIGHT_0;			\
    xil_printf("Inside MLP 1\n");									\
    double b0[1][UNIT_LAYER_1] = BIAS_0;							\
    xil_printf("Inside MLP 2\n");									\
    double w1[UNIT_LAYER_1][UNIT_LAYER_OUTPUT] = WEIGHT_1;			\
    xil_printf("Inside MLP 3\n");									\
    double b1[1][UNIT_LAYER_OUTPUT] = BIAS_1;						\
    xil_printf("Inside MLP 4\n");									\
    																\
    double hidden[1][UNIT_LAYER_1];									\
    MUL(hidden, input,  w0);										\
    ADD(hidden, hidden, b0);										\
    RELU(hidden);													\
																	\
	xil_printf("Inside MLP 5\n");									\
    double output[1][UNIT_LAYER_OUTPUT];							\
    MUL(output, hidden, w1);										\
    ADD(output, output, b1);										\
    RELU(output);													\
    SOFTMAX(output);												\
    																\
	xil_printf("Inside MLP 6\n");									\
	result = 0;														\
    for (int i = 0 ; i < LEN(output[0]) ; i++)						\
    	if (output[0][i] > output[0][result])						\
    		result = i;												\
																	\
	xil_printf("Inside MLP 7\n");									\
}

#endif /* SRC_MLP_H_ */
