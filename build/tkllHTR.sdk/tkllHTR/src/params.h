/*
 * params.h
 *
 *  Created on: Jul 2, 2019
 *      Author: dangn
 */

#ifndef SRC_PARAMS_H_
#define SRC_PARAMS_H_

#include "main.h"

extern double w0[LAYER_INPUT][LAYER_1];
extern double b0[1][LAYER_1];
extern double w1[LAYER_1][LAYER_OUTPUT];
extern double b1[1][LAYER_OUTPUT];

void init_weight_0();
void init_weight_1();
void init_bias_0();
void init_bias_1();

#endif /* SRC_PARAMS_H_ */
