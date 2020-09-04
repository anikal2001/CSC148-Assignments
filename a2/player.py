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
Misha Schwartz, and Jaisie Sin.

=== Module Description ===

This file contains the hierarchy of player classes.
"""
from __future__ import annotations
from typing import List, Optional, Tuple
import random
import pygame

from block import Block
from goal import Goal, generate_goals

from actions import KEY_ACTION, ROTATE_CLOCKWISE, ROTATE_COUNTER_CLOCKWISE, \
    SWAP_HORIZONTAL, SWAP_VERTICAL, SMASH, PASS, PAINT, COMBINE


def create_players(num_human: int, num_random: int, smart_players: List[int]) \
        -> List[Player]:
    """Return a new list of Player objects.

    <num_human> is the number of human player, <num_random> is the number of
    random players, and <smart_players> is a list of difficulty levels for each
    SmartPlayer that is to be created.

    The list should contain <num_human> HumanPlayer objects first, then
    <num_random> RandomPlayer objects, then the same number of SmartPlayer
    objects as the length of <smart_players>. The difficulty levels in
    <smart_players> should be applied to each SmartPlayer object, in order.
    """
    player_lst = []
    id_num = num_human + num_random + len(smart_players)
    goals = generate_goals(id_num)

    if id_num >= 4:
        id_num = 4

    for i in range(0, id_num):
        if i < num_human and num_human > 0:
            player_lst.append(HumanPlayer(i, goals[i]))
        elif num_human - 1 < i <= (num_random + num_human - 1) and \
                num_random > 0:
            player_lst.append(RandomPlayer(i, goals[i]))
        else:
            player_lst.append(SmartPlayer(i, goals[i], smart_players\
                [i-num_human-num_random]))
    return player_lst


def _get_block(block: Block, location: Tuple[int, int], level: int) -> \
        Optional[Block]:
    """Return the Block within <block> that is at <level> and includes
    <location>. <location> is a coordinate-pair (x, y).

    A block includes all locations that are strictly inside of it, as well as
    locations on the top and left edges. A block does not include locations that
    are on the bottom or right edge.

    If a Block includes <location>, then so do its ancestors. <level> specifies
    which of these blocks to return. If <level> is greater than the level of
    the deepest block that includes <location>, then return that deepest block.

    If no Block can be found at <location>, return None.

    Preconditions:
        - 0 <= level <= max_depth
    """
    if block.position[0] <= location[0] < block.position[0] + block.size and \
        block.position[1] <= location[1] < block.position[1] + block.size:
        if level == block.level or block.children == []:
            return block
        for child in block.children:
            c_block = _get_block(child, location, level)
            if c_block is not None:
                return c_block
    return None




class Player:
    """A player in the Blocky game.

    This is an abstract class. Only child classes should be instantiated.

    === Public Attributes ===
    id:
        This player's number.
    goal:
        This player's assigned goal for the game.
    """
    id: int
    goal: Goal

    def __init__(self, player_id: int, goal: Goal) -> None:
        """Initialize this Player.
        """
        self.goal = goal
        self.id = player_id

    def get_selected_block(self, board: Block) -> Optional[Block]:
        """Return the block that is currently selected by the player.

        If no block is selected by the player, return None.
        """
        raise NotImplementedError

    def process_event(self, event: pygame.event.Event) -> None:
        """Update this player based on the pygame event.
        """
        raise NotImplementedError

    def generate_move(self, board: Block) -> \
            Optional[Tuple[str, Optional[int], Block]]:
        """Return a potential move to make on the game board.

        The move is a tuple consisting of a string, an optional integer, and
        a block. The string indicates the move being made (i.e., rotate, swap,
        or smash). The integer indicates the direction (i.e., for rotate and
        swap). And the block indicates which block is being acted on.

        Return None if no move can be made, yet.
        """
        raise NotImplementedError


def _create_move(action: Tuple[str, Optional[int]], block: Block) -> \
        Tuple[str, Optional[int], Block]:
    """
    Returns a formatted move in the form of a tuple, of the move name, and the
    chosen block to perform the move on.
    """
    return action[0], action[1], block


class HumanPlayer(Player):
    """A human player.
    """
    # == Public Attributes ==
    # id:
    # This player's id number.
    # goal:
    # This player's assigned goal for the game.

    # === Private Attributes ===
    # _level:
    #     The level of the Block that the user selected most recently.
    # _desired_action:
    #     The most recent action that the user is attempting to do.
    #
    # == Representation Invariants concerning the private attributes ==
    #     _level >= 0
    id: int
    goal: Goal
    _level: int
    _desired_action: Optional[Tuple[str, Optional[int]]]

    def __init__(self, player_id: int, goal: Goal) -> None:
        """Initialize this HumanPlayer with the given <renderer>, <player_id>
        and <goal>.
        """
        Player.__init__(self, player_id, goal)

        # This HumanPlayer has not yet selected a block, so set _level to 0
        # and _selected_block to None.
        self._level = 0
        self._desired_action = None

    def get_selected_block(self, board: Block) -> Optional[Block]:
        """Return the block that is currently selected by the player based on
        the position of the mouse on the screen and the player's desired level.

        If no block is selected by the player, return None.
        """
        mouse_pos = pygame.mouse.get_pos()
        block = _get_block(board, mouse_pos, self._level)

        return block

    def process_event(self, event: pygame.event.Event) -> None:
        """Respond to the relevant keyboard events made by the player based on
        the mapping in KEY_ACTION, as well as the W and S keys for changing
        the level.
        """
        if event.type == pygame.KEYDOWN:
            if event.key in KEY_ACTION:
                self._desired_action = KEY_ACTION[event.key]
            elif event.key == pygame.K_w:
                self._level = max(0, self._level - 1)
                self._desired_action = None
            elif event.key == pygame.K_s:
                self._level += 1
                self._desired_action = None

    def generate_move(self, board: Block) -> \
            Optional[Tuple[str, Optional[int], Block]]:
        """Return the move that the player would like to perform. The move may
        not be valid.

        Return None if the player is not currently selecting a block.
        """
        block = self.get_selected_block(board)

        if block is None or self._desired_action is None:
            return None
        else:
            move = _create_move(self._desired_action, block)

            self._desired_action = None
            return move


class RandomPlayer(Player):
    """A RandomPlayer, which is an automated player that picks their next move
    at random."""
    # == Public Attributes ==
    # id:
    # This player's id number.
    # goal:
    # This player's assigned goal for the game.

    # === Private Attributes ===
    # _proceed:
    #   True when the player should make a move, False when the player should
    #   wait.

    id: int
    goal: Goal
    _proceed: bool

    def __init__(self, player_id: int, goal: Goal) -> None:
        """Initializes a new RandomPlayer.
        """
        Player.__init__(self, player_id, goal)
        self._proceed = False

    def get_selected_block(self, board: Block) -> Optional[Block]:
        """ Returns None.
        """
        return None

    def process_event(self, event: pygame.event.Event) -> None:
        """Sets self._proceed to True if the mousebutton is pressed.
        """
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self._proceed = True

    def generate_move(self, board: Block) ->\
            Optional[Tuple[str, Optional[int], Block]]:
        """Return a valid, randomly generated move.

        A valid move is a move other than PASS that can be successfully
        performed on the <board>.

        This function does not mutate <board>.
        """
        if not self._proceed:
            return None  # Do not remove
        board_copy = board.create_copy()
        move_tup = _find_valid_move(self.goal.colour, board_copy)
        change_block = _get_block(board, move_tup[1], move_tup[2])
        move = move_tup[0]
        self._proceed = False  # Must set to False before returning!
        return _create_move(tuple(move), change_block)


class SmartPlayer(Player):
    """
    A SmartPlayer, which is an automated player that picks the highest score out
    of a randomly generated selection of possible moves.
    """
    # == Public Attributes ==
    # id:
    # This player's id number.
    # goal:
    # This player's assigned goal for the game.

    # === Private Attributes ===
    # _proceed:
    #   True when the player should make a move, False when the player should
    #   wait.
    # _difficulty:
    #The difficulty that the SmartPlayer will play at.

    id: int
    goal: Goal
    _proceed: bool
    _difficulty: int

    def __init__(self, player_id: int, goal: Goal, difficulty: int) -> None:
        """Initializes a new SmartPlayer.
        """
        Player.__init__(self, player_id, goal)
        self._difficulty = difficulty
        self._proceed = False

    def get_selected_block(self, board: Block) -> Optional[Block]:
        """Returns None.
        """
        return None

    def process_event(self, event: pygame.event.Event) -> None:
        """Sets self._proceed to True if the mousebutton is pressed.
        """
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self._proceed = True

    def generate_move(self, board: Block) ->\
            Optional[Tuple[str, Optional[int], Block]]:
        """Return a valid move by assessing multiple valid moves and choosing
        the move that results in the highest score for this player's goal (i.e.,
        disregarding penalties).

        A valid move is a move other than PASS that can be successfully
        performed on the <board>. If no move can be found that is better than
        the current score, this player will pass.

        This function does not mutate <board>.

        PRECONDITION: self.difficulty > 0
        """
        if not self._proceed:
            return None

        num_moves = self._difficulty
        max_score = self.goal.score(board)
        original_score = self.goal.score(board)
        best_move = tuple('')
        best_block = None

        for _ in range(num_moves):
            copy_board = board.create_copy()
            valid_tup = _find_valid_move(self.goal.colour, copy_board)
            temp_move = valid_tup[0]

            if max_score < self.goal.score(copy_board):
                max_score = self.goal.score(copy_board)
                best_move = temp_move
                best_block = _get_block(board, valid_tup[1], valid_tup[2])

        self._proceed = False
        if max_score == original_score:
            return _create_move(PASS, board)
        return _create_move(best_move, best_block)

def _find_valid_move(goal_colour: Tuple[int, int, int], board: Block) -> \
        Tuple[str, Tuple[int, int], int]:
    """
    Helper for SmartPlayer.generate_move and RandomPlayer.generate_move. Returns
    a tuple of the random valid move, a random location, a the random block
    depth for the move to be enacted on. Returns

    """
    is_valid = False
    move = ''
    rand_location = (0, 0)
    rand_depth = 0

    while not is_valid:
        copy_board = board.create_copy()
        x = random.randint(0, board.size - 1)
        y = random.randint(0, board.size - 1)
        rand_location = (x, y)
        rand_depth = random.randint(0, board.max_depth)
        temp_block = _get_block(copy_board, rand_location, rand_depth)
        true_block = _get_block(board, rand_location, rand_depth)

        rand_move = random.randint(1, 7)
        if rand_move == 1:
            is_valid = temp_block.smash()
            if is_valid:
                move = SMASH
                true_block.smash()

        elif rand_move == 2:
            is_valid = temp_block.swap(0)
            if is_valid:
                move = SWAP_HORIZONTAL
                true_block.swap(0)
        elif rand_move == 3:
            is_valid = temp_block.swap(1)
            if is_valid:
                move = SWAP_VERTICAL
                true_block.swap(1)
        elif rand_move == 4:
            is_valid = temp_block.rotate(1)
            if is_valid:
                move = ROTATE_CLOCKWISE
                true_block.rotate(1)
        elif rand_move == 5:
            is_valid = temp_block.rotate(3)
            if is_valid:
                move = ROTATE_COUNTER_CLOCKWISE
                true_block.rotate(3)
        elif rand_move == 6:
            is_valid = temp_block.paint(goal_colour)
            if is_valid:
                move = PAINT
                true_block.paint(goal_colour)
        else:
            is_valid = temp_block.combine()
            if is_valid:
                move = COMBINE
                true_block.combine()

    return move, rand_location, rand_depth


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'allowed-io': ['process_event'],
        'allowed-import-modules': [
            'doctest', 'python_ta', 'random', 'typing', 'actions', 'block',
            'goal', 'pygame', '__future__'
        ],
        'max-attributes': 10,
        'generated-members': 'pygame.*'
    })
