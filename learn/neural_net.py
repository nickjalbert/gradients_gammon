'''
Extremely basic implementation of a neural network.  Inefficient and naive
but will provide a template for future work.
'''
import math
import random
import pickle
from itertools import chain

from learn.basic import BaseMoveTracker, BasePlayer
from backgammon.utility import swap_colors


'''
Questions:
    
    * Does it make sense to use softmax over the activation of each 
      boards in the list of legal next boards? Especially if we will only
      push the gradient back against the one board we selected.

    * Does it make sense to take the log of the activations to squash the 
      range before softmax?  No, unnecessary if we're using a sigmoid output
      neuron.

    * Should we use rectified neurons or sigmoid activiations functions for
      the hidden layer?  What are the trade-offs?

    * How do we determine a good shape for the network?
'''

class NeuralNetMover(BaseMoveTracker, BasePlayer):
    '''
    Fully connected with one hidden layer.  
        
        * Input layer: 56 non-negative integers.  
        * Hidden layer: 56 fully connected neurons with a sigmoid activiation
        * Output is a single sigmoid neuron

    In general, we use this network as follows:
        * We run a list of legal next board states through the network
        * We log() the activation of each board state
        * We softmax the activations
        * We choose a next board state by rolling a die biased by the softmax

    Once we know the outcome of the game, we train:
        * For each board along the winning rollout, we train network to
          respond with greater activation.
        * For each board along the losing rollout, we train the network to
          respond with weaker activation.
    
    Uses numerical gradients which will be inefficient but (hopefully)
    explicit.

    TODO:
        * Analytic gradients
        * Use a cross-entropy function for cost; choose the highest cost board
          (or still use roulette select?)
        * Regularize cost function
        * Train s.t. losing boards push activation toward zero and winning
          boards push activation toward 1
        * Play against neural network opponent to learn against stronger
          strategies
        * Numpy for efficiency, then keras and/or tensorflow
        * Smarter weight initialization
        * Batch training vs online training?
        * Other hyper parameter tuning (regularization constant, learning rate)
        * Different network architectures
        * Optimize backgammon board generation
    '''
    def __init__(self):
        self.reset_move_tracking()
        self.FLAT_BOARD_SIZE = 56
        self.HIDDEN_LAYER_NEURONS = 56
        self.initialize_weights()

    def initialize_weights(self):
        small_random = lambda: (random.random() - .5)*.01
        small_random_list = lambda x: [small_random() for i in range(x)]
        self.input_to_hidden_weights = {}
        self.input_to_hidden_biases = [0]*self.HIDDEN_LAYER_NEURONS
        for neuron_index in range(self.HIDDEN_LAYER_NEURONS):
            input_weights = small_random_list(self.FLAT_BOARD_SIZE)
            self.input_to_hidden_weights[neuron_index] = input_weights
            self.input_to_hidden_biases[neuron_index] = small_random()
        output_weights = small_random_list(self.HIDDEN_LAYER_NEURONS)
        self.hidden_to_output_weights = output_weights
        self.hidden_to_output_bias = small_random()

    def move(self, is_black_turn, roll, current_board, board_list):
        if is_black_turn:
            board_list = [swap_colors(board) for board in board_list]
        outputs = [self.feed_forward(board) for board in board_list]
        return self.softmax_choose(outputs)

    def feed_forward(self, board):
        hidden_activations = self.feed_to_hidden_layer(board)
        return self.feed_to_output(hidden_activations)

    @classmethod
    def sigmoid(cls, val):
        return 1.0 / (1 + math.exp(-1* val))

    def feed_to_hidden_layer(self, board):
        sigmoid_activations = {}
        for neuron_index in range(self.HIDDEN_LAYER_NEURONS):
            activation = self.feed_to_hidden_neuron(neuron_index, board)
            sigmoid_activations[neuron_index] = activation
        return sigmoid_activations

    def feed_to_hidden_neuron(self, neuron_index, board):
        flat_board = list(chain.from_iterable(board))
        assert len(flat_board) == 56
        neuron_weights = self.input_to_hidden_weights[neuron_index]
        assert len(neuron_weights) == len(flat_board)
        activation = 0.0
        for i in range(len(flat_board)):
            activation += neuron_weights[i]*flat_board[i]
        activation += self.input_to_hidden_biases[neuron_index]
        return self.sigmoid(activation)

    def feed_to_output(self, hidden_activations):
        assert len(hidden_activations) == len(self.hidden_to_output_weights)
        activation = 0.0
        for neuron_index in range(self.HIDDEN_LAYER_NEURONS):
            hidden_activation = hidden_activations[neuron_index]
            weight = self.hidden_to_output_weights[neuron_index]
            activation += hidden_activation*weight
        activation += self.hidden_to_output_bias
        return self.sigmoid(activation)

    def softmax_choose(self, outputs):
        exp_outputs = [math.exp(output) for output in outputs]
        sum_exp_outputs = sum(exp_outputs)
        softmax = [exp_output/sum_exp_outputs for exp_output in exp_outputs]
        return self.roulette_wheel_select(softmax)

    def roulette_wheel_select(self, softmax):
        prefix_sum = [0]
        for probability in softmax:
            prefix_sum.append(probability + prefix_sum[-1])
        prefix_sum.pop()
        choice = random.random()
        for index in range(len(prefix_sum)):
            if index + 1 >= len(prefix_sum):
                return index
            if prefix_sum[index] <= choice < prefix_sum[index+1]:
                return index

    def learn(self):
        self.assert_moves_were_tracked()
        training = self.apply_policy_gradients()
        self.stochastic_gradient_descent(training)
        self.reset_move_tracking()

    def apply_policy_gradients(self):
        training = []
        self.black_moves = [swap_colors(board) for board in self.black_moves]
        training = [(board, self.black_payoff) for board in self.black_moves]
        training += [(board, self.white_payoff) for board in self.white_moves]
        return training

    def stochastic_gradient_descent(self, training):
        for (board, payoff) in training:
            self.backpropagate(board, payoff)

    def backpropagate(self, board, payoff):
        '''
        Calculate gradients numerically.
        '''
        output_old = self.feed_forward(board)
        self.backpropagate_to_hidden_layer(board, payoff)
        self.backpropagate_to_input(board, payoff)
        output_new = self.feed_forward(board)
        if payoff > 0 and output_new < output_old:
            print 'Warning id:1'
        elif payoff < 0 and output_new > output_old:
            print 'Warning id:2'

    def backpropagate_to_hidden_layer(self, board, payoff):
        # Initialize
        self.hidden_to_output_weight_gradients = [0.0]
        self.hidden_to_output_weight_gradients *= self.HIDDEN_LAYER_NEURONS
        self.hidden_to_output_bias_gradient = 0.0

        # Get hidden activations and current output
        hidden_activations = self.feed_to_hidden_layer(board)
        output = self.feed_to_output(hidden_activations)

        # Numerically calculate the gradient for each weight wrt output
        h = .0001
        for neuron_index in range(self.HIDDEN_LAYER_NEURONS):
            self.hidden_to_output_weights[neuron_index] += h
            output_tweaked = self.feed_to_output(hidden_activations)
            self.hidden_to_output_weights[neuron_index] -= h

            gradient = (output_tweaked - output)/h
            self.hidden_to_output_weight_gradients[neuron_index] = gradient

        # Numerically calculate the gradient for the bias wrt output
        self.hidden_to_output_bias += h
        output_tweaked = self.feed_to_output(hidden_activations)
        self.hidden_to_output_bias -= h
        self.hidden_to_output_bias_gradient = (output_tweaked - output)/h

        # Update weights along gradient in direction of the payoff
        step_size = .01
        for neuron_index in range(self.HIDDEN_LAYER_NEURONS):
            weight = self.hidden_to_output_weights[neuron_index]
            gradient = self.hidden_to_output_weight_gradients[neuron_index]
            weight += step_size * gradient * payoff
            self.hidden_to_output_weights[neuron_index] = weight

        # Update bias along gradient in direction of the payoff
        bias = self.hidden_to_output_bias
        bias += step_size * self.hidden_to_output_bias_gradient
        self.hidden_to_output_bias = bias

        output_new = self.feed_to_output(hidden_activations)
        if payoff > 0 and output_new < output:
            print 'Warning id:3'
        elif payoff < 0 and output_new > output:
            print 'Warning id:4'

    def backpropagate_to_input(self, board, payoff):
        # Initialize
        self.input_to_hidden_weight_gradients = {}
        for neuron_index in range(self.HIDDEN_LAYER_NEURONS):
            gradients = [0.0] * self.FLAT_BOARD_SIZE
            self.input_to_hidden_weight_gradients[neuron_index] = gradients
        self.input_to_hidden_bias_gradients = [0.0]*self.HIDDEN_LAYER_NEURONS

        # Numerically calculate gradients for hidden layer weights and biases
        # wrt to the hidden layer neuron's output
        h = .0001
        for neuron_index in range(self.HIDDEN_LAYER_NEURONS):
            output = self.feed_to_hidden_neuron(neuron_index, board)
            for input_index in range(self.FLAT_BOARD_SIZE):
                self.input_to_hidden_weights[neuron_index][input_index] += h
                output_new = self.feed_to_hidden_neuron(neuron_index, board)
                self.input_to_hidden_weights[neuron_index][input_index] -= h
                gradient = (output_new - output)/h
                self.input_to_hidden_weight_gradients[neuron_index][input_index] = gradient
            self.input_to_hidden_biases[neuron_index] += h
            output_new = self.feed_to_hidden_neuron(neuron_index, board)
            self.input_to_hidden_biases[neuron_index] -= h
            gradient = (output_new - output)/h
            self.input_to_hidden_bias_gradients[neuron_index] = gradient

        # Apply chain rule to gradients to update weights and biases
        step_size = .01
        for neuron_index in range(self.HIDDEN_LAYER_NEURONS):
            output_old = self.feed_to_hidden_neuron(neuron_index, board)
            chain_gradient = self.hidden_to_output_weight_gradients[neuron_index]
            for input_index in range(self.FLAT_BOARD_SIZE):
                weight = self.input_to_hidden_weights[neuron_index][input_index]
                local_gradient = self.input_to_hidden_weight_gradients[neuron_index][input_index]
                weight += local_gradient * chain_gradient * step_size * payoff
                self.input_to_hidden_weights[neuron_index][input_index] = weight

            bias = self.input_to_hidden_biases[neuron_index]
            local_gradient = self.input_to_hidden_bias_gradients[neuron_index]
            bias += local_gradient * chain_gradient * step_size * payoff
            self.input_to_hidden_biases[neuron_index] = bias
            output_new = self.feed_to_hidden_neuron(neuron_index, board)
            if payoff > 0 and output_new < output_old:
                print 'Warning id:5'
            elif payoff < 0 and output_new > output_old:
                print 'Warning id:6'

    def save_state(self, path):
        serialized_self = [self.input_to_hidden_weights,
                           self.input_to_hidden_biases,
                           self.hidden_to_output_weights,
                           self.hidden_to_output_bias]
        with open(path, 'wb') as f:
            pickle.dump(serialized_self, f)
    
    def load_state(self, path):
        with open(path, 'rb') as f:
            serialized_self = pickle.load(f)
        self.input_to_hidden_weights = serialized_self[0] 
        self.input_to_hidden_biases = serialized_self[1] 
        self.hidden_to_output_weights = serialized_self[2] 
        self.hidden_to_output_bias = serialized_self[3]


class DumbNeuralNetMover(NeuralNetMover):
    '''Simply applies the neural net but doesn't try to learn'''
    def __init__(self):
        super(DumbNeuralNetMover, self).__init__()

    def learn(self):
        self.assert_moves_were_tracked()
        self.reset_move_tracking()

    def move(self, is_black_turn, roll, current_board, board_list):
        if is_black_turn:
            board_list = [swap_colors(board) for board in board_list]
        outputs = [self.feed_forward(board) for board in board_list]
        return max(enumerate(outputs), key=lambda x: x[1])[0]

    def save_state(self, path):
        pass


if __name__ == '__main__':
    print NeuralNetMover().softmax_choose([33, 4, 1, 13])





