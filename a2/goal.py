"""CSC148 Assignment 2

=== CSC148 Winter 2020 ===
Department of Computer Science,
University of Toronto

This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

Authors: Diane Horton, David Liu, Mario Badr, Sophia Huynh, Misha Schwartz,
and Jaisie Sin

All of the files in this directory and all subdirectories are:
Copyright (c) Diane Horton, David Liu, Mario Badr, Sophia Huynh,
Misha Schwartz, and Jaisie Sin

=== Module Description ===

This file contains the hierarchy of Goal classes.
"""
from __future__ import annotations
import random
from typing import List, Tuple
from block import Block
from settings import COLOUR_LIST


def generate_goals(num_goals: int) -> List[Goal]:
    """Return a randomly generated list of goals with length num_goals.

    All elements of the list must be the same type of goal, but each goal
    must have a different randomly generated colour from COLOUR_LIST. No two
    goals can have the same colour.

    Precondition:
        - num_goals <= len(COLOUR_LIST)
    """
    goals = [PerimeterGoal(COLOUR_LIST[0]), BlobGoal(COLOUR_LIST[0])]
    rand_goal = random.randint(0, 1)
    chosen_goal = goals[rand_goal]
    goal_list = []
    num_list = [0, 1, 2, 3]
    if isinstance(chosen_goal, PerimeterGoal):
        random.shuffle(num_list)
        for i in range(0, num_goals):
            goal_list.append(PerimeterGoal(COLOUR_LIST[num_list[i]]))
    else:
        random.shuffle(num_list)
        for i in range(0, num_goals):
            goal_list.append(BlobGoal(COLOUR_LIST[num_list[i]]))

    return goal_list


def _flatten(block: Block) -> List[List[Tuple[int, int, int]]]:
    """Return a two-dimensional list representing <block> as rows and columns of
    unit cells.

    Return a list of lists L, where,
    for 0 <= i, j < 2^{max_depth - self.level}
        - L[i] represents column i and
        - L[i][j] represents the unit cell at column i and row j.

    Each unit cell is represented by a tuple of 3 ints, which is the colour
    of the block at the cell location[i][j]

    L[0][0] represents the unit cell in the upper left corner of the Block.
    """
    ret_list = []
    num_row = 2 ** (block.max_depth - block.level)
    if len(block.children) == 0:
        for _ in range(0, num_row):
            temp_list = []
            for j in range(0, num_row):
                temp_list.append(block.colour)
            ret_list.append(temp_list)
    else:
        for j in range(0, num_row):
            temp_list = []
            if j < (num_row / 2):
                temp_list.extend(_flatten(block.children[1])[j])
                temp_list.extend(_flatten(block.children[2])[j])
            else:
                temp_list.extend(
                    _flatten(block.children[0])[j - (num_row // 2)])
                temp_list.extend(
                    _flatten(block.children[3])[j - (num_row // 2)])
            ret_list.append(temp_list)
    return ret_list


class Goal:
    """A player goal in the game of Blocky.

    This is an abstract class. Only child classes should be instantiated.

    === Attributes ===
    colour:
        The target colour for this goal, that is the colour to which
        this goal applies.
    """
    colour: Tuple[int, int, int]

    def __init__(self, target_colour: Tuple[int, int, int]) -> None:
        """Initialize this goal to have the given target colour.
        """
        self.colour = target_colour

    def score(self, board: Block) -> int:
        """Return the current score for this goal on the given board.

        The score is always greater than or equal to 0.
        """
        raise NotImplementedError

    def description(self) -> str:
        """Return a description of this goal.
        """
        raise NotImplementedError


class PerimeterGoal(Goal):
    """A PerimeterGoal, a goal where players aim to have the most blocks of
    their respective color on the edges, or perimeter of the block."""

    # === Public Attributes ===
    # colour:
    # The target colour for this goal, that is the colour to which
    # this goal applies.

    colour: Tuple[int, int, int]

    def score(self, board: Block) -> int:
        """ Returns score based on PerimeterGoal. Adds 1 point to the score for
        blocks on the side border and 2 points for corner blocks.
        """
        score = 0
        flat_board = _flatten(board)
        if self.colour == board.colour and board.max_depth == 0:
            return 4

        if len(flat_board) > 1:
            for row in range(0, len(flat_board)):  # left and right column
                for i in range(0, -2, -1):
                    score += self._score_helper(flat_board, row, i)

        if len(flat_board) > 2:
            for j in range(1, len(flat_board[0]) - 1):  # first row middle
                if flat_board[0][j] == self.colour:
                    score += 1

            for k in range(1, len(flat_board) - 1):  # last row middle
                if flat_board[len(flat_board) - 1][k] == self.colour:
                    score += 1

        return score

    def _score_helper(self, flat_board: List[List[Tuple[int, int, int]]],
                      x: int, y: int) -> int:
        """ Helper for PerimeterGoal.score. Returns an int of how much the score
        should increase. Calculates the score based on PerimeterGoal of
        the left and right columns of the board given.

        """
        if flat_board[x][y] == self.colour:
            if x in (0, len(flat_board) - 1):
                return 2
            else:
                return 1
        return 0

    def description(self) -> str:
        """Returns a description of PerimeterGoal.
        """
        return 'The player must aim to put the most possible units of a given \
        colour c on the outer perimeter of the board.'


class BlobGoal(Goal):
    """
    A BlobGoal, a goal where players try to get the largest mass in one place
    of their respective color..
    """

    # === Public Attributes ===
    # colour:
    # The target colour for this goal, that is the colour to which
    # this goal applies.

    colour: Tuple[int, int, int]

    def score(self, board: Block) -> int:
        """Return score based on BlobGoal, which calculates the largest mass
        of the given goal color.
        """
        max_blob = 0
        flat_board = _flatten(board)
        visited = []
        blob = 0
        for _ in flat_board:
            new_lst = []
            for _ in flat_board:
                new_lst.append(-1)
            visited.append(new_lst)

        for k in range(len(flat_board)):
            for m in range(len(flat_board[k])):
                if visited[k][m] == -1:
                    blob = self._undiscovered_blob_size((k, m),
                                                        flat_board, visited)
                if blob > max_blob:
                    max_blob = blob
        return max_blob

    def _undiscovered_blob_size(self, pos: Tuple[int, int],
                                board: List[List[Tuple[int, int, int]]],
                                visited: List[List[int]]) -> int:
        """Return the size of the largest connected blob that (a) is of this
        Goal's target colour, (b) includes the cell at <pos>, and (c) involves
        only cells that have never been visited.

        If <pos> is out of bounds for <board>, return 0.

        <board> is the flattened board on which to search for the blob.
        <visited> is a parallel structure that, in each cell, contains:
            -1 if this cell has never been visited
            0  if this cell has been visited and discovered
               not to be of the target colour
            1  if this cell has been visited and discovered
               to be of the target colour

        Update <visited> so that all cells that are visited are marked with
        either 0 or 1.
        """
        size = 0
        if 0 <= pos[0] < len(board) and 0 <= pos[1] < len(board):
            if visited[pos[0]][pos[1]] == -1 and \
                    board[pos[0]][pos[1]] == self.colour:
                size += 1
                visited[pos[0]][pos[1]] = 1
            else:
                visited[pos[0]][pos[1]] = 0
                return 0

            adjacent = [(pos[0] - 1, pos[1]), (pos[0] + 1, pos[1]),
                        (pos[0], pos[1] - 1), (pos[0], pos[1] + 1)]
            # up, down, left, right
            for block in adjacent:
                if 0 <= block[0] < len(board) and 0 <= block[1] < len(board):
                    size += self._undiscovered_blob_size(block, board,
                                                         visited)
        return size

    def description(self) -> str:
        """Returns a description of BlobGoal.
        """
        return 'The player must aim for the largest “blob” of a given colour c.'


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'allowed-import-modules': [
            'doctest', 'python_ta', 'random', 'typing', 'block', 'settings',
            'math', '__future__'
        ],
        'max-attributes': 15
    })
