# gradients_gammon

Reinforcement learning with policy gradients for backgammon.   Implementing
ideas related to the
[ATARI game playing paper](http://www.nature.com/nature/journal/v518/n7540/abs/nature14236.html)
and the deep neural network extensions discussed by
Andrej Karpathy [here](http://karpathy.github.io/2016/05/31/rl/).


### Results

This section compares the naive Neural Net found in ```learn/neural_net.py```
with the player that makes random moves found in ```learn/random_mover.py```.

The naive Neural Net has the following properties:
* 56 inputs, 1 hidden layer with 56 fully connected hidden neurons, and
  1 output neuron
* Each neuron uses a sigmoid activation function
* All gradients are determined numerically
* No regularization, implicit sketchy cost function, dumb weight
  initialization, no batching for training
* No tuned hyperparameters
* All training was done against the random moving opponent

The results are as follows:

* A player making random moves beats another player
  making random moves between 44.9% and 53.0% of the time (99% CI).

* After training on 50 games, the naive Neural Net
  beats a player making random moves between 90.4% and 98.5% of the time
  (99% CI).

* After training on 3400 games, the naive Neural Net
  beats a player making random moves between 89.6% and 97.7% of the time
  (99% CI).

