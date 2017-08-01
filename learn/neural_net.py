import random
import math
from itertools import chain

from learn.basic import BaseMoveTracker, BasePlayer

# TODO: convert all boards to white

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

    def move(self, board_list):
        outputs = []
        for board in board_list:
            hidden_activations = self.feed_to_hidden_layer(board)
            output = self.feed_to_output(hidden_activations)
            outputs.append(output)
        index = self.softmax_choose(outputs)
        return board_list[index]

    @classmethod
    def sigmoid(cls, val):
        return 1.0 / (1 + math.exp(-1* val))

    def feed_to_hidden_layer(self, board):
        flat_board = list(chain.from_iterable(board))
        assert len(flat_board) == 56
        sigmoid_activations = {}
        for neuron_index in range(self.HIDDEN_LAYER_NEURONS):
            neuron_weights = self.input_to_hidden_weights[neuron_index]
            assert len(neuron_weights) == len(flat_board)
            activation = 0.0
            for i in range(len(flat_board)):
                activation += neuron_weights[i]*flat_board[i]
            activation += self.input_to_hidden_biases[neuron_index]
            sigmoid_activations[neuron_index] = self.sigmoid(activation)
        return sigmoid_activations

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
        self.backpropagate()
        self.reset_move_tracking()

    def backpropagate(self):
        pass


if __name__ == '__main__':
    print NeuralNetMover().softmax_choose([33, 4, 1, 13])





