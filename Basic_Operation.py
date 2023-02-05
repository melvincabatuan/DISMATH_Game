#!/usr/bin/env python
# coding: utf-8

# In[1]:
class Checkers_Basic:
    def __init__(self, Nx, man_value, king_value, step_fr_r, step_fl_r, step_br_r, step_bl_r, step_fr_w, step_fl_w, step_br_w, step_bl_w, man_r, man_w, king_r, king_w, operations):
        self.Nx = Nx
        self.man_value = man_value
        self.king_value = king_value
        self.step_fr_r = step_fr_r
        self.step_fl_r = step_fl_r
        self.step_br_r = step_br_r
        self.step_bl_r = step_bl_r
        self.step_fr_w = step_fr_w
        self.step_fl_w = step_fl_w
        self.step_br_w = step_br_w
        self.step_bl_w = step_bl_w
        self.man_r = man_r
        self.man_w = man_w
        self.king_r = king_r
        self.king_w = king_w
        self.operations = operations

    def CHECKER_LIST(self, list_of_checkers):
        for element in self.man_r:
            list_of_checkers[element] = -self.man_value
        for element in self.man_w:
            list_of_checkers[element] = self.man_value
        for element in self.king_r:
            list_of_checkers[element] = -self.king_value
        for element in self.king_w:
            list_of_checkers[element] = self.king_value
        return(list_of_checkers)

    def LIST_CHECKER(self, list_of_checkers):
        for index, element in enumerate(list_of_checkers):
            if element == -self.man_value:
                self.man_r.append(index)
            elif element == self.man_value:
                self.man_w.append(index)
            elif element == -self.king_value:
                self.king_r.append(index)
            elif element == self.king_value:
                self.king_w.append(index)
        return(self.man_r, self.man_w, self.king_r, self.king_w)

    def MAN_JUMP_RED(self, index, list_of_checkers, man_jump, taken_by_man):
        # IF NOT RIGHTMOST, YOU CAN EAT FORWARD RIGHT
        if index % self.Nx != self.Nx-1:
            temp = index + self.step_fr_r
            temp2 = temp + self.step_fr_r
            if index//self.Nx > 1 and temp % self.Nx != self.Nx-1 and list_of_checkers[temp] > 0 and list_of_checkers[temp2] == 0:
                # record the position of taken pieces
                taken_by_man.append(temp)
                man_jump.append((index, temp2))
            temp = index + self.step_br_r
            temp2 = temp + self.step_br_r
            if index//self.Nx < self.Nx-2 and temp % self.Nx != self.Nx-1 and list_of_checkers[temp] > 0 and list_of_checkers[temp2] == 0:
                taken_by_man.append(temp)
                man_jump.append((index, temp2))

        # IF NOT LEFTMOST, YOU CAN EAT FORWARD LEFT
        if index % self.Nx != 0:
            temp = index + self.step_fl_r
            temp2 = temp + self.step_fl_r
            if index//self.Nx > 1 and temp % self.Nx != 0 and list_of_checkers[temp] > 0 and list_of_checkers[temp2] == 0:
                # record the position of taken pieces
                taken_by_man.append(temp)
                man_jump.append((index, temp2))
            temp = index + self.step_bl_r
            temp2 = temp + self.step_bl_r
            if index//self.Nx < self.Nx-2 and temp % self.Nx != 0 and list_of_checkers[temp] > 0 and list_of_checkers[temp2] == 0:
                taken_by_man.append(temp)
                man_jump.append((index, temp2))

    def MAN_WALK_RED(self, index, list_of_checkers, man_walk):
        if index // self.Nx > 0:
            if index % self.Nx < self.Nx-1:
                temp = index + self.step_fr_r
                if list_of_checkers[temp] == 0:
                    man_walk.append((index, temp))
            if index % self.Nx > 0:
                temp = index + self.step_fl_r
                if list_of_checkers[temp] == 0:
                    man_walk.append((index, temp))

    def KING_JUMP_RED(self, index, list_of_checkers, king_jump, taken_by_king):
        if index % self.Nx != self.Nx-1:  # Not Rightmost
            temp = index + self.step_fr_r
            temp2 = temp + self.step_fr_r
            if index//self.Nx > 1 and temp % self.Nx != self.Nx-1 and list_of_checkers[temp] > 0.0 and list_of_checkers[temp2] == 0:
                # record the position of taken pieces
                taken_by_king.append(temp)
                king_jump.append((index, temp2))
            temp = index + self.step_br_r
            temp2 = temp + self.step_br_r
            if index//self.Nx < self.Nx-2 and temp % self.Nx != self.Nx-1 and list_of_checkers[temp] > 0 and list_of_checkers[temp2] == 0:
                # record the position of taken pieces
                taken_by_king.append(temp)
                king_jump.append((index, temp2))

        if index % self.Nx != 0:           # Not Leftmost
            temp = index + self.step_fl_r
            temp2 = temp + self.step_fl_r
            if index//self.Nx > 1 and temp % self.Nx != 0 and list_of_checkers[temp] > 0.0 and list_of_checkers[temp2] == 0:
                # record the position of taken pieces
                taken_by_king.append(temp)
                king_jump.append((index, temp2))
            temp = index + self.step_bl_r
            temp2 = temp + self.step_bl_r
            if index//self.Nx < self.Nx-2 and temp % self.Nx != 0 and list_of_checkers[temp] > 0 and list_of_checkers[temp2] == 0:
                # record the position of taken pieces
                taken_by_king.append(temp)
                king_jump.append((index, temp2))

    def KING_WALK_RED(self, index, list_of_checkers, king_walk):
        temp_fr = index
        temp_br = index
        temp_fl = index
        temp_bl = index
        is_fr_done = False
        is_br_done = False
        is_fl_done = False
        is_bl_done = False

        while True:

            # 1. while not rightmost and not topmost, move forward right
            if not is_fr_done and temp_fr % self.Nx != self.Nx-1 and temp_fr//self.Nx > 0:
                temp_fr += self.step_fr_r
                if list_of_checkers[temp_fr] == 0:
                    king_walk.append((index, temp_fr))
                else:
                    is_fr_done = True
            else:
                is_fr_done = True

            # 2. while not rightmost and not bottom, move backward right
            if not is_br_done and temp_br % self.Nx != self.Nx-1 and temp_br//self.Nx < self.Nx-1:
                temp_br += self.step_br_r
                if list_of_checkers[temp_br] == 0:
                    king_walk.append((index, temp_br))
                else:
                    is_br_done = True
            else:
                is_br_done = True

            # 3. while not leftmost and not topmost, move forward left
            if not is_fl_done and temp_fl % self.Nx != 0 and temp_fl//self.Nx > 0:
                temp_fl += self.step_fl_r
                if list_of_checkers[temp_fl] == 0:
                    king_walk.append((index, temp_fl))
                else:
                    is_fl_done = True
            else:
                is_fl_done = True

            # 4. while not leftmost and not bottom, move backward left
            if not is_bl_done and temp_bl % self.Nx != 0 and temp_bl//self.Nx < self.Nx-1:
                temp_bl += self.step_bl_r
                if list_of_checkers[temp_bl] == 0:
                    king_walk.append((index, temp_bl))
                else:
                    is_bl_done = True
            else:
                is_bl_done = True

            # Sentinel
            if is_fr_done and is_br_done and is_fl_done and is_bl_done:
                break

    def MAN_JUMP_WHITE(self, index, list_of_checkers, man_jump, taken_by_man):
        if index % self.Nx != self.Nx-1:
            temp = index + self.step_fr_w
            temp2 = temp + self.step_fr_w
            if index//self.Nx < self.Nx-2 and temp % self.Nx != self.Nx-1 and list_of_checkers[temp] < 0 and list_of_checkers[temp2] == 0:
                # record the position of taken pieces
                taken_by_man.append(temp)
                man_jump.append((index, temp2))
            temp = index + self.step_br_w
            temp2 = temp + self.step_br_w
            if index//self.Nx > 1 and temp % self.Nx != self.Nx-1 and list_of_checkers[temp] < 0 and list_of_checkers[temp2] == 0:
                taken_by_man.append(temp)
                man_jump.append((index, temp2))

        if index % self.Nx != 0:
            temp = index + self.step_fl_w
            temp2 = temp + self.step_fl_w
            if index//self.Nx < self.Nx-2 and temp % self.Nx != 0 and list_of_checkers[temp] < 0 and list_of_checkers[temp2] == 0:
                # record the position of taken pieces
                taken_by_man.append(temp)
                man_jump.append((index, temp2))
            temp = index + self.step_bl_w
            temp2 = temp + self.step_bl_w
            if index//self.Nx > 1 and temp % self.Nx != 0 and list_of_checkers[temp] < 0 and list_of_checkers[temp2] == 0:
                taken_by_man.append(temp)
                man_jump.append((index, temp2))

    def MAN_WALK_WHITE(self, index, list_of_checkers, man_walk):
        if index//self.Nx < self.Nx-1:
            if index % self.Nx < self.Nx-1:
                temp = index + self.step_fr_w
                if list_of_checkers[temp] == 0:
                    man_walk.append((index, temp))
            if index % self.Nx > 0:
                temp = index + self.step_fl_w
                if list_of_checkers[temp] == 0:
                    man_walk.append((index, temp))

    def KING_JUMP_WHITE(self, index, list_of_checkers, king_jump, taken_by_king):
        if index % self.Nx != self.Nx-1:
            temp = index + self.step_fr_w
            temp2 = temp + self.step_fr_w
            if index//self.Nx < self.Nx-2 and temp % self.Nx != self.Nx-1 and list_of_checkers[temp] < 0 and list_of_checkers[temp2] == 0:
                # record the position of taken pieces
                taken_by_king.append(temp)
                king_jump.append((index, temp2))
            temp = index + self.step_br_w
            temp2 = temp + self.step_br_w
            if index//self.Nx > 1 and temp % self.Nx != self.Nx-1 and list_of_checkers[temp] < 0 and list_of_checkers[temp2] == 0:
                # record the position of taken pieces
                taken_by_king.append(temp)
                king_jump.append((index, temp2))
        if index % self.Nx != 0:
            temp = index + self.step_fl_w
            temp2 = temp + self.step_fl_w
            if index//self.Nx < self.Nx-2 and temp % self.Nx != 0 and list_of_checkers[temp] < 0 and list_of_checkers[temp2] == 0:
                # record the position of taken pieces
                taken_by_king.append(temp)
                king_jump.append((index, temp2))
            temp = index + self.step_bl_w
            temp2 = temp + self.step_bl_w
            if index//self.Nx > 1 and temp % self.Nx != 0 and list_of_checkers[temp] < 0 and list_of_checkers[temp2] == 0:
                # record the position of taken pieces
                taken_by_king.append(temp)
                king_jump.append((index, temp2))

    def KING_WALK_WHITE(self, index, list_of_checkers, king_walk):
        temp_fr = index
        temp_br = index
        temp_fl = index
        temp_bl = index
        is_fr_done = False
        is_br_done = False
        is_fl_done = False
        is_bl_done = False

        while True:

            # 1. while not rightmost and not bottom, move forward right
            if not is_fr_done and temp_fr % self.Nx != self.Nx-1 and temp_fr//self.Nx < self.Nx-1:
                temp_fr += self.step_fr_w
                if list_of_checkers[temp_fr] == 0:
                    king_walk.append((index, temp_fr))
                else:
                    is_fr_done = True
            else:
                is_fr_done = True

            # 2. while not rightmost and not topmost, move backward right
            if not is_br_done and temp_br % self.Nx != self.Nx-1 and temp_br//self.Nx > 0:
                temp_br += self.step_br_w
                if list_of_checkers[temp_br] == 0:
                    king_walk.append((index, temp_br))
                else:
                    is_br_done = True
            else:
                is_br_done = True

            # 3. while not leftmost and not bottom, move forward left
            if not is_fl_done and temp_fl % self.Nx != 0 and temp_fl//self.Nx < self.Nx-1:
                temp_fl += self.step_fl_w
                if list_of_checkers[temp_fl] == 0:
                    king_walk.append((index, temp_fl))
                else:
                    is_fl_done = True
            else:
                is_fl_done = True

            # 4. while not leftmost and not topmost, move backward left
            if not is_bl_done and temp_bl % self.Nx != 0 and temp_bl//self.Nx > 0:
                temp_bl += self.step_bl_w
                if list_of_checkers[temp_bl] == 0:
                    king_walk.append((index, temp_bl))
                else:
                    is_bl_done = True
            else:
                is_bl_done = True

            # Sentinel
            if is_fr_done and is_br_done and is_fl_done and is_bl_done:
                break

    def AVAILABLE_MOVE(self, side, list_of_checkers):
        man_jump = []
        king_jump = []
        man_walk = []
        king_walk = []
        taken_by_man = []
        taken_by_king = []
        have_man = []
        have_king = []

        # red
        if side == 1:
            for index, element in enumerate(list_of_checkers):
                # red man jump
                if element == -self.man_value:
                    self.MAN_JUMP_RED(index, list_of_checkers,
                                      man_jump, taken_by_man)
                    # save the position having man so no need to go through the empty sites again
                    have_man.append(index)
                # red king jump
                elif element == -self.king_value:
                    self.KING_JUMP_RED(index, list_of_checkers,
                                       king_jump, taken_by_king)
                    # save the position having king so no need to go through the empty sites again
                    have_king.append(index)
            if man_jump == [] and king_jump == []:
                for index in have_man:
                    self.MAN_WALK_RED(index, list_of_checkers, man_walk)
                for index in have_king:
                    self.KING_WALK_RED(index, list_of_checkers, king_walk)
        # white
        if side == -1:
            for index, element in enumerate(list_of_checkers):
                # white man jump
                if element == self.man_value:
                    self.MAN_JUMP_WHITE(
                        index, list_of_checkers, man_jump, taken_by_man)
                    # save the position having man so no need to go through the empty sites again
                    have_man.append(index)
                # white king jump
                elif element == self.king_value:
                    self.KING_JUMP_WHITE(
                        index, list_of_checkers, king_jump, taken_by_king)
                    # save the position having king so no need to go through the empty sites again
                    have_king.append(index)
            if man_jump == [] and king_jump == []:
                for index in have_man:
                    self.MAN_WALK_WHITE(index, list_of_checkers, man_walk)
                for index in have_king:
                    self.KING_WALK_WHITE(index, list_of_checkers, king_walk)

        return (man_jump, king_jump, man_walk, king_walk, taken_by_man, taken_by_king)

    def COMPUTE(self, operand1, operand2, stop):  # Balanced
        op = self.operations[stop]
        if op == '∧' or op == '⇔' or op == '↓':  # AND XNOR NOR
            return -1
        elif op == '∨' or op == '⊻' or op == '↑':  # OR XOR NAND
            return 1
        elif op == '¬' or op == '⇒':
            if operand1 == 1:  # WHITE JUMPS
                return -1
            else:             # BLACK JUMPS
                return 1
        elif op == '⇐':
            if operand1 == 1:  # WHITE JUMPS
                return 1
            else:
                return -1
        else:
            return 0

    def COMPUTE_KING(self, operand1, operand2, stop):
        op = self.operations[stop]
        if op == '∧':  # AND
            return -1
        elif op == '∨':  # OR
            return 1
        elif op == '⇔':  # XNOR
            if operand1 == 1:  # WHITE CHANGES AND GET 1 PT
                return 1
            else:
                return -1
        elif op == '↓':  # NOR
            if operand1 == 1:  # WHITE CHANGES AND GET 1 PT
                return 1
            else:
                return -1
        elif op == '⇒':  # WHITE IMBALANCE SINCE IT CAN CHANGE TO F VALUE
            return 1
        elif op == '⊻':  # XOR
            if operand1 == -1:  # BLACK CHANGES AND GET -1 PT
                return -1
            else:
                return 1
        elif op == '↑':  # NAND
            if operand1 == -1:  # BLACK CHANGES AND GET -1 PT
                return -1
            else:
                return 1
        elif op == '⇐':  # AS IS (SAME AS MAN)
            if operand1 == 1:  # WHITE JUMPS
                return 1
            else:
                return -1
        elif op == '¬':
            if operand1 == 1:  # WHITE CHAGES TO -1 AND GETS 1 AS NEGATION
                return 1
            else:
                return -1
        else:
            return 0

    # def COMPUTE(self, operand1, operand2, stop):
    #     op = self.operations[stop]
    #     if op == '∧':
    #         return (-1)
    #     elif op == '∨':
    #         return (1)
    #     elif op == '⇒':
    #         return (1)
    #     elif op == '⇔':
    #         return (-1)
    #     else:
    #         return (0)

    def saving(self, list_of_checkers, save):
        # Use copy to clone the element of list.
        save.append(list_of_checkers.copy())
