#include <stdio.h>
#include <stdlib.h>
#include "xil_printf.h"
#include "sleep.h"
#include "mlp.h"
#include "matrix.h"

#define INPUT_SIZE			784
#define BUFFER_SIZE 		(INPUT_SIZE*3 + INPUT_SIZE)
#define IDLE_STATE 			1
#define EXECUTION_STATE 	2
#define RESULT_STATE 		3

int main(){

	char buffer[3136];
	char* token = strtok(str, ",");
	int state = IDLE_STATE;
	int result = -1;
	Matrix input = new_matrix(1, INPUT_SIZE);

	while (1) {
		switch (state) {
			case IDLE_STATE:
				/*
				 *
				 * 	To be fix by Hieu
				 *
				 */
				gets(buffer);

//				Normalize input to 0-1
//				for (int i = 0 ; i < INPUT_SIZE ; ++i)
//					input.at[0][i] /= 255.0;

				state = EXECUTION_STATE;
				break;
				
			case EXECUTION_STATE:
				input = strtok(buffer, ",");
				//result = MLP(input);
				state = RESULT_STATE;
				break;

			case RESULT_STATE:
				/*
				 *
				 * 	To be fix by Hieu
				 *
				 */
				state = IDLE_STATE;
				break;

			default:
				state = IDLE_STATE;
				break;
		}
	}
	return 0;
}
