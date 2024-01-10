import numpy as np
import copy

class conny4:
    
    def __init__(self, start_board = np.zeros((6,7))):
        self.board = copy.deepcopy(start_board)
        self.player = self.player()

        if np.sum(self.board) == 1:
            self.player.player = 'Y'
        elif np.sum(self.board) == 0:
            self.player.player = 'R'
        else:
            self.board = np.zeros((6,7))
    
    class player:
        def __init__(self):
            self.player = None
            self.player_swap = {'R':'Y', 'Y':'R'}
            self.player_score = {'R':1, 'Y':-1}
            self.player_name = {'R':'Red', 'Y':'Yellow'}
            
    def legal(self):
        leg = []
        if not self.game_end()[0]:
            for i in range(7):
                if self.board[0,i] == 0:
                    leg.append(i)
        return(leg)
        
    def turn(self, pos):
        if pos not in self.legal():
            pass
        else:
            self.board[sum(np.where(self.board[:,pos] == 0, 1 ,0)) - 1,pos] = self.player.player_score[self.player.player]
            if not self.game_end()[0]:
                self.player.player = self.player.player_swap[self.player.player]
    
    def game_end(self):
        if self.score_update() == 4:
            return(True,self.player.player_score[self.player.player])
        elif sum(sum(np.where(self.board == 0, 1,0))) == 0:
            return(True,0)
        else:
            return(False,)
    
    def score_update(self):
        for i in range(3):
            for j in range(4):
                x4 = self.board[i:4+i,j:4+j]
                hors = [abs(sum(x4[:,k])) for k in range(4)]
                vers = [abs(sum(x4[k,:])) for k in range(4)]
                diag = [abs(np.trace(x4)),abs(np.trace(np.flip(x4,0)))]
                score = max(hors+vers+diag)
                if score == 4:
                    return(score)
        return(score)
