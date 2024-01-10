
# Bryce Shakespeares Repository
Contains projects outside of work entirely produced by myself. Does not contain many uni files either due to potential plagiarism or licensing issues.

Summary of files in order of interest:

### Estimating the Booundary of Hyperbolic Groups
This contains the coding files for my thesis, which aimed to generate and plot the boundary of hyperbolic group. 
The primary functions to generate points are done in [GAP](https://www.gap-system.org/) 'a system for computational discrete algebra, with particular emphasis on Computational Group Theory'. The points generated via GAP were then evaluated and plotted via Python, the specific technique is [MDS](https://scikit-learn.org/stable/modules/generated/sklearn.manifold.MDS.html) via sklearn.

#### distance-matrix-generation-functions.g (Examples and time testing.g)
(only runs in linux)
GAP file containing functions used to generate dissimilarity matrices for spheres of small cancellation groups
Tutorial and testing.g gives example and generates some tables on runtime

##### MDS and CSV functions.py
Takes the output csv from the `distance-matrix-generation-functions.g` functions, converts to readable form and uses MDS to generate plots in euclidian space.

##### Examples and time testing.g
Use of the functions found in `distance-matrix-generation-functions.g` on different groups and experimentations on time.

### Reinforcement Learning
This contains files used in reinforcement learning projects.

There are two projects.
1. Connect 4 bot thats trained via deep Q learning in an incremental/online fashion.
2. Tic-Tac-Three uses value iteration to play a variation of tic-tac-toe. \


#### Connect 4
Still a work in progress but the main functionality is there and working. This project will develop a bot to play connect 4 along with a GUI of the game that utilises the bot so I can play against it.

##### Game.py
Contains the class that simulates the connect 4 game used for the GUI and to train an agent.

##### train.ipynb
Read the game simulation and trains the bot that plays it. The end result model is saved via the 'model' directory.

##### GUI.py
Reads the game simulation and uses it to produce an interactive GUI to play the game. End goal is to have the bot interact with this GUI also.



#### Tic Tac Three
This was apart of a group project but all code here is work developed by myself. The files below use value iteration to produce a dictionary of state-value pairs in order to play a variety of tic-tac-toe we imagined and evaluates the gameplay between the two.

##### Tic tac three - actual.py
Building a tic tac toe variety and teaching an agent how to play with value iteration.

##### Generate Matrix Corr plot thing.R
Expansion on Tic tac Three. Using R to generate some nice plots from the output of gameplay simualtion.

### Individual
Smaller projects that can each be summarised in a single file.

##### prime factorisation.py + fizz buzz.py
Standard coding problems and my approach to solving them

##### shakespeare-Bryce-HW-01.rmd
R markdown piece evaluating how good an LCG is at generating 'random' numbers

##### fisher test.R
applying fishers method to combine and evaluate multiple p values

##### cancsurv.R
30 min go at survival modelling with small data. not very good
