# dotsandboxes
Dots and Boxes

## Requirements
* Python 3
* Numpy
* Tensorflow 1.1 or greater

## Instructions

#### Training a Model

To train a functional model, simply run the command

`python3 src/sim.py`

Currently, this file is hard-coded to halt at 10,000 iterations. Since the current model has already been trained on 10,000 iterations, you must either change the previous number in the sim.py file AND create a models folder in the same directory and a size3 folder inside it to successfully run the code. This parameter is denoted by `n_games`.

To train a tabular model, simple run execute table_game.py

