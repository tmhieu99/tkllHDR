/*
 * main.c
 *
 *  Created on: Jul 2, 2019
 *      Author: dangn
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include "xil_printf.h"
#include "xil_mmu.h"
#include "operations.h"
#include "params.h"

int main(){
	char buffer[BUFFER_SIZE];
	char* token;
	int state = IDLE_STATE;
	int result;

	// Declare layers of the neural networks
	double input[1][LAYER_INPUT];
	double hidden[1][LAYER_1];
	double output[1][LAYER_OUTPUT];

	// Disable Memory Management Unit
	Xil_DisableMMU();

	// Initialize weights and biases
	init_weight_0();
	init_weight_1();
	init_bias_0();
	init_bias_1();

	while (1) {
		switch (state) {
			case IDLE_STATE:
				// Reset variables
				memset(hidden, 0, sizeof(hidden[0][0])*LAYER_1);
				memset(output, 0, sizeof(output[0][0])*LAYER_OUTPUT);

				// Waiting for input data
				gets(buffer);
				state = EXECUTION_STATE;
				break;
				
			case EXECUTION_STATE:
				// Sparse input data
				token = strtok(buffer, ",");
				int i = 0;
				while (token != NULL){
					input[0][i] = 0;
					for (int j = 0 ; j < strlen(token) ; ++j)
						input[0][i] = input[0][i]*10 + token[j] - '0';
					token = strtok(NULL, ",");
					i++;
				}

				// Normalize input to 0-1
				for (int i = 0 ; i < LAYER_INPUT ; ++i)
					input[0][i] /= 255.0;

				//MUL(hidden, input,  w0);
				for (int i = 0; i < LEN(hidden) ; i++)
					for (int k = 0; k < LEN(hidden[0]) ; k++)
						for (int j = 0; j < LEN(w0) ; j++)
							hidden[i][j] += input[i][k] * w0[k][j];

				//ADD(hidden, hidden, b0);
				for (int i = 0 ; i < LEN(hidden) ; ++i)
					for (int j = 0 ; j < LEN(hidden[0]) ; ++j)
						hidden[i][j] = hidden[i][j] + b0[i][j];

				//RELU(hidden);
				for (int i = 0 ; i < LEN(hidden) ; ++i)
					for (int j = 0 ; j < LEN(hidden[0]) ; ++j)
						hidden[i][j] = (hidden[i][j] > 0 ? hidden[i][j] : 0);




				//MUL(output, hidden, w1);
				for (int i = 0; i < LEN(output) ; i++)
					for (int k = 0; k < LEN(output[0]) ; k++)
						for (int j = 0; j < LEN(w1) ; j++)
							output[i][j] += hidden[i][k] * w1[k][j];

				//ADD(output, output, b1);
				for (int i = 0 ; i < LEN(output) ; ++i)
					for (int j = 0 ; j < LEN(output[0]) ; ++j)
						output[i][j] = output[i][j] + b1[i][j];

				//RELU(output);
				for (int i = 0 ; i < LEN(output) ; ++i)
					for (int j = 0 ; j < LEN(output[0]) ; ++j)
						output[i][j] = (output[i][j] > 0 ? output[i][j] : 0);

				//SOFTMAX(output);
			    double sum = 0;
				for(int i = 0 ; i < LEN(output) ; i++)
			    	for (int j = 0 ; j < LEN(output[0]) ; j++)
			            sum += (output[i][j] = exp(output[i][j]));
				for(int i = 0 ; i < LEN(output) ; i++)
			    	for (int j = 0 ; j < LEN(output[0]) ; j++)
			    		output[i][j] /= sum;

//				result = 0;
//				for (int i = 0 ; i < LEN(output[0]) ; i++)
//					if (abs(output[0][i]) > abs(output[0][result]))
//						result = i;

				result = 0;
				for (int i = 0 ; i < LEN(output[0]) ; i++)
					if (output[0][i] > output[0][result])
						result = i;
				state = RESULT_STATE;
				break;

			case RESULT_STATE:
				xil_printf("Result: %d\n", result);
				state = IDLE_STATE;
				break;

			default:
				state = IDLE_STATE;
				break;
		}
	}
	return 0;
}
