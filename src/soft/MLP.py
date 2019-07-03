INPUT_SIZE = 14
import csv
#try:
import numpy as np
import cv2
import keras 
from keras.datasets import mnist
from keras.layers import Dense, Flatten
from keras.models import Sequential
from keras.utils.vis_utils import plot_model

# Load MNIST data
(x1, y_train), (x2, y_test) = mnist.load_data()
x_train = np.array([cv2.resize(x1[i], (INPUT_SIZE, INPUT_SIZE), interpolation = cv2.INTER_AREA) for i in range(len(x1))])
x_test = np.array([cv2.resize(x2[i], (INPUT_SIZE, INPUT_SIZE), interpolation = cv2.INTER_AREA) for i in range(len(x2))])
 
num_classes = 10
 
# Normalize inputs from 0-255 to 0-1
x_train = x_train / 255
x_test = x_test / 255
 
# One hot encode outputs
y_train = keras.utils.to_categorical(y_train, num_classes)
y_test = keras.utils.to_categorical(y_test, num_classes)
 
# Flatten
x_train = x_train.reshape(x_train.shape[0], INPUT_SIZE*INPUT_SIZE).astype('float32')
x_test = x_test.reshape(x_test.shape[0], INPUT_SIZE*INPUT_SIZE).astype('float32')
    
#except:
#    print("Error: Initialization for MLP failed.")

# Print weights to .csv files
def print_weights(model):
    a = model.get_weights()
    for t in range(6, 18, 2):
        for i in range(len(a)):
            File = open(["bias", "weight"][i % 2 == 0] + str(i//2) + "_" + str(t) + ".csv", "w")
            for j in range(len(a[i])):
                try:
                    for k in range(len(a[i][j])):
                        if k != 0: File.write(", ")
                        File.write(("{0:0." + str(t) + "f}").format(a[i][j][k]))
                    File.write("\n")
                except:
                    if j != 0: File.write(", ")
                    File.write(("{0:0." + str(t) + "f}").format(a[i][j]))
            File.close()

# Convert to c code to import weights into Zedboard
def to_c(file_out = "params", num_layers = 4):
    for k in range(6, 18, 2):
        fo = open(file_out + "_" + str(k) + ".h", "w")
        fo.write(
'''/*
 * params.h
 *
 *  Created on: Jun 23, 2019
 *      Author: dangn
 */

#ifndef SRC_PARAMS_H_
#define SRC_PARAMS_H_

''')
        for t in range(num_layers):
            fo.write("#define " + ("WEIGHT" if t < 2 else "BIAS") + "_" + str(t % 2) + " \\\n")
            with open(("weight" if t < 2 else "bias") + str(t % 2) + "_" + str(k) + ".csv") as f:
                a = list(csv.reader(f))
                for i in range(len(a)):
                    fo.write("/*{:>3}*/\t".format(i) + ["{"," "][i>0] + "{")
                    for j in range(len(a[0])):
                        if j != 0: fo.write(",")
                        a[i][j] = a[i][j].lstrip() 
                        fo.write((" "*(a[i][j][0] != '-')) + a[i][j])
                    fo.write("}" + (",\\\n" if i != len(a)-1 else "}\n"))
            if t != num_layers - 1: fo.write("\n"*3)
        fo.write(
'''
#endif /* SRC_PARAMS_H_ */
''')
        fo.close()

def to_c2(file_out = "params_explicit", num_layers = 4):
    for k in range(6, 18, 2):
        fo = open(file_out + "_" + str(k) + ".h", "w")
        fo.write(
'''/*
 * params.h
 *
 *  Created on: Jun 23, 2019
 *      Author: dangn
 */

#ifndef SRC_PARAMS_H_
#define SRC_PARAMS_H_

''')
        for t in range(num_layers):
            fo.write("#define " + ("WEIGHT" if t < 2 else "BIAS") + "_" + str(t % 2) + " \\\n")
            with open(("weight" if t < 2 else "bias") + str(t % 2) + "_" + str(k) + ".csv") as f:
                a = list(csv.reader(f))
                for i in range(len(a)):
                    for j in range(len(a[0])):
                        fo.write("\t" + ("w" if t < 2 else "b") + str(t % 2) + ("[%3d][%3d] = " % (i, j)))
                        a[i][j] = a[i][j].lstrip() 
                        fo.write((" "*(a[i][j][0] != '-')) + a[i][j] + ';\\\n')
    
            if t != num_layers - 1: fo.write("\n"*3)
        fo.write(
'''
#endif /* SRC_PARAMS_H_ */
''')
        fo.close()

# Define MLP model
def MLP(num_layers = 1, num_units = 1):
    # Create layers
    model = Sequential()
    model.add(Dense(num_units, activation='relu', input_shape=(INPUT_SIZE*INPUT_SIZE,)))
    model.add(Dense(num_classes, activation='softmax'))
    # Compile model
    '''
    model.compile(loss=keras.losses.categorical_crossentropy,
                    optimizer=keras.optimizers.SGD(lr=0.1),
                    metrics=['accuracy'])
    '''
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

    # Fit the model
    model.fit(x_train, y_train, batch_size=128, epochs=20)

    # Evaluate the model
    score = model.evaluate(x_test, y_test, verbose=0)
    print('Test loss: %.4f'% score[0])
    print('Test accuracy %.4f'% score[1])
    
    # Visualize the model
    plot_model(model, to_file="model.png", show_shapes=True, show_layer_names=True) 

    return model

print(
"""
Instruction:
###########################################################################################
#                                                                                         #
#   This program defines a function that helps you create a Multilayer Perceptron model   #
#   with user-defined number of hidden layers and number of units in each layer.          #
#                                                                                         #
#   To create one and evaluate it, use the following syntax:                              #
#                                                                                         #
#           model = MLP(<num_layers>, <num_units>)                                        #
#                                                                                         #
#   where <num_layers> is an integer indicates the number of hidden layers of the         #
#   model and <num_units> is a list of integers correspond to the number of units         #
#   in each layer.                                                                        #
#                                                                                         # 
#   FEATURES:                                                                             #
#   1. print_weights(model)                                                               #
#   Use this function to save weights of object model into .csv files                     #
#                                                                                         #
#   2. to_c()                                                                             #
#   Use this function to convert the weights into c code ('layers.h')                     #
#                                                                                         #
###########################################################################################
"""
)
