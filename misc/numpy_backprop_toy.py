# Toy example to test out numpy vectorization of backprop
#
#  * Fully connected NN with 1 hidden layer and 1 output neuron
#  * All neurons are sigmoid neurons with a bias 
#  * Use mean squared error (MSE) for 1 example: .5 * (expected - output)**2
#
# Network Architecture (note bias is not shown)
#
#              w1
# (INPUT_A)------------ (hiddenNeuron1)
#         \          /                  \
#       w2  \      /                      \ w5
#             \  /                          \               output
#              /\                            (outputNeuron)--------(MSE)--Error
#            /    \                         /
#       w3 /        \                     / w6
#        /            \                 /
# (INPUT_B)------------ (hiddenNeuron2) 
#              w4
#

import math
import numpy as np


def sigmoid(x):
    return 1.0 / (1.0 + np.exp(-1.0*x))

# Constants
label = 1.0
input_data = np.array([3.0, 4.0]) 
hidden_weights = np.array([[ .5, .9],
                           [-.3, .4]]) 
hidden_bias = np.array([.3, -.1])
output_weights = np.array([[-.1],
                           [ .2]])
output_bias = .2

# Forward pass
hidden_feed_in = input_data.dot(hidden_weights) + hidden_bias #2x1
hidden_activation = sigmoid(hidden_feed_in)
hidden_local_gradient = sigmoid(hidden_feed_in) * (1 - sigmoid(hidden_feed_in))

output_feed_in = hidden_activation.dot(output_weights) + output_bias
output_activation = sigmoid(output_feed_in)
output_local_gradient = sigmoid(output_feed_in) * (1-sigmoid(output_feed_in))

MSE = .5 * (output_activation-label)**2

# Backward pass
output_global_gradient = output_local_gradient * (output_activation-label)

output_weight_gradients = hidden_activation * output_global_gradient
output_bias_gradient = output_global_gradient

hidden_global_gradient = hidden_local_gradient * (output_weights * output_global_gradient).T
w1w2grad = input_data[0] * hidden_global_gradient 
w3w4grad = input_data[1] * hidden_global_gradient
print w3w4grad


hn1_hn2_bias_gradient = hidden_global_gradient

# Sanity check
def ugly_forward_pass():
    output = sigmoid(
            output_weights[0][0]*sigmoid(
                    hidden_weights[0][0]*input_data[0] + 
                    hidden_weights[1][0]*input_data[1] +
                    hidden_bias[0]) +
            output_weights[1][0]*sigmoid(
                    hidden_weights[0][1]*input_data[0] +
                    hidden_weights[1][1]*input_data[1] +
                    hidden_bias[1]) +
            output_bias)
    error = .5 * (label - output)**2
    return output, error

original_output, original_error = ugly_forward_pass()
e = .000001
assert abs(original_output - output_activation) < e
assert abs(original_error - MSE) < e

# Numerically calculate gradients and check against gradients calculated during backprop 
h = .0000001
hidden_weights[0][0] += h
output, error = ugly_forward_pass()
hidden_weights[0][0] -= h
w1_numerical_gradient = (error - original_error)/h
assert abs(w1_numerical_gradient - w1w2grad[0][0]) < e


hidden_weights[0][1] += h
output, error = ugly_forward_pass()
hidden_weights[0][1] -= h
w2_numerical_gradient = (error - original_error)/h
assert abs(w2_numerical_gradient - w1w2grad[0][1]) < e

hidden_weights[1][0] += h
output, error = ugly_forward_pass()
hidden_weights[1][0] -= h
w3_numerical_gradient = (error - original_error)/h
assert abs(w3_numerical_gradient - w3w4grad[0][0]) < e

hidden_weights[0][1] += h
output, error = ugly_forward_pass()
hidden_weights[0][1] -= h
w4_numerical_gradient = (error - original_error)/h
print w4_numerical_gradient
print w3w4grad
#assert abs(w4_numerical_gradient - w3w4grad[0][1]) < e

output_weights[0][0] += h
output, error = ugly_forward_pass()
output_weights[0][0] -= h
w5_numerical_gradient = (error - original_error)/h
assert abs(w5_numerical_gradient - output_weight_gradients[0]) < e

output_weights[1][0] += h
output, error = ugly_forward_pass()
output_weights[1][0] -= h
w6_numerical_gradient =  (error - original_error)/h
assert abs(w6_numerical_gradient - output_weight_gradients[1]) < e

hn1_bias += h
output, error = ugly_forward_pass()
hn1_bias -= h
hn1_bias_numerical_gradient = (error - original_error)/h
assert abs(hn1_bias_numerical_gradient - hn1_bias_global_gradient) < e

hn2_bias += h
output, error = ugly_forward_pass()
hn2_bias -= h
hn2_bias_numerical_gradient = (error - original_error)/h
assert abs(hn2_bias_numerical_gradient - hn2_bias_global_gradient) < e

output_bias += h
output, error = ugly_forward_pass()
output_bias -= h
output_bias_numerical_gradient = (error - original_error)/h
assert abs(output_bias_numerical_gradient - on_bias_global_gradient) < e








