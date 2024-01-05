
# %%    Libraries and useful functs

import numpy as np
import copy
import random
import sys
import os
import pickle
from timeit import default_timer as timer
from itertools import combinations
import pandas as pd

# Disable
def blockPrint():
    sys.__stdout__ = sys.stdout
    sys.stdout = open(os.devnull, 'w')

# Restore
def enablePrint():
    sys.stdout = sys.__stdout__


#%%

# reward and state_values are in perspective of X Player, simply reversing this (similar to min max) optimises 0


class Tic_Tac_Steve_Reinforce:
    
    #always start with a 3 x 3 board
    def __init__(self, play_start ='X', start_board = np.zeros((3,3,3)), last_move = None, st_va = {}):

        self.game_board = copy.deepcopy(start_board)
        self.player_swap = {'X':'O', 'O':'X'}
        self.player_prev = self.player_swap[play_start]
        self.play_dict = {'X':1, 'O':-1}
        self.score_keeper = [0]*3
        self.unplayable_boards = [0]*3
        self.final_board = None
        self.last_move = last_move
        self.story = [[self.player_prev, self.game_board.copy(), self.last_move]]
        self.reward = None
        self.playable_moves = None
        self.state_values = {} if st_va == None else copy.deepcopy(st_va)
        
        self.update_score()
        self.game_winner_check()
        self.playable_moves_update()
        self.game_print()
    
    
    def game_winner_check(self):
        self.game_finished = False
        if 3 in self.score_keeper or -3 in self.score_keeper:
            self.game_finished = True
            print(self.player_prev +' wins!')
            self.reward = self.play_dict[self.player_prev]*10
            self.update_state_values()
        elif sum(self.unplayable_boards) == self.game_board.shape[0]:
            if abs(self.score_keeper[self.final_board] == 5):
                self.game_finished = True
                print('This Game is a draw!')
                self.reward = 0
                self.update_state_values()
            
            
    
    def update_points_single(self,x):
        for i in range(3):
            self.score_keeper[x] = max(abs(self.score_keeper[x]), abs(sum(self.game_board[x][i][:])))
            #count scores for rows, updates if greater than current
            self.score_keeper[x] = max(abs(self.score_keeper[x]), abs(sum(self.game_board[x][:,i])))
            # count scores for column, update if greater than current
        #print(self.score_keeper)
        self.score_keeper[x] = max(abs(self.score_keeper[x]), abs(sum([self.game_board[x][0,0],self.game_board[x][1,1],self.game_board[x][2,2]])))
        # updates the diagonal 1 score
        self.score_keeper[x] = max(abs(self.score_keeper[x]), abs(sum([self.game_board[x][0,2],self.game_board[x][1,1],self.game_board[x][2,0]])))
        # updates the diagonal 1 score
        
        if 0 not in self.game_board[x]: 
          self.score_keeper[x] = 5
          
          
    def update_score(self):
        for k in range(3):
            self.update_points_single(k)
            if abs(self.score_keeper[k]) >= 3:
                self.unplayable_boards[k] = 1
        if sum(self.unplayable_boards) == self.game_board.shape[0] -1:
            self.final_board = self.unplayable_boards.index(0)
    
    
    def game_print(self):
        print(self.game_board)
        print('PLayable Moves now are:  ', self.playable_moves)
        print('unplayable boards: ',self.unplayable_boards)
        print('score_keep: ',self.score_keeper)
        print('last move was: ',self.last_move, '   You can use boards : ', self.sent_to(), ' next')
        
    
    def player_turn(self, posi = None):
        if self.player_prev in ['O','X'] and posi in self.playable_moves:
            self.player_prev = self.player_swap[self.player_prev]
            self.game_board[posi[0],posi[2],posi[1]] = self.play_dict[self.player_prev]
            self.last_move = posi
            self.story.append([self.player_prev, copy.deepcopy(self.game_board), self.last_move])
            
            self.update_score()
            self.playable_moves_update()
            self.game_winner_check()
            self.game_print()
        else:
            print('not allowed this move')


    def state_return(self, k = 0):
    # reset reward incase someone won
        self.reward = None
        # reset player to relevant entry in story
        self.player_prev = self.story[k][0]
        # reset gameboard to relevenat entry in story
        self.game_board = copy.deepcopy(self.story[k][1])
        # reset last move player
        self.last_move = self.story[k][2]
        # reset the story to remove states that occur after Kth turn
        self.story = self.story[:k+1]
        self.score_keeper = [0]*3
        self.unplayable_boards = [0]*3
        # update the points again to match new state
        self.update_score()
        # potentially current state is also winning so check that off
        self.game_winner_check()
        #update list of playable moves
        self.playable_moves_update()
        # print where we are
        print(self.game_board)
        print(' last play was:   ', self.player_prev)
    
    
    def sent_to(self):
        if self.last_move == None:
            return([0,1,2])
        elif self.unplayable_boards[self.last_move[1]] == 1:
            return([0,1,2])
        elif self.unplayable_boards[self.last_move[1]] == 0:
            return([self.last_move[1]])
    
        
    def playable_moves_update(self):
        self.playable_moves = []
        if sum(self.unplayable_boards) == self.game_board.shape[0]:
            self.playable_moves = [None]
        else:
            for x in range(len(self.unplayable_boards)):
                if self.unplayable_boards[x] == 0 and x in self.sent_to() :
                    for i in range(3):
                        for j in range(3):
                            if self.game_board[x,i,j] == 0:
                                self.playable_moves.append([x,j,i])
    
    def choose_action(self, rand_rate = 0.3):
        
        blockPrint()
        if np.random.uniform(0, 1) <= rand_rate:
            # take random action
            action = self.playable_moves[np.random.choice(len(self.playable_moves))]
            
        else:
            value_max = -500
            # set initial value for score lookup
            Moves_list = copy.deepcopy(self.playable_moves)
            random.shuffle(Moves_list)
            for move in Moves_list:
            # randomise the order moves are checked so that if multiple have same value (low iteration number) it does not always choose the same one and get stuck
                self.player_turn(posi = move)
                # makes a move
                if self.game_finished:
                    value = self.reward*self.play_dict[self.player_prev]
                    self.state_values[str(self.game_board)] = copy.deepcopy(self.reward)
                # if the move finishes the game, add the reward value to the states array
                elif self.state_values.get(str(self.game_board)) == None:
                    value = 0
                # if the value for the state moved into is empty then set it to 0
                else:
                    value = self.state_values.get(str(self.game_board))*self.play_dict[self.player_prev]
                # collects value for the move based on the values in the array
                # the states_values are as if the player is X, so add in a player multiplier (1 or -1) to maximise player_0 choice also
                # have to use str(gameboard) to retrieve value as each one should be unique and cant pass an array through to a dict
                self.state_return( k = (len(self.story) - 2))
                # return state to the state before move was taken so comparison can be made with the other moves available
                # have to do len(story -2, as -1 for previous state and -1 another because arrays initialise at arr[0] but will have len 1)
                if value >= value_max:
                    value_max = value
                    action = move
        enablePrint()
        print('next chosen move is:  ', action)
        return action
    
    def update_state_values(self, learning_rate = 0.3, decay = 0.9):
        plugged_reward = copy.deepcopy(self.reward)
        for state in reversed(np.array(self.story)[:,1][:-1]):
            # update all states visited (apart from the end state which will have an associated reward)
            if self.state_values.get(str(state)) == None:
                self.state_values[str(state)] = 0
            self.state_values[str(state)] += (learning_rate * ((decay * plugged_reward) - self.state_values[str(state)]))
            plugged_reward = copy.deepcopy(self.state_values[str(state)])
    
    def play_game(self, rounds = 10, rando_rate = 0.3, reset = True):
        for i in range(rounds):
            while self.game_finished != True:
                self.player_turn(posi = self.choose_action(rand_rate = rando_rate))
                # take turns until a win is given
                # upon a win the game should detect this, give updates and update the state_value dict
                # in which case we wish to reset everything (execpt the state_value dict) and iterate again
            if rounds != 1:
                self.state_return()
            elif reset:
                self.state_return()
            # go back to start of game once it has finished and run again with next i



# %% tic tac game against

class Tic_Tac_Steve_Against:
    
    #always start with a 3 x 3 board
    def __init__(self, play_start ='X', start_board = np.zeros((3,3,3)), last_move = None, st_va = {}):

        self.game_board = copy.deepcopy(start_board)
        self.player_swap = {'X':'O', 'O':'X'}
        self.player_prev = self.player_swap[play_start]
        self.play_dict = {'X':1, 'O':-1}
        self.score_keeper = [0]*3
        self.unplayable_boards = [0]*3
        self.final_board = None
        self.last_move = last_move
        self.story = [[self.player_prev, self.game_board.copy(), self.last_move]]
        self.win_log =[]
        self.reward = None
        self.playable_moves = None
        self.state_values = {} if st_va == None else copy.deepcopy(st_va)
        
        self.update_score()
        self.game_winner_check()
        self.playable_moves_update()
        #self.game_print()
    
    
    def game_winner_check(self):
        self.game_finished = False
        if 3 in self.score_keeper or -3 in self.score_keeper:
            self.game_finished = True
            print(self.player_prev +' wins!')
            self.reward = self.play_dict[self.player_prev]*10
            self.win_log.append(self.play_dict[self.player_prev])
            #self.update_state_values()
        elif sum(self.unplayable_boards) == self.game_board.shape[0]:
            if abs(self.score_keeper[self.final_board] == 5):
                self.game_finished = True
                print('This Game is a draw!')
                self.reward = 0
                self.win_log.append(0)
                #self.update_state_values()
            
            
    
    def update_points_single(self,x):
        for i in range(3):
            self.score_keeper[x] = max(abs(self.score_keeper[x]), abs(sum(self.game_board[x][i][:])))
            #count scores for rows, updates if greater than current
            self.score_keeper[x] = max(abs(self.score_keeper[x]), abs(sum(self.game_board[x][:,i])))
            # count scores for column, update if greater than current
        #print(self.score_keeper)
        self.score_keeper[x] = max(abs(self.score_keeper[x]), abs(sum([self.game_board[x][0,0],self.game_board[x][1,1],self.game_board[x][2,2]])))
        # updates the diagonal 1 score
        self.score_keeper[x] = max(abs(self.score_keeper[x]), abs(sum([self.game_board[x][0,2],self.game_board[x][1,1],self.game_board[x][2,0]])))
        # updates the diagonal 1 score
        
        if 0 not in self.game_board[x]: 
          self.score_keeper[x] = 5
          
          
    def update_score(self):
        for k in range(3):
            self.update_points_single(k)
            if abs(self.score_keeper[k]) >= 3:
                self.unplayable_boards[k] = 1
        if sum(self.unplayable_boards) == self.game_board.shape[0] -1:
            self.final_board = self.unplayable_boards.index(0)
    
    
    def game_print(self):
        print(self.game_board)
        print('PLayable Moves now are:  ', self.playable_moves)
        print('unplayable boards: ',self.unplayable_boards)
        print('score_keep: ',self.score_keeper)
        print('last move was: ',self.last_move, '   You can use boards : ', self.sent_to(), ' next')
        
    
    def player_turn(self, posi = None):
        if self.player_prev in ['O','X'] and posi in self.playable_moves:
            self.player_prev = self.player_swap[self.player_prev]
            self.game_board[posi[0],posi[2],posi[1]] = self.play_dict[self.player_prev]
            self.last_move = posi
            self.story.append([self.player_prev, copy.deepcopy(self.game_board), self.last_move])
            
            self.update_score()
            self.playable_moves_update()
            self.game_winner_check()
            #self.game_print()
        else:
            print('not allowed this move')


    def state_return(self, k = 0):
    # reset reward incase someone won
        self.reward = None
        # reset player to relevant entry in story
        self.player_prev = self.story[k][0]
        # reset gameboard to relevenat entry in story
        self.game_board = copy.deepcopy(self.story[k][1])
        # reset last move player
        self.last_move = self.story[k][2]
        # reset the story to remove states that occur after Kth turn
        self.story = self.story[:k+1]
        self.score_keeper = [0]*3
        self.unplayable_boards = [0]*3
        # update the points again to match new state
        self.update_score()
        # potentially current state is also winning so check that off
        self.game_winner_check()
        #update list of playable moves
        self.playable_moves_update()
        # print where we are
        #print(self.game_board)
        #print(' last play was:   ', self.player_prev)
    
    
    def sent_to(self):
        if self.last_move == None:
            return([0,1,2])
        elif self.unplayable_boards[self.last_move[1]] == 1:
            return([0,1,2])
        elif self.unplayable_boards[self.last_move[1]] == 0:
            return([self.last_move[1]])
    
        
    def playable_moves_update(self):
        self.playable_moves = []
        if sum(self.unplayable_boards) == self.game_board.shape[0]:
            self.playable_moves = [None]
        else:
            for x in range(len(self.unplayable_boards)):
                if self.unplayable_boards[x] == 0 and x in self.sent_to() :
                    for i in range(3):
                        for j in range(3):
                            if self.game_board[x,i,j] == 0:
                                self.playable_moves.append([x,j,i])
    
    def choose_action(self, rand_rate = 0.3):
        
        blockPrint()
        if np.random.uniform(0, 1) <= rand_rate:
            # take random action
            action = self.playable_moves[np.random.choice(len(self.playable_moves))]
            
        else:
            value_max = -500
            # set initial value for score lookup
            Moves_list = copy.deepcopy(self.playable_moves)
            random.shuffle(Moves_list)
            for move in Moves_list:
            # randomise the order moves are checked so that if multiple have same value (low iteration number) it does not always choose the same one and get stuck
                self.player_turn(posi = move)
                # makes a move
                if self.game_finished:
                    value = self.reward*self.play_dict[self.player_prev]
                    self.state_values[str(self.game_board)] = copy.deepcopy(self.reward)
                    self.win_log = self.win_log[:-1]
                # if the move finishes the game, add the reward value to the states array
                elif self.state_values.get(str(self.game_board)) == None:
                    value = 0
                # if the value for the state moved into is empty then set it to 0
                else:
                    value = self.state_values.get(str(self.game_board))*self.play_dict[self.player_prev]
                # collects value for the move based on the values in the array
                # the states_values are as if the player is X, so add in a player multiplier (1 or -1) to maximise player_0 choice also
                # have to use str(gameboard) to retrieve value as each one should be unique and cant pass an array through to a dict
                self.state_return( k = (len(self.story) - 2))
                # return state to the state before move was taken so comparison can be made with the other moves available
                # have to do len(story -2, as -1 for previous state and -1 another because arrays initialise at arr[0] but will have len 1)
                if value >= value_max:
                    value_max = value
                    action = move
        enablePrint()
        #print('next chosen move is:  ', action)
        return action
    
    def update_state_values(self, learning_rate = 0.3, decay = 0.9):
        plugged_reward = copy.deepcopy(self.reward)
        for state in reversed(np.array(self.story)[:,1][:-1]):
            # update all states visited (apart from the end state which will have an associated reward)
            if self.state_values.get(str(state)) == None:
                self.state_values[str(state)] = 0
            self.state_values[str(state)] += (learning_rate * ((decay * plugged_reward) - self.state_values[str(state)]))
            plugged_reward = copy.deepcopy(self.state_values[str(state)])
    
    def play_game(self, rounds = 10, rando_rate = 0.3, reset = True):
        for i in range(rounds):
            while self.game_finished != True:
                self.player_turn(posi = self.choose_action(rand_rate = rando_rate))
                # take turns until a win is given
                # upon a win the game should detect this, give updates and update the state_value dict
                # in which case we wish to reset everything (execpt the state_value dict) and iterate again
            if rounds != 1:
                self.state_return()
            elif reset:
                self.state_return()
            # go back to start of game once it has finished and run again with next i

#%% testing and running reinforcement class


with open('State_values - 0 draw - 60000 rounds.pickle', 'rb') as handle:
    state_values_dict_test = pickle.load(handle)

game_Q = Tic_Tac_Steve_Reinforce()

rando = [0.95, 0.75, 0.5]

start = timer()
for ra in rando:
    game_Q.play_game(rounds = 1000, rando_rate = ra)

#game_Q.play_game(rounds = 10000, rando_rate=0.8)
#game_Q.play_game(rounds = 10000, rando_rate=0.3)
#game_Q.play_game(rounds = 10000, rando_rate=0.1)

end = timer()

time_taken = end - start
print(time_taken/60)
# 3 minutes for 3K round *6

state_values_dict = copy.deepcopy(game_Q.state_values)

with open('State_values - 0 draw - 3000 rounds - take 3.pickle', 'wb') as handle:
    pickle.dump(state_values_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)



# %% training multiples

rounds_array = [333333, 200000, 100000, 33333, 20000, 10000]

rando = [0.95, 0.75, 0.5]

start = timer()

for ro in rounds_array:
    game_Run = Tic_Tac_Steve_Reinforce(st_va = {})
    # reset class for each iter so state_value array is empty at start
    for ra in rando:
        game_Run.play_game(rounds = ro, rando_rate = ra)
    states_vals_dic = copy.deepcopy(game_Run.state_values)
    file_name = 'State_values - 0 draw - '+str(ro * 3)+' rounds - take 5.pickle'
    with open(file_name, 'wb') as handle:
        pickle.dump(states_vals_dic, handle, protocol=pickle.HIGHEST_PROTOCOL)

end = timer()

time_taken = end - start
print('minutes taken to run: ', time_taken/60)

#%% Play against it

with open('State_values - 0 draw - 400000 rounds - take 4.pickle', 'rb') as handle:
    state_values_dict_big = pickle.load(handle)

game_1 = Tic_Tac_Steve_Reinforce(st_va=state_values_dict_big)
#game_1.playable_moves show playable moves

game_1.player_turn(posi = [0,0,0])
# this is a manual turn, input array from playable moves list will auto swap player turn after one has been taken
# [X,Y,Z] X is the board number 0-2, Y is the column number 0-2, Z is the row 0-2

game_1.player_turn(posi = game_1.choose_action(rand_rate=0))
# this will make the next move that the ai wants
# rand_rate = 0, to make sure there is no exploration 

game_1.player_turn(posi = [0,1,1])
#### example game against AI, AI goes first


game_1.player_turn(posi = game_1.choose_action(rand_rate=0))


game_1.player_turn(posi = [2,1,1])

game_1.player_turn(posi = game_1.choose_action(rand_rate=0))

game_1.player_turn(posi = [1,0,2])

game_1.player_turn(posi = game_1.choose_action(rand_rate=0))

game_1.player_turn(posi = [2,0,2])

game_1.player_turn(posi = game_1.choose_action(rand_rate=0))

game_1.player_turn(posi = [2,2,0])

game_1.player_turn(posi = game_1.choose_action(rand_rate=0))

game_1.player_turn(posi = [1,1,2])

#%%  playing against itself

start = timer()

def single_game(game_1_initialised = None, game_2_initialised = None):

    # let player 1 decide a random move and play it on both
    move = game_1_initialised.choose_action(rand_rate=1)
    game_1_initialised.player_turn(move)
    game_2_initialised.player_turn(move)
    
    # let player 2 decide a random move and play it on both
    move = game_2_initialised.choose_action(rand_rate=1)
    game_1_initialised.player_turn(move)
    game_2_initialised.player_turn(move)
    
    # let player 1 decide a random move and play it on both
    move = game_1_initialised.choose_action(rand_rate=1)
    game_1_initialised.player_turn(move)
    game_2_initialised.player_turn(move)
    
    # will stop looping if the game has reached an end
    while game_1_initialised.game_finished != True:
        
        # let player 1 decide a move using its given states_values dictionary and randomness
        # play it on both game boards
        move = game_2_initialised.choose_action(rand_rate = 0)
        game_1_initialised.player_turn(move)
        game_2_initialised.player_turn(move)
        
        #if the last move did not result in a finish, then let player 2 take a turn, then run while case again
        if game_2_initialised.game_finished != True:
            
            # let player 2 decide a move using its givens states_values dictionary and randomness
            # play it on both game boards
            move = game_1_initialised.choose_action(rand_rate = 0)
            game_1_initialised.player_turn(move)
            game_2_initialised.player_turn(move)
    
    game_1_initialised.state_return()
    game_2_initialised.state_return()
    


rounds_array = [333333, 200000, 100000, 33333, 20000, 10000]
rounds_array.sum()

playable = {'random':{}}
for ro in rounds_array:
    file_name = 'State_values - 0 draw - '+str(int(ro*3))+' rounds - take 5.pickle'
    var_name = str(int(ro*3)) +'_rounds'
    with open(file_name, 'rb') as handle:
        playable[var_name] = pickle.load(handle)

playable_combinations = list(combinations(playable.keys(), 2))

dic_size = []
for i in playable.values():
    dic_size.append(len(i))
    
size_df = pd.DataFrame({'Rounds': playable.keys(),
                        'State_size': dic_size})

#size_df.to_csv(r'Size by rounds.csv')

Game_Winners_df = pd.DataFrame(columns= ['First Player', 'Second Player', 'Winner'])

for comb in playable_combinations:
    
    count = 0
    game_player_1 = Tic_Tac_Steve_Against(st_va=playable[comb[0]])
    game_player_2 = Tic_Tac_Steve_Against(st_va=playable[comb[1]])
    
    while count < 500:
        single_game(game_1_initialised=game_player_1, game_2_initialised=game_player_2)
        count += 1
    
    Game_Winners_df = pd.concat([Game_Winners_df,
                          pd.DataFrame({
                              'First Player': [str(comb[0])]*count,
                              'Second Player': [str(comb[1])]*count,
                              'Winner': game_player_1.win_log})])
    
    count = 0
    game_player_1 = Tic_Tac_Steve_Against(st_va=playable[comb[1]])
    game_player_2 = Tic_Tac_Steve_Against(st_va=playable[comb[0]])
    
    while count < 500:
        single_game(game_1_initialised=game_player_1, game_2_initialised=game_player_2)
        count += 1
    
    Game_Winners_df = pd.concat([Game_Winners_df,
                          pd.DataFrame({
                              'First Player': [str(comb[1])]*count,
                              'Second Player': [str(comb[0])]*count,
                              'Winner': game_player_1.win_log})])
end = timer()

time_taken = end - start
print('minutes taken to run: ', time_taken/60)

Game_Winners_df.to_csv(r'Ai va Ai - rounds - results.csv')


# %% combine dicts to rule them all

Dict_to_rule_them_all = {}

for i in reversed(playable.values()):
    Dict_to_rule_them_all = {**Dict_to_rule_them_all, **i}

file_name = 'State_values - 0 draw - to rule them all.pickle'
with open(file_name, 'wb') as handle:
    pickle.dump(Dict_to_rule_them_all, handle, protocol=pickle.HIGHEST_PROTOCOL)



# %% against minimax

win = Tic_Tac_Steve_Reinforce(st_va=Dict_to_rule_them_all)

win.player_turn(posi = win.choose_action(rand_rate=0))
win.player_turn(posi= [2,2,0])
win.player_turn(posi = win.choose_action(rand_rate=0))
win.player_turn(posi= [1,1,1])
win.player_turn(posi = win.choose_action(rand_rate=0))
win.player_turn(posi= [0,1,1])
win.player_turn(posi = win.choose_action(rand_rate=0))
win.player_turn(posi= [0,2,1])
win.player_turn(posi = win.choose_action(rand_rate=0))
win.player_turn(posi= [2,0,2])
win.player_turn(posi = win.choose_action(rand_rate=0))
win.player_turn(posi= [2,1,1])

win.state_return()

