import numpy as np
import Basic_Operation
from random import randrange

class pruning:
    def __init__(self, Nx, max_eva, man_value, king_value, CHECKERS):
        self.Nx = Nx
        self.max_eva = max_eva
        self.man_value = man_value
        self.king_value = king_value
        self.CHECKERS = CHECKERS

    def EVALUATION(self, side, list_of_checkers, list_of_scores):
        #LIST_CHECKER(list_of_checkers, man_r, man_w, king_r, king_w)
        total_r = len(np.argwhere(np.array(list_of_checkers)<0)) # counts all negative values
        total_w = len(np.argwhere(np.array(list_of_checkers)>0)) # counts all positive values
        (man_jump, king_jump, man_walk, king_walk, taken_by_man, taken_by_king) = self.CHECKERS.AVAILABLE_MOVE(side, list_of_checkers)
        available_move = man_jump + king_jump + man_walk + king_walk
        game_score = np.array(list_of_checkers).sum() + np.array(list_of_scores).sum()
        evaluation = game_score

        # if either chips runs out
        if total_r == 0 or total_w == 0:
            if game_score > 0:              # White wins
                evaluation = self.max_eva;
            elif  game_score < 0:
                evaluation = -self.max_eva; # Red wins
            else:
                evaluation = 0              # Draw
        # if moves runs out
        elif available_move == []:
            if game_score > 0:             # WHITE wins if RED has no more moves and current score is in its favor
                evaluation = self.max_eva
            elif game_score < 0:
                evaluation = -self.max_eva
            else:
                evaluation = 0 # Draw
        else:
            evaluation = game_score
 
        if abs(evaluation) != self.max_eva:
            evaluation = game_score
        return evaluation

    def ONE_MOVE(self, side, list_of_checkers, list_of_scores):
        (man_jump, king_jump, man_walk, king_walk, taken_by_man, taken_by_king ) = self.CHECKERS.AVAILABLE_MOVE(side, list_of_checkers)
        checkers_tree = []
        scores_tree = []
        # Jump / Capture
        if man_jump+king_jump != []:

            man_jump_tree = []
            man_jump_tree.append((man_jump.copy(),list_of_checkers.copy(), list_of_scores.copy()))

            while man_jump_tree != []:
                man_jump = man_jump_tree[-1][0].copy()
                temp = man_jump_tree[-1][1].copy()
                score_temp = man_jump_tree[-1][2].copy()
                del man_jump_tree[-1]
                for (start, stop) in man_jump:
                    virtual_checkers = temp.copy()
                    virtual_scores = score_temp.copy()
                    taken = (start+stop)//2
                    virtual_checkers[start] = 0 # empty the start position
                    virtual_checkers[taken] = 0 # empty the taken position
                    if side == 1: # RED's turn
                        virtual_checkers[stop] = -self.man_value
                        virtual_scores[stop] += self.CHECKERS.COMPUTE(-self.man_value, self.man_value, stop)
                        man_jump_prime = []
                        taken_by_man = []
                        self.CHECKERS.MAN_JUMP_RED(stop, virtual_checkers, man_jump_prime, taken_by_man)
                        if man_jump_prime == []:
                            if stop//self.Nx == 0:
                                virtual_checkers[stop] = -self.king_value
                            checkers_tree.append(virtual_checkers.copy())
                            scores_tree.append(virtual_scores.copy())
                        else: # multi jump
                            man_jump_tree.append((man_jump_prime.copy(),virtual_checkers.copy(),virtual_scores.copy()))

                    else: #WHITE's turn
                        virtual_checkers[stop] = self.man_value
                        virtual_scores[stop] += self.CHECKERS.COMPUTE(self.man_value, -self.man_value, stop)
                        man_jump_prime = []
                        taken_by_man = []
                        self.CHECKERS.MAN_JUMP_WHITE(stop, virtual_checkers, man_jump_prime, taken_by_man)
                        if man_jump_prime == []:
                            if stop//self.Nx == self.Nx-1:
                                virtual_checkers[stop] = self.king_value
                            checkers_tree.append(virtual_checkers.copy())
                            scores_tree.append(virtual_scores.copy())
                        else:
                            man_jump_tree.append((man_jump_prime.copy(),virtual_checkers.copy(), virtual_scores.copy()))


            king_jump_tree = []
            king_jump_tree.append((king_jump.copy(), list_of_checkers.copy(), list_of_scores.copy()))

            while king_jump_tree != []:
                king_jump = king_jump_tree[-1][0].copy()
                temp = king_jump_tree[-1][1].copy()
                score_temp = king_jump_tree[-1][2].copy()
                del king_jump_tree[-1]
                for (start, stop) in king_jump:
                    virtual_checkers = temp.copy()
                    virtual_scores =score_temp.copy()
                    taken = (start+stop)//2
                    virtual_checkers[start] = 0
                    virtual_checkers[taken] = 0
                    if side == 1:
                        virtual_checkers[stop] = -self.king_value
                        virtual_scores[stop] += self.CHECKERS.COMPUTE_KING(-self.man_value, self.man_value, stop)
                        king_jump_prime = []
                        taken_by_king = []
                        self.CHECKERS.KING_JUMP_RED(stop, virtual_checkers, king_jump_prime, taken_by_king)
                        if king_jump_prime == []:
                            checkers_tree.append(virtual_checkers.copy())
                            scores_tree.append(virtual_scores.copy())
                        else:
                            king_jump_tree.append((king_jump_prime.copy(), virtual_checkers.copy(), virtual_scores.copy()))
                    else:
                        virtual_checkers[stop] = self.king_value
                        virtual_scores[stop] += self.CHECKERS.COMPUTE_KING( self.man_value, -self.man_value, stop)
                        king_jump_prime = []
                        taken_by_king = []
                        self.CHECKERS.KING_JUMP_WHITE(stop, virtual_checkers, king_jump_prime, taken_by_king)
                        if king_jump_prime == []:
                            checkers_tree.append(virtual_checkers.copy())
                            scores_tree.append(virtual_scores.copy())
                        else:
                            king_jump_tree.append((king_jump_prime.copy(), virtual_checkers.copy(), virtual_scores.copy()))
        # Walk (no score update)
        elif man_walk+king_walk != []:
            for (start, stop) in man_walk:
                virtual_checkers = list_of_checkers.copy()
                virtual_scores = list_of_scores.copy()
                virtual_checkers[start] = 0
                if side == 1:
                    if stop//self.Nx == 0:
                        virtual_checkers[stop] = -self.king_value
                    else:
                        virtual_checkers[stop] = -self.man_value
                else:
                    if stop//self.Nx == self.Nx-1:
                        virtual_checkers[stop] = self.king_value
                    else:
                        virtual_checkers[stop] = self.man_value
                checkers_tree.append(virtual_checkers.copy())
                scores_tree.append(virtual_scores.copy())

            for (start, stop) in king_walk:
                virtual_checkers = list_of_checkers.copy()
                virtual_scores = list_of_scores.copy()
                virtual_checkers[start] = 0
                if side == 1:
                    virtual_checkers[stop] = -self.king_value
                else:
                    virtual_checkers[stop] = self.king_value
                checkers_tree.append(virtual_checkers.copy())
                scores_tree.append(virtual_scores.copy())
        else:
            checkers_tree.append(list_of_checkers)
            scores_tree.append(list_of_scores)
        return (checkers_tree, scores_tree)

    def BUILD_TREE(self, side, list_of_checkers, list_of_scores, depth):
        temp, temp_scores = self.ONE_MOVE(side,list_of_checkers, list_of_scores)
        if depth != 1:
            A = []
            for i in temp:
                A.append(BUILD_TREE(-side, i, depth-1))
            return A.copy()
        elif depth == 1:
            point = np.zeros((len(temp)))
            for index,(element, score_item) in enumerate(zip(temp, temp_scores)):
                point[index] = self.EVALUATION(side, element, score_item)
            return point

    def MIN_MAX_SEARCH(self, side, list_of_checkers, depth):
        temp = self.ONE_MOVE(side,list_of_checkers)
        point = np.zeros((len(temp)))
        if depth > 1:
            for index, element in enumerate(temp):
                point[index] = self.MIN_MAX_SEARCH(-side, element, depth-1)
            if side == 1:
                return point.min()
            else:
                return point.max()
        elif depth == 1:
            #print(side)
            for index,element in enumerate(temp):
                point[index] = self.EVALUATION(side, element)
            if side == 1:
                return point.min()
            else:
                return point.max()

    def FIND_BEST_MOVE_MIN_MAX(self, side, list_of_checkers, depth):
        temp = self.ONE_MOVE(side, list_of_checkers)
        point = np.zeros((len(temp)))
        for index,element in enumerate(temp):
            if depth > 1:
                point[index] = self.MIN_MAX_SEARCH(-side, element, depth-1)
            elif depth == 1:
                point[index] = self.EVALUATION(side, element)
        choice = np.random.choice(np.argwhere(point==point.max()).reshape(-1))
        return (temp[choice].copy(), point.max() )

    def ALPHA_BETA_SEARCH(self, side, list_of_checkers, list_of_scores, depth, alpha, beta):
        if depth > 0:
            temp, temp_scores = self.ONE_MOVE(side, list_of_checkers, list_of_scores)
            if side == 1: #minimum node, evaluate beta
                for (i,j) in zip(temp, temp_scores):
                    if depth != 1:
                        beta = min(beta, self.ALPHA_BETA_SEARCH(-side, i, j, depth-1, alpha, beta))
                    else:
                        beta = min(beta, self.ALPHA_BETA_SEARCH(side, i, j, depth-1, alpha, beta))
                    if beta <= alpha:
                        break
                return beta
            else:
                for (i, j) in zip(temp, temp_scores):
                    if depth != 1:
                        alpha = max(alpha, self.ALPHA_BETA_SEARCH(-side, i, j, depth-1, alpha, beta))
                    else:
                        alpha = max(alpha, self.ALPHA_BETA_SEARCH(side, i, j, depth-1, alpha, beta))
                    if beta <= alpha:
                        break
                return alpha
        elif depth == 0:
            point = self.EVALUATION(side, list_of_checkers, list_of_scores)
            return point

    def FIND_BEST_MOVE_ALPHA_BETA(self, side, list_of_checkers, list_of_scores, depth, alpha, beta):
        temp, temp_scores = self.ONE_MOVE(side, list_of_checkers, list_of_scores)  # all possible moves
        # print('\t len(temp) = %d.' %(len(temp)) )
        # print('\t len(temp_scores) = %d.' % (len(temp_scores)))
        point = np.zeros((len(temp)))
        for index, (chips_item, score_item) in enumerate(zip(temp, temp_scores)):
            point[index] = self.ALPHA_BETA_SEARCH(-side, chips_item, score_item, depth-1, alpha, beta)

        choice = np.random.choice(np.argwhere(point==point.max()).reshape(-1))
        return (temp[choice].copy(), point.max(), temp_scores[choice].copy() )

    def FIND_RANDOM_MOVE(self, side, list_of_checkers, list_of_scores):
        temp, temp_scores = self.ONE_MOVE(side, list_of_checkers, list_of_scores)
        choice =  randrange(len(temp))
        return (temp[choice].copy(), temp_scores[choice].copy() )

    def REVERSE_COLOR_AND_BOARD(self, list_of_checkers):  # designed for red if alpha-beta prouning need to be applied
        reverse = []
        for i in range(0, self.Nx**2):
            a = list_of_checkers[63-i]
            if a!=0:
                reverse.append(-a)
            else:
                reverse.append(0)
        return reverse.copy()
