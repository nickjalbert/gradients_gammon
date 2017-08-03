# Toy example to check backprop conceptual understanding
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

# Fix an input example
INPUT_A = 3.0
INPUT_B = 4.0
INPUT_EXPECTED_LABEL = 1.0

# Choose some random starting weights and biases
w1 = .5
w2 = .9
w3 = -.3
w4 = .4
w5 = -.1
w6 = .2
hn1_bias = .3
hn2_bias = -.1
output_bias = .2

def sigmoid(x):
    return 1.0 / (1.0 + math.exp(-1 * x))


##### Forward pass #####

# Hidden neuron 1
hn1_input = w1*INPUT_A + w3*INPUT_B + hn1_bias
hn1_forward = sigmoid(hn1_input)
# calculate local gradient of neuron output w.r.t. inputs: 
# sigmoid'(x) = sigmoid(x)*(1-sigmoid(x))
hn1_local_gradient = sigmoid(hn1_input)*(1-sigmoid(hn1_input))

# Hidden neuron 2
hn2_input = w2*INPUT_A + w4*INPUT_B + hn2_bias
hn2_forward = sigmoid(hn2_input)
hn2_local_gradient = sigmoid(hn2_input)*(1-sigmoid(hn2_input)) 

# Output neuron
on_input = w5*hn1_forward + w6*hn2_forward + output_bias
on_forward = sigmoid(on_input) # NN output
on_local_gradient = sigmoid(on_input) * (1-sigmoid(on_input))

# Mean squared error for one example
mean_squared_error = .5 * (INPUT_EXPECTED_LABEL - on_forward)**2
mean_squared_error_local_gradient = (on_forward - INPUT_EXPECTED_LABEL) # Change in mean_squared_error w.r.t. NN output


##### Get our backprop on ######

# Global gradient for the Output Neuron's input
on_global_gradient = on_local_gradient * mean_squared_error_local_gradient
on_bias_global_gradient = on_global_gradient
w5_global_gradient = hn1_forward * on_global_gradient # Tricky 1 - weight gradient is a function of the gradient to the right and the activation (NOT the weight itself)
w6_global_gradient = hn2_forward * on_global_gradient

# Global gradient for Hidden Neuron 1's input
hn1_global_gradient = hn1_local_gradient * w5 * on_global_gradient # Tricky 2 - push the gradient through BOTH the weight AND the neuron
hn1_bias_global_gradient = hn1_global_gradient
w1_global_gradient = INPUT_A * hn1_global_gradient
w3_global_gradient = INPUT_B * hn1_global_gradient

# Global gradient fo rHidden Neuron 2's input
hn2_global_gradient = hn2_local_gradient * w6 * on_global_gradient
hn2_bias_global_gradient = hn2_global_gradient
w2_global_gradient = INPUT_A * hn2_global_gradient
w4_global_gradient = INPUT_B * hn2_global_gradient


##### Check our work #####

def quick_forward_pass():
    output = sigmoid(w5*sigmoid(w1*INPUT_A+w3*INPUT_B+hn1_bias)+w6*sigmoid(w2*INPUT_A+w4*INPUT_B+hn2_bias)+output_bias)
    error = .5 * (INPUT_EXPECTED_LABEL - output)**2
    return output, error

original_output, original_error = quick_forward_pass()
e = .000001
assert abs(original_output - on_forward) < e
assert abs(original_error - mean_squared_error) < e

# Numerically calculate gradients and check against gradients calculated during backprop 
h = .0000001
w1 += h
output, error = quick_forward_pass()
w1 -= h
w1_numerical_gradient = (error - original_error)/h
assert abs(w1_numerical_gradient - w1_global_gradient) < e

w2 += h
output, error = quick_forward_pass()
w2 -= h
w2_numerical_gradient = (error - original_error)/h
assert abs(w2_numerical_gradient - w2_global_gradient) < e

w3 += h
output, error = quick_forward_pass()
w3 -= h
w3_numerical_gradient = (error - original_error)/h
assert abs(w3_numerical_gradient - w3_global_gradient) < e

w4 += h
output, error = quick_forward_pass()
w4 -= h
w4_numerical_gradient = (error - original_error)/h
assert abs(w4_numerical_gradient - w4_global_gradient) < e

w5 += h
output, error = quick_forward_pass()
w5 -= h
w5_numerical_gradient = (error - original_error)/h
assert abs(w5_numerical_gradient - w5_global_gradient) < e

w6 += h
output, error = quick_forward_pass()
w6 -= h
w6_numerical_gradient =  (error - original_error)/h
assert abs(w6_numerical_gradient - w6_global_gradient) < e

hn1_bias += h
output, error = quick_forward_pass()
hn1_bias -= h
hn1_bias_numerical_gradient = (error - original_error)/h
assert abs(hn1_bias_numerical_gradient - hn1_bias_global_gradient) < e

hn2_bias += h
output, error = quick_forward_pass()
hn2_bias -= h
hn2_bias_numerical_gradient = (error - original_error)/h
assert abs(hn2_bias_numerical_gradient - hn2_bias_global_gradient) < e

output_bias += h
output, error = quick_forward_pass()
output_bias -= h
output_bias_numerical_gradient = (error - original_error)/h
assert abs(output_bias_numerical_gradient - on_bias_global_gradient) < e


##### Make the network learn #####

learning_rate = .01
w1 += -1 * learning_rate * w1_global_gradient
w2 += -1 * learning_rate * w2_global_gradient
w3 += -1 * learning_rate * w3_global_gradient
w4 += -1 * learning_rate * w4_global_gradient
w5 += -1 * learning_rate * w5_global_gradient
w6 += -1 * learning_rate * w6_global_gradient 
hn1_bias += -1 * learning_rate * hn1_bias_global_gradient
hn2_bias += -1 * learning_rate * hn2_bias_global_gradient
output_bias += -1 * learning_rate * on_bias_global_gradient

new_output, new_error = quick_forward_pass()

assert new_error < original_error

print 'Original error: {0:.6f}'.format(original_error)
print 'Training network with learning rate of {}'.format(learning_rate)
print 'New error (should be smaller than original): {0:.6f}'.format(new_error)




