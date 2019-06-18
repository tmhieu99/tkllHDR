import numpy as np
import keras 
from keras.datasets import mnist
from keras.layers import Dense, Flatten
from keras.models import Sequential
from keras.utils.vis_utils import plot_model

# Load MNIST data
(x_train, y_train), (x_test, y_test) = mnist.load_data()
num_classes = 10

# Normalize inputs from 0-255 to 0-1
x_train = x_train / 255
x_test = x_test / 255

# One hot encode outputs
y_train = keras.utils.to_categorical(y_train, num_classes)
y_test = keras.utils.to_categorical(y_test, num_classes)

# Flatten
x_train = x_train.reshape(x_train.shape[0], 28*28).astype('float32')
x_test = x_test.reshape(x_test.shape[0], 28*28).astype('float32')

# Define MLP model
def print_weights(model):
    a = model.get_weights()
    for i in range(len(a)):
        File = open("layer" + str(i) + ".csv", "w")
        for j in range(len(a[i])):
            try:
                for k in range(len(a[i][j])):
                    File.write("{0:0.25f}, ".format(a[i][j][k]))
                File.write("\n")
            except:
                File.write("{0:0.25f}, \n".format(a[i][j]))
        File.close()

def MLP(num_layers = 1, num_units = 1):
    # Create layers
    model = Sequential()
    model.add(Dense(num_units, activation='relu', input_shape=(784,)))
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
###########################################################################################
"""
)
