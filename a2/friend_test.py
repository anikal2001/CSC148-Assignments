#
from typing import List, Optional, Tuple
# import os
# import pygame
# import pytest

from block import Block
from blocky import _block_to_squares
from goal import BlobGoal, PerimeterGoal, _flatten, generate_goals
from player import _get_block, create_players
from renderer import Renderer
from settings import COLOUR_LIST


def set_children(block: Block, colours: List[Optional[Tuple[int, int, int]]]) \
        -> None:
    """Set the children at <level> for <block> using the given <colours>.

    Precondition:
        - len(colours) == 4
        - block.level + 1 <= block.max_depth
    """
    size = block._child_size()
    positions = block._children_positions()
    level = block.level + 1
    depth = block.max_depth

    block.children = []  # Potentially discard children
    for i in range(4):
        b = Block(positions[i], size, colours[i], level, depth)
        block.children.append(b)


def board_one_by_one() -> Block:
    board = Block((0, 0), 750, COLOUR_LIST[1], 0, 0)
    return board


def board_2x2() -> Block:
    # Level 0
    board = Block((0, 0), 750, None, 0, 1)

    # Level 1
    colours = [COLOUR_LIST[0], COLOUR_LIST[2], COLOUR_LIST[1], COLOUR_LIST[3]]
    set_children(board, colours)

    return board


def board_2x2_swap_0() -> Block:
    # Level 0
    board = Block((0, 0), 750, None, 0, 1)

    # Level 1
    colours = [COLOUR_LIST[2], COLOUR_LIST[0], COLOUR_LIST[3], COLOUR_LIST[1]]
    set_children(board, colours)

    return board


def board_2x2_swap_1() -> Block:
    # Level 0
    board = Block((0, 0), 750, None, 0, 1)

    # Level 1
    colours = [COLOUR_LIST[3], COLOUR_LIST[1], COLOUR_LIST[2], COLOUR_LIST[0]]
    set_children(board, colours)

    return board


def board_2x2_clockwise_once() -> Block:
    # Level 0
    board = Block((0, 0), 750, None, 0, 1)

    # Level 1
    colours = [COLOUR_LIST[2], COLOUR_LIST[1], COLOUR_LIST[3], COLOUR_LIST[0]]
    set_children(board, colours)

    return board


def board_2x2_clockwise_twice() -> Block:
    # Level 0
    board = Block((0, 0), 750, None, 0, 1)

    # Level 1
    colours = [COLOUR_LIST[1], COLOUR_LIST[3], COLOUR_LIST[0], COLOUR_LIST[2]]
    set_children(board, colours)

    return board


def board_2x2_clockwise_three_times() -> Block:
    # Level 0
    board = Block((0, 0), 750, None, 0, 1)

    # Level 1
    colours = [COLOUR_LIST[3], COLOUR_LIST[0], COLOUR_LIST[2], COLOUR_LIST[1]]
    set_children(board, colours)

    return board


def board_2x2_combine_1() -> Block:
    # Level 0
    board = Block((0, 0), 750, None, 0, 1)

    # Level 1
    colours = [COLOUR_LIST[2], COLOUR_LIST[2], COLOUR_LIST[1], COLOUR_LIST[3]]
    set_children(board, colours)

    return board


def board_2x2_combine_2() -> Block:
    # Level 0
    board = Block((0, 0), 750, None, 0, 1)

    # Level 1
    colours = [COLOUR_LIST[3], COLOUR_LIST[1], COLOUR_LIST[2], COLOUR_LIST[2]]
    set_children(board, colours)

    return board


def board_2x2_combine_3() -> Block:
    # Level 0
    board = Block((0, 0), 750, None, 0, 1)

    # Level 1
    colours = [COLOUR_LIST[2], COLOUR_LIST[1], COLOUR_LIST[3], COLOUR_LIST[2]]
    set_children(board, colours)

    return board


def board_2x2_combine_4() -> Block:
    # Level 0
    board = Block((0, 0), 750, None, 0, 1)

    # Level 1
    colours = [COLOUR_LIST[2], COLOUR_LIST[2], COLOUR_LIST[1], COLOUR_LIST[1]]
    set_children(board, colours)

    return board


def board_2x2_combine_5() -> Block:
    # Level 0
    board = Block((0, 0), 750, None, 0, 1)

    # Level 1
    colours = [COLOUR_LIST[1], COLOUR_LIST[2], COLOUR_LIST[2], COLOUR_LIST[1]]
    set_children(board, colours)

    return board


def board_2x2_combine_6() -> Block:
    # Level 0
    board = Block((0, 0), 750, None, 0, 1)

    # Level 1
    colours = [COLOUR_LIST[2], COLOUR_LIST[1], COLOUR_LIST[2], COLOUR_LIST[1]]
    set_children(board, colours)

    return board


def board_2x2_combine_7() -> Block:
    # Level 0
    board = Block((0, 0), 750, None, 0, 1)

    # Level 1
    colours = [COLOUR_LIST[2], COLOUR_LIST[2], COLOUR_LIST[2], COLOUR_LIST[1]]
    set_children(board, colours)

    return board


def board_2x2_combine_8() -> Block:
    # Level 0
    board = Block((0, 0), 750, None, 0, 1)

    # Level 1
    colours = [COLOUR_LIST[1], COLOUR_LIST[2], COLOUR_LIST[2], COLOUR_LIST[2]]
    set_children(board, colours)

    return board


def board_2x2_combine_9() -> Block:
    # Level 0
    board = Block((0, 0), 750, None, 0, 1)

    # Level 1
    colours = [COLOUR_LIST[2], COLOUR_LIST[1], COLOUR_LIST[2], COLOUR_LIST[2]]
    set_children(board, colours)

    return board


def board_2x2_combine_10() -> Block:
    # Level 0
    board = Block((0, 0), 750, None, 0, 1)

    # Level 1
    colours = [COLOUR_LIST[2], COLOUR_LIST[2], COLOUR_LIST[2], COLOUR_LIST[2]]
    set_children(board, colours)

    return board


def board_16x16() -> Block:
    """Create a reference board with a size of 750 and a max_depth of 2.
    """
    # Level 0
    board = Block((0, 0), 750, None, 0, 2)

    # Level 1
    colours = [None, COLOUR_LIST[2], COLOUR_LIST[1], COLOUR_LIST[3]]
    set_children(board, colours)

    # Level 2
    colours = [COLOUR_LIST[0], COLOUR_LIST[1], COLOUR_LIST[1], COLOUR_LIST[3]]
    set_children(board.children[0], colours)

    return board


def board_4x4_rotate() -> Block:
    """Create a reference board with a size of 750 and a max_depth of 2.
    """
        # Level 0
    board = Block((0, 0), 750, None, 0, 2)

    # Level 1
    colours = [COLOUR_LIST[2], COLOUR_LIST[1], COLOUR_LIST[3], None]
    set_children(board, colours)

    # Level 2
    colours = [COLOUR_LIST[1], COLOUR_LIST[1], COLOUR_LIST[3], COLOUR_LIST[0]]
    set_children(board.children[3], colours)

    return board


def board_16x16_swap_1() -> Block:
    """Create a reference board with a size of 750 and a max_depth of 2.
    """
    # Level 0
    board = Block((0, 0), 750, None, 0, 2)

    # Level 1
    colours = [COLOUR_LIST[3], COLOUR_LIST[1], COLOUR_LIST[2], None]
    set_children(board, colours)

    # Level 2
    colours = [COLOUR_LIST[0], COLOUR_LIST[1], COLOUR_LIST[1], COLOUR_LIST[3]]
    set_children(board.children[3], colours)

    return board


def board_16x16_example_1() -> Block:
    # """Create a reference board with a size of 750 and a max_depth of 2.
    # """
    # Level 0
    board = Block((0, 0), 750, None, 0, 2)

    # Level 1
    colours = [COLOUR_LIST[2], None, COLOUR_LIST[1], COLOUR_LIST[3]]
    set_children(board, colours)

    # Level 2
    colours = [COLOUR_LIST[0], COLOUR_LIST[1], COLOUR_LIST[1], COLOUR_LIST[3]]
    set_children(board.children[1], colours)

    return board


def board_16x16_example_2() -> Block:
    # """Create a reference board with a size of 750 and a max_depth of 2.
    # """
    # Level 0
    board = Block((0, 0), 750, None, 0, 2)

    # Level 1
    colours = [COLOUR_LIST[2], COLOUR_LIST[1], None, COLOUR_LIST[3]]
    set_children(board, colours)

    # Level 2
    colours = [COLOUR_LIST[0], COLOUR_LIST[1], COLOUR_LIST[1], COLOUR_LIST[3]]
    set_children(board.children[2], colours)

    return board


def board_16x16_example_3() -> Block:
    # """Create a reference board with a size of 750 and a max_depth of 2.
    # """
    # Level 0
    board = Block((0, 0), 750, None, 0, 2)

    # Level 1
    colours = [COLOUR_LIST[2], COLOUR_LIST[1], COLOUR_LIST[3], None]
    set_children(board, colours)

    # Level 2
    colours = [COLOUR_LIST[0], COLOUR_LIST[1], COLOUR_LIST[1], COLOUR_LIST[3]]
    set_children(board.children[3], colours)

    return board


def board_8x8_example() -> Block:
    # Level 0
    board = Block((0, 0), 800, None, 0, 3)

    # Level 1
    colours = [None, None, COLOUR_LIST[3], None]
    set_children(board, colours)

    # Level 2
    colours = [COLOUR_LIST[0], COLOUR_LIST[1], COLOUR_LIST[2], COLOUR_LIST[3]]
    set_children(board.children[0], colours)

    # Level 2
    colours = [None, None, None, None]
    set_children(board.children[1], colours)

    # Level 2
    colours = [COLOUR_LIST[0], COLOUR_LIST[1], None, COLOUR_LIST[3]]
    set_children(board.children[3], colours)

    # Level 3
    colours = [COLOUR_LIST[0], COLOUR_LIST[1], COLOUR_LIST[2], COLOUR_LIST[3]]
    set_children(board.children[1].children[0], colours)
    set_children(board.children[1].children[1], colours)
    set_children(board.children[1].children[2], colours)
    set_children(board.children[1].children[3], colours)
    set_children(board.children[3].children[2], colours)

    return board


def board_8x8_rotate() -> Block:
    # Level 0
    board = Block((0, 0), 800, None, 0, 3)

    # Level 1
    colours = [None, COLOUR_LIST[3], None, None]
    set_children(board, colours)

    # Level 2
    colours = [COLOUR_LIST[1], COLOUR_LIST[2], COLOUR_LIST[3], COLOUR_LIST[0]]
    set_children(board.children[3], colours)

    # Level 2
    colours = [None, None, None, None]
    set_children(board.children[0], colours)

    # Level 2
    colours = [COLOUR_LIST[1], None, COLOUR_LIST[3], COLOUR_LIST[0]]
    set_children(board.children[2], colours)

    # Level 3
    colours = [COLOUR_LIST[1], COLOUR_LIST[2], COLOUR_LIST[3], COLOUR_LIST[0]]
    set_children(board.children[0].children[0], colours)
    set_children(board.children[0].children[1], colours)
    set_children(board.children[0].children[2], colours)
    set_children(board.children[0].children[3], colours)
    set_children(board.children[2].children[1], colours)

    return board


def board_16x16_actual_example() -> Block:
    # Level 0
    board = Block((0, 0), 1600, None, 0, 4)

    # Level 1
    colours = [COLOUR_LIST[0], None, None, None]
    set_children(board, colours)

    # Level 2
    colours = [COLOUR_LIST[0], COLOUR_LIST[1], COLOUR_LIST[2], COLOUR_LIST[3]]
    set_children(board.children[1], colours)

    # Level 2
    colours = [None, None, None, COLOUR_LIST[3]]
    set_children(board.children[2], colours)

    # Level 2
    colours = [None, None, None, None]
    set_children(board.children[3], colours)

    # Level 3
    colours = [None, None, None, None]
    set_children(board.children[3].children[0], colours)
    set_children(board.children[3].children[1], colours)
    set_children(board.children[3].children[2], colours)
    set_children(board.children[3].children[3], colours)

    colours = [COLOUR_LIST[0], COLOUR_LIST[1], COLOUR_LIST[2], COLOUR_LIST[3]]
    set_children(board.children[2].children[0], colours)
    set_children(board.children[2].children[1], colours)

    colours = [None, None, None, None]
    set_children(board.children[2].children[2], colours)

    # Level 4
    colours = [COLOUR_LIST[0], COLOUR_LIST[1], COLOUR_LIST[2], COLOUR_LIST[3]]
    set_children(board.children[2].children[2].children[0], colours)
    set_children(board.children[2].children[2].children[1], colours)
    set_children(board.children[2].children[2].children[2], colours)
    set_children(board.children[2].children[2].children[3], colours)
    set_children(board.children[3].children[0].children[0], colours)
    set_children(board.children[3].children[0].children[1], colours)
    set_children(board.children[3].children[0].children[2], colours)
    set_children(board.children[3].children[0].children[3], colours)
    set_children(board.children[3].children[1].children[0], colours)
    set_children(board.children[3].children[1].children[1], colours)
    set_children(board.children[3].children[1].children[2], colours)
    set_children(board.children[3].children[1].children[3], colours)
    set_children(board.children[3].children[2].children[0], colours)
    set_children(board.children[3].children[2].children[1], colours)
    set_children(board.children[3].children[2].children[2], colours)
    set_children(board.children[3].children[2].children[3], colours)
    set_children(board.children[3].children[3].children[0], colours)
    set_children(board.children[3].children[3].children[1], colours)
    set_children(board.children[3].children[3].children[2], colours)
    set_children(board.children[3].children[3].children[3], colours)

    return board


def board_actual_16x16_rotate() -> Block:
    # Level 0
    board = Block((0, 0), 1600, None, 0, 4)

    # Level 1
    colours = [None, None, None, COLOUR_LIST[0]]
    set_children(board, colours)

    # Level 2
    colours = [COLOUR_LIST[1], COLOUR_LIST[2], COLOUR_LIST[3], COLOUR_LIST[0]]
    set_children(board.children[0], colours)

    # Level 2
    colours = [None, None, COLOUR_LIST[3], None]
    set_children(board.children[1], colours)

    # Level 2
    colours = [None, None, None, None]
    set_children(board.children[2], colours)

    # Level 3
    colours = [None, None, None, None]
    set_children(board.children[2].children[0], colours)
    set_children(board.children[2].children[1], colours)
    set_children(board.children[2].children[2], colours)
    set_children(board.children[2].children[3], colours)

    colours = [COLOUR_LIST[1], COLOUR_LIST[2], COLOUR_LIST[3], COLOUR_LIST[0]]
    set_children(board.children[1].children[0], colours)
    set_children(board.children[1].children[3], colours)

    colours = [None, None, None, None]
    set_children(board.children[1].children[1], colours)

    # Level 4
    colours = [COLOUR_LIST[1], COLOUR_LIST[2], COLOUR_LIST[3], COLOUR_LIST[0]]
    set_children(board.children[1].children[1].children[0], colours)
    set_children(board.children[1].children[1].children[1], colours)
    set_children(board.children[1].children[1].children[2], colours)
    set_children(board.children[1].children[1].children[3], colours)
    set_children(board.children[2].children[0].children[0], colours)
    set_children(board.children[2].children[0].children[1], colours)
    set_children(board.children[2].children[0].children[2], colours)
    set_children(board.children[2].children[0].children[3], colours)
    set_children(board.children[2].children[1].children[0], colours)
    set_children(board.children[2].children[1].children[1], colours)
    set_children(board.children[2].children[1].children[2], colours)
    set_children(board.children[2].children[1].children[3], colours)
    set_children(board.children[2].children[2].children[0], colours)
    set_children(board.children[2].children[2].children[1], colours)
    set_children(board.children[2].children[2].children[2], colours)
    set_children(board.children[2].children[2].children[3], colours)
    set_children(board.children[2].children[3].children[0], colours)
    set_children(board.children[2].children[3].children[1], colours)
    set_children(board.children[2].children[3].children[2], colours)
    set_children(board.children[2].children[3].children[3], colours)

    return board


def board_16x16_actual_example_swap_all_vertical() -> Block:
    # Level 0
    board = Block((0, 0), 1600, None, 0, 4)

    # Level 1
    colours = [None, None, None, COLOUR_LIST[0]]
    set_children(board, colours)

    # Level 2
    colours = [COLOUR_LIST[0], COLOUR_LIST[1], COLOUR_LIST[2], COLOUR_LIST[3]]
    set_children(board.children[2], colours)

    # Level 2
    colours = [None, None, None, COLOUR_LIST[3]]
    set_children(board.children[1], colours)

    # Level 2
    colours = [None, None, None, None]
    set_children(board.children[0], colours)

    # Level 3
    colours = [None, None, None, None]
    set_children(board.children[0].children[0], colours)
    set_children(board.children[0].children[1], colours)
    set_children(board.children[0].children[2], colours)
    set_children(board.children[0].children[3], colours)

    colours = [COLOUR_LIST[0], COLOUR_LIST[1], COLOUR_LIST[2], COLOUR_LIST[3]]
    set_children(board.children[1].children[0], colours)
    set_children(board.children[1].children[1], colours)

    colours = [None, None, None, None]
    set_children(board.children[1].children[2], colours)

    # Level 4
    colours = [COLOUR_LIST[0], COLOUR_LIST[1], COLOUR_LIST[2], COLOUR_LIST[3]]
    set_children(board.children[1].children[2].children[0], colours)
    set_children(board.children[1].children[2].children[1], colours)
    set_children(board.children[1].children[2].children[2], colours)
    set_children(board.children[1].children[2].children[3], colours)
    set_children(board.children[0].children[0].children[0], colours)
    set_children(board.children[0].children[0].children[1], colours)
    set_children(board.children[0].children[0].children[2], colours)
    set_children(board.children[0].children[0].children[3], colours)
    set_children(board.children[0].children[1].children[0], colours)
    set_children(board.children[0].children[1].children[1], colours)
    set_children(board.children[0].children[1].children[2], colours)
    set_children(board.children[0].children[1].children[3], colours)
    set_children(board.children[0].children[2].children[0], colours)
    set_children(board.children[0].children[2].children[1], colours)
    set_children(board.children[0].children[2].children[2], colours)
    set_children(board.children[0].children[2].children[3], colours)
    set_children(board.children[0].children[3].children[0], colours)
    set_children(board.children[0].children[3].children[1], colours)
    set_children(board.children[0].children[3].children[2], colours)
    set_children(board.children[0].children[3].children[3], colours)

    return board


def board_actual_16x16_swap_all_horizontal() -> Block:
    # Level 0
    board = Block((0, 0), 1600, None, 0, 4)

    # Level 1
    colours = [None, COLOUR_LIST[0], None, None]
    set_children(board, colours)

    # Level 2
    colours = [COLOUR_LIST[0], COLOUR_LIST[1], COLOUR_LIST[2], COLOUR_LIST[3]]
    set_children(board.children[0], colours)

    # Level 2
    colours = [None, None, None, COLOUR_LIST[3]]
    set_children(board.children[3], colours)

    # Level 2
    colours = [None, None, None, None]
    set_children(board.children[2], colours)

    # Level 3
    colours = [None, None, None, None]
    set_children(board.children[2].children[0], colours)
    set_children(board.children[2].children[1], colours)
    set_children(board.children[2].children[2], colours)
    set_children(board.children[2].children[3], colours)

    colours = [COLOUR_LIST[0], COLOUR_LIST[1], COLOUR_LIST[2], COLOUR_LIST[3]]
    set_children(board.children[3].children[0], colours)
    set_children(board.children[3].children[1], colours)

    colours = [None, None, None, None]
    set_children(board.children[3].children[2], colours)

    # Level 4
    colours = [COLOUR_LIST[0], COLOUR_LIST[1], COLOUR_LIST[2], COLOUR_LIST[3]]
    set_children(board.children[3].children[2].children[0], colours)
    set_children(board.children[3].children[2].children[1], colours)
    set_children(board.children[3].children[2].children[2], colours)
    set_children(board.children[3].children[2].children[3], colours)
    set_children(board.children[2].children[0].children[0], colours)
    set_children(board.children[2].children[0].children[1], colours)
    set_children(board.children[2].children[0].children[2], colours)
    set_children(board.children[2].children[0].children[3], colours)
    set_children(board.children[2].children[1].children[0], colours)
    set_children(board.children[2].children[1].children[1], colours)
    set_children(board.children[2].children[1].children[2], colours)
    set_children(board.children[2].children[1].children[3], colours)
    set_children(board.children[2].children[2].children[0], colours)
    set_children(board.children[2].children[2].children[1], colours)
    set_children(board.children[2].children[2].children[2], colours)
    set_children(board.children[2].children[2].children[3], colours)
    set_children(board.children[2].children[3].children[0], colours)
    set_children(board.children[2].children[3].children[1], colours)
    set_children(board.children[2].children[3].children[2], colours)
    set_children(board.children[2].children[3].children[3], colours)

    return board


def board_16x16_swap_children_horizontal() -> Block:
    # Level 0
    board = Block((0, 0), 1600, None, 0, 4)

    # Level 1
    colours = [COLOUR_LIST[0], None, None, None]
    set_children(board, colours)

    # Level 2
    colours = [COLOUR_LIST[0], COLOUR_LIST[1], COLOUR_LIST[2], COLOUR_LIST[3]]
    set_children(board.children[1], colours)

    # Level 2
    colours = [None, None, COLOUR_LIST[3], None]
    set_children(board.children[2], colours)

    # Level 2
    colours = [None, None, None, None]
    set_children(board.children[3], colours)

    # Level 3
    colours = [None, None, None, None]
    set_children(board.children[3].children[0], colours)
    set_children(board.children[3].children[1], colours)
    set_children(board.children[3].children[2], colours)
    set_children(board.children[3].children[3], colours)

    colours = [COLOUR_LIST[0], COLOUR_LIST[1], COLOUR_LIST[2], COLOUR_LIST[3]]
    set_children(board.children[2].children[0], colours)
    set_children(board.children[2].children[1], colours)

    colours = [None, None, None, None]
    set_children(board.children[2].children[3], colours)

    # Level 4
    colours = [COLOUR_LIST[0], COLOUR_LIST[1], COLOUR_LIST[2], COLOUR_LIST[3]]
    set_children(board.children[2].children[3].children[0], colours)
    set_children(board.children[2].children[3].children[1], colours)
    set_children(board.children[2].children[3].children[2], colours)
    set_children(board.children[2].children[3].children[3], colours)
    set_children(board.children[3].children[0].children[0], colours)
    set_children(board.children[3].children[0].children[1], colours)
    set_children(board.children[3].children[0].children[2], colours)
    set_children(board.children[3].children[0].children[3], colours)
    set_children(board.children[3].children[1].children[0], colours)
    set_children(board.children[3].children[1].children[1], colours)
    set_children(board.children[3].children[1].children[2], colours)
    set_children(board.children[3].children[1].children[3], colours)
    set_children(board.children[3].children[2].children[0], colours)
    set_children(board.children[3].children[2].children[1], colours)
    set_children(board.children[3].children[2].children[2], colours)
    set_children(board.children[3].children[2].children[3], colours)
    set_children(board.children[3].children[3].children[0], colours)
    set_children(board.children[3].children[3].children[1], colours)
    set_children(board.children[3].children[3].children[2], colours)
    set_children(board.children[3].children[3].children[3], colours)

    return board


def board_16x16_swap_children_vertical() -> Block:
    # Level 0
    board = Block((0, 0), 1600, None, 0, 4)

    # Level 1
    colours = [COLOUR_LIST[0], None, None, None]
    set_children(board, colours)

    # Level 2
    colours = [COLOUR_LIST[0], COLOUR_LIST[1], COLOUR_LIST[2], COLOUR_LIST[3]]
    set_children(board.children[1], colours)

    # Level 2
    colours = [COLOUR_LIST[3], None, None, None]
    set_children(board.children[2], colours)

    # Level 2
    colours = [None, None, None, None]
    set_children(board.children[3], colours)

    # Level 3
    colours = [None, None, None, None]
    set_children(board.children[3].children[0], colours)
    set_children(board.children[3].children[1], colours)
    set_children(board.children[3].children[2], colours)
    set_children(board.children[3].children[3], colours)

    colours = [COLOUR_LIST[0], COLOUR_LIST[1], COLOUR_LIST[2], COLOUR_LIST[3]]
    set_children(board.children[2].children[2], colours)
    set_children(board.children[2].children[3], colours)

    colours = [None, None, None, None]
    set_children(board.children[2].children[1], colours)

    # Level 4
    colours = [COLOUR_LIST[0], COLOUR_LIST[1], COLOUR_LIST[2], COLOUR_LIST[3]]
    set_children(board.children[2].children[1].children[0], colours)
    set_children(board.children[2].children[1].children[1], colours)
    set_children(board.children[2].children[1].children[2], colours)
    set_children(board.children[2].children[1].children[3], colours)
    set_children(board.children[3].children[0].children[0], colours)
    set_children(board.children[3].children[0].children[1], colours)
    set_children(board.children[3].children[0].children[2], colours)
    set_children(board.children[3].children[0].children[3], colours)
    set_children(board.children[3].children[1].children[0], colours)
    set_children(board.children[3].children[1].children[1], colours)
    set_children(board.children[3].children[1].children[2], colours)
    set_children(board.children[3].children[1].children[3], colours)
    set_children(board.children[3].children[2].children[0], colours)
    set_children(board.children[3].children[2].children[1], colours)
    set_children(board.children[3].children[2].children[2], colours)
    set_children(board.children[3].children[2].children[3], colours)
    set_children(board.children[3].children[3].children[0], colours)
    set_children(board.children[3].children[3].children[1], colours)
    set_children(board.children[3].children[3].children[2], colours)
    set_children(board.children[3].children[3].children[3], colours)

    return board


def flattened_board_1x1() -> List[List[Tuple[int, int, int]]]:
    """Create a list of the unit cells inside the reference board."""
    return [
        [COLOUR_LIST[1]]
    ]


def flattened_board_2x2() -> List[List[Tuple[int, int, int]]]:
    """Create a list of the unit cells inside the reference board."""
    return [
        [COLOUR_LIST[2], COLOUR_LIST[1]],
        [COLOUR_LIST[0], COLOUR_LIST[3]]
    ]


def flattened_board_8x8() -> List[List[Tuple[int, int, int]]]:
    """Create a list of the unit cells inside the reference board."""
    return [
        [COLOUR_LIST[1], COLOUR_LIST[2], COLOUR_LIST[1], COLOUR_LIST[2], COLOUR_LIST[3], COLOUR_LIST[3], COLOUR_LIST[3], COLOUR_LIST[3]],
        [COLOUR_LIST[0], COLOUR_LIST[3], COLOUR_LIST[0], COLOUR_LIST[3], COLOUR_LIST[3], COLOUR_LIST[3], COLOUR_LIST[3], COLOUR_LIST[3]],
        [COLOUR_LIST[1], COLOUR_LIST[2], COLOUR_LIST[1], COLOUR_LIST[2], COLOUR_LIST[3], COLOUR_LIST[3], COLOUR_LIST[3], COLOUR_LIST[3]],
        [COLOUR_LIST[0], COLOUR_LIST[3], COLOUR_LIST[0], COLOUR_LIST[3], COLOUR_LIST[3], COLOUR_LIST[3], COLOUR_LIST[3], COLOUR_LIST[3]],
        [COLOUR_LIST[1], COLOUR_LIST[1], COLOUR_LIST[2], COLOUR_LIST[2], COLOUR_LIST[1], COLOUR_LIST[1], COLOUR_LIST[1], COLOUR_LIST[2]],
        [COLOUR_LIST[1], COLOUR_LIST[1], COLOUR_LIST[2], COLOUR_LIST[2], COLOUR_LIST[1], COLOUR_LIST[1], COLOUR_LIST[0], COLOUR_LIST[3]],
        [COLOUR_LIST[0], COLOUR_LIST[0], COLOUR_LIST[3], COLOUR_LIST[3], COLOUR_LIST[0], COLOUR_LIST[0], COLOUR_LIST[3], COLOUR_LIST[3]],
        [COLOUR_LIST[0], COLOUR_LIST[0], COLOUR_LIST[3], COLOUR_LIST[3], COLOUR_LIST[0], COLOUR_LIST[0], COLOUR_LIST[3], COLOUR_LIST[3]]
    ]


def flattened_board_actual_16x16() -> List[List[Tuple[int, int, int]]]:
    """Create a list of the unit cells inside the reference board."""
    return [
        [COLOUR_LIST[1], COLOUR_LIST[1], COLOUR_LIST[1], COLOUR_LIST[1], COLOUR_LIST[2], COLOUR_LIST[2], COLOUR_LIST[2], COLOUR_LIST[2],
         COLOUR_LIST[1], COLOUR_LIST[1], COLOUR_LIST[2], COLOUR_LIST[2], COLOUR_LIST[1], COLOUR_LIST[2], COLOUR_LIST[1], COLOUR_LIST[2]],
        [COLOUR_LIST[1], COLOUR_LIST[1], COLOUR_LIST[1], COLOUR_LIST[1], COLOUR_LIST[2], COLOUR_LIST[2], COLOUR_LIST[2], COLOUR_LIST[2],
         COLOUR_LIST[1], COLOUR_LIST[1], COLOUR_LIST[2], COLOUR_LIST[2], COLOUR_LIST[0], COLOUR_LIST[3], COLOUR_LIST[0], COLOUR_LIST[3]],
        [COLOUR_LIST[1], COLOUR_LIST[1], COLOUR_LIST[1], COLOUR_LIST[1], COLOUR_LIST[2], COLOUR_LIST[2], COLOUR_LIST[2], COLOUR_LIST[2],
         COLOUR_LIST[0], COLOUR_LIST[0], COLOUR_LIST[3], COLOUR_LIST[3], COLOUR_LIST[1], COLOUR_LIST[2], COLOUR_LIST[1], COLOUR_LIST[2]],
        [COLOUR_LIST[1], COLOUR_LIST[1], COLOUR_LIST[1], COLOUR_LIST[1], COLOUR_LIST[2], COLOUR_LIST[2], COLOUR_LIST[2], COLOUR_LIST[2],
         COLOUR_LIST[0], COLOUR_LIST[0], COLOUR_LIST[3], COLOUR_LIST[3], COLOUR_LIST[0], COLOUR_LIST[3], COLOUR_LIST[0], COLOUR_LIST[3]],
        [COLOUR_LIST[0], COLOUR_LIST[0], COLOUR_LIST[0], COLOUR_LIST[0], COLOUR_LIST[3], COLOUR_LIST[3], COLOUR_LIST[3], COLOUR_LIST[3],
         COLOUR_LIST[1], COLOUR_LIST[1], COLOUR_LIST[2], COLOUR_LIST[2], COLOUR_LIST[3], COLOUR_LIST[3], COLOUR_LIST[3], COLOUR_LIST[3]],
        [COLOUR_LIST[0], COLOUR_LIST[0], COLOUR_LIST[0], COLOUR_LIST[0], COLOUR_LIST[3], COLOUR_LIST[3], COLOUR_LIST[3], COLOUR_LIST[3],
         COLOUR_LIST[1], COLOUR_LIST[1], COLOUR_LIST[2], COLOUR_LIST[2], COLOUR_LIST[3], COLOUR_LIST[3], COLOUR_LIST[3], COLOUR_LIST[3]],
        [COLOUR_LIST[0], COLOUR_LIST[0], COLOUR_LIST[0], COLOUR_LIST[0], COLOUR_LIST[3], COLOUR_LIST[3], COLOUR_LIST[3], COLOUR_LIST[3],
         COLOUR_LIST[0], COLOUR_LIST[0], COLOUR_LIST[3], COLOUR_LIST[3], COLOUR_LIST[3], COLOUR_LIST[3], COLOUR_LIST[3], COLOUR_LIST[3]],
        [COLOUR_LIST[0], COLOUR_LIST[0], COLOUR_LIST[0], COLOUR_LIST[0], COLOUR_LIST[3], COLOUR_LIST[3], COLOUR_LIST[3], COLOUR_LIST[3],
         COLOUR_LIST[0], COLOUR_LIST[0], COLOUR_LIST[3], COLOUR_LIST[3], COLOUR_LIST[3], COLOUR_LIST[3], COLOUR_LIST[3], COLOUR_LIST[3]],
        [COLOUR_LIST[0], COLOUR_LIST[0], COLOUR_LIST[0], COLOUR_LIST[0], COLOUR_LIST[0], COLOUR_LIST[0], COLOUR_LIST[0], COLOUR_LIST[0],
         COLOUR_LIST[1], COLOUR_LIST[2], COLOUR_LIST[1], COLOUR_LIST[2], COLOUR_LIST[1], COLOUR_LIST[2], COLOUR_LIST[1], COLOUR_LIST[2]],
        [COLOUR_LIST[0], COLOUR_LIST[0], COLOUR_LIST[0], COLOUR_LIST[0], COLOUR_LIST[0], COLOUR_LIST[0], COLOUR_LIST[0], COLOUR_LIST[0],
         COLOUR_LIST[0], COLOUR_LIST[3], COLOUR_LIST[0], COLOUR_LIST[3], COLOUR_LIST[0], COLOUR_LIST[3], COLOUR_LIST[0], COLOUR_LIST[3]],
        [COLOUR_LIST[0], COLOUR_LIST[0], COLOUR_LIST[0], COLOUR_LIST[0], COLOUR_LIST[0], COLOUR_LIST[0], COLOUR_LIST[0], COLOUR_LIST[0],
         COLOUR_LIST[1], COLOUR_LIST[2], COLOUR_LIST[1], COLOUR_LIST[2], COLOUR_LIST[1], COLOUR_LIST[2], COLOUR_LIST[1], COLOUR_LIST[2]],
        [COLOUR_LIST[0], COLOUR_LIST[0], COLOUR_LIST[0], COLOUR_LIST[0], COLOUR_LIST[0], COLOUR_LIST[0], COLOUR_LIST[0], COLOUR_LIST[0],
         COLOUR_LIST[0], COLOUR_LIST[3], COLOUR_LIST[0], COLOUR_LIST[3], COLOUR_LIST[0], COLOUR_LIST[3], COLOUR_LIST[0], COLOUR_LIST[3]],
        [COLOUR_LIST[0], COLOUR_LIST[0], COLOUR_LIST[0], COLOUR_LIST[0], COLOUR_LIST[0], COLOUR_LIST[0], COLOUR_LIST[0], COLOUR_LIST[0],
         COLOUR_LIST[1], COLOUR_LIST[2], COLOUR_LIST[1], COLOUR_LIST[2], COLOUR_LIST[1], COLOUR_LIST[2], COLOUR_LIST[1], COLOUR_LIST[2]],
        [COLOUR_LIST[0], COLOUR_LIST[0], COLOUR_LIST[0], COLOUR_LIST[0], COLOUR_LIST[0], COLOUR_LIST[0], COLOUR_LIST[0], COLOUR_LIST[0],
         COLOUR_LIST[0], COLOUR_LIST[3], COLOUR_LIST[0], COLOUR_LIST[3], COLOUR_LIST[0], COLOUR_LIST[3], COLOUR_LIST[0], COLOUR_LIST[3]],
        [COLOUR_LIST[0], COLOUR_LIST[0], COLOUR_LIST[0], COLOUR_LIST[0], COLOUR_LIST[0], COLOUR_LIST[0], COLOUR_LIST[0], COLOUR_LIST[0],
         COLOUR_LIST[1], COLOUR_LIST[2], COLOUR_LIST[1], COLOUR_LIST[2], COLOUR_LIST[1], COLOUR_LIST[2], COLOUR_LIST[1], COLOUR_LIST[2]],
        [COLOUR_LIST[0], COLOUR_LIST[0], COLOUR_LIST[0], COLOUR_LIST[0], COLOUR_LIST[0], COLOUR_LIST[0], COLOUR_LIST[0], COLOUR_LIST[0],
         COLOUR_LIST[0], COLOUR_LIST[3], COLOUR_LIST[0], COLOUR_LIST[3], COLOUR_LIST[0], COLOUR_LIST[3], COLOUR_LIST[0], COLOUR_LIST[3]]
    ]


def test_block_to_square_1_by_1() -> None:
    board1 = board_one_by_one()
    assert _block_to_squares(board1) == [((199, 44, 58), (0, 0), 750)]


def test_block_to_square_2_by_2() -> None:
    board1 = board_2x2()
    assert set(_block_to_squares(board1)) == {((1, 128, 181), (375, 0), 375),
                                         ((138, 151, 71), (0, 0), 375),
                                         ((199, 44, 58), (0, 375), 375),
                                         ((255, 211, 92), (375, 375), 375)
                                         }


def test_block_to_squares_16_by_16_example_1() -> None:
    """Test that the reference board can be correctly translated into a set of
    squares that would be rendered onto the screen.
    """
    # The order the squares appear may differ based on the implementation, so
    # we use a set here.gh
    new_board = board_16x16_example_1()
    assert set(_block_to_squares(new_board)) == {((199, 44, 58), (0, 0), 188),
                                                 ((199, 44, 58), (0, 188), 188),
                                                 ((255, 211, 92), (188, 188), 188),
                                                 ((1, 128, 181), (188, 0), 188),
                                                 ((199, 44, 58), (0, 375), 375),
                                                 ((138, 151, 71), (375, 0), 375),
                                                 ((255, 211, 92), (375, 375), 375)
                                                 }


def test_block_to_squares_16_by_16_example_2() -> None:
    """Test that the reference board can be correctly translated into a set of
    squares that would be rendered onto the screen.
    """
    # The order the squares appear may differ based on the implementation, so
    # we use a set here.
    new_board = board_16x16_example_2()
    assert set(_block_to_squares(new_board)) == {(COLOUR_LIST[2], (375, 0), 375),
                                                 (COLOUR_LIST[1], (0, 0), 375),
                                                 (COLOUR_LIST[3], (375, 375), 375),
                                                 (COLOUR_LIST[0], (188, 375), 188),
                                                 (COLOUR_LIST[1], (0, 375), 188),
                                                 (COLOUR_LIST[1], (0, 563), 188),
                                                 (COLOUR_LIST[3], (188, 563), 188)
                                                 }


def test_block_to_squares_16_by_16_example_3() -> None:
    """Test that the reference board can be correctly translated into a set of
    squares that would be rendered onto the screen.
    """
    # The order the squares appear may differ based on the implementation, so
    # we use a set here.
    new_board = board_16x16_example_3()
    assert set(_block_to_squares(new_board)) == {((199, 44, 58), (375, 375), 188),
                                                 ((199, 44, 58), (375, 563), 188),
                                                 ((255, 211, 92), (563, 563), 188),
                                                 ((1, 128, 181), (563, 375), 188),
                                                 ((199, 44, 58), (0, 0), 375),
                                                 ((138, 151, 71), (375, 0), 375),
                                                 ((255, 211, 92), (0, 375), 375)
                                                 }


def test_block_to_squares_8_by_8_example_1() -> None:
    """Test that the reference board can be correctly translated into a set of
    squares that would be rendered onto the screen.
    """
    # The order the squares appear may differ based on the implementation, so
    # we use a set here.
    new_board = board_8x8_example()
    assert set(_block_to_squares(new_board)) == {(COLOUR_LIST[0], (100, 0), 100),
                                                 (COLOUR_LIST[1], (0, 0), 100),
                                                 (COLOUR_LIST[2], (0, 100), 100),
                                                 (COLOUR_LIST[3], (100, 100), 100),
                                                 (COLOUR_LIST[0], (300, 0), 100),
                                                 (COLOUR_LIST[1], (200, 0), 100),
                                                 (COLOUR_LIST[2], (200, 100), 100),
                                                 (COLOUR_LIST[3], (300, 100), 100),
                                                 (COLOUR_LIST[0], (100, 200), 100),
                                                 (COLOUR_LIST[1], (0, 200), 100),
                                                 (COLOUR_LIST[2], (0, 300), 100),
                                                 (COLOUR_LIST[3], (100, 300), 100),
                                                 (COLOUR_LIST[0], (300, 200), 100),
                                                 (COLOUR_LIST[1], (200, 200), 100),
                                                 (COLOUR_LIST[2], (200, 300), 100),
                                                 (COLOUR_LIST[3], (300, 300), 100),
                                                 (COLOUR_LIST[0], (600, 0), 200),
                                                 (COLOUR_LIST[1], (400, 0), 200),
                                                 (COLOUR_LIST[2], (400, 200), 200),
                                                 (COLOUR_LIST[3], (600, 200), 200),
                                                 (COLOUR_LIST[3], (0, 400), 400),
                                                 (COLOUR_LIST[0], (600, 400), 200),
                                                 (COLOUR_LIST[1], (400, 400), 200),
                                                 (COLOUR_LIST[3], (600, 600), 200),
                                                 (COLOUR_LIST[0], (500, 600), 100),
                                                 (COLOUR_LIST[1], (400, 600), 100),
                                                 (COLOUR_LIST[2], (400, 700), 100),
                                                 (COLOUR_LIST[3], (500, 700), 100)
                                                 }


def test_actual_16x16() -> None:
    new_board = board_16x16_actual_example()
    assert set(_block_to_squares(new_board)) == {(COLOUR_LIST[0], (800, 0), 800),
                                                 (COLOUR_LIST[0], (400, 0), 400),
                                                 (COLOUR_LIST[1], (0, 0), 400),
                                                 (COLOUR_LIST[2], (0, 400), 400),
                                                 (COLOUR_LIST[3], (400, 400), 400),
                                                 (COLOUR_LIST[0], (1500, 800), 100),
                                                 (COLOUR_LIST[1], (1400, 800), 100),
                                                 (COLOUR_LIST[2], (1400, 900), 100),
                                                 (COLOUR_LIST[3], (1500, 900), 100),
                                                 (COLOUR_LIST[0], (1300, 800), 100),
                                                 (COLOUR_LIST[1], (1200, 800), 100),
                                                 (COLOUR_LIST[2], (1200, 900), 100),
                                                 (COLOUR_LIST[3], (1300, 900), 100),
                                                 (COLOUR_LIST[0], (1500, 1000), 100),
                                                 (COLOUR_LIST[1], (1400, 1000), 100),
                                                 (COLOUR_LIST[2], (1400, 1100), 100),
                                                 (COLOUR_LIST[3], (1500, 1100), 100),
                                                 (COLOUR_LIST[0], (1300, 1000), 100),
                                                 (COLOUR_LIST[1], (1200, 1000), 100),
                                                 (COLOUR_LIST[2], (1200, 1100), 100),
                                                 (COLOUR_LIST[3], (1300, 1100), 100),
                                                 (COLOUR_LIST[0], (1500, 1200), 100),
                                                 (COLOUR_LIST[1], (1400, 1200), 100),
                                                 (COLOUR_LIST[2], (1400, 1300), 100),
                                                 (COLOUR_LIST[3], (1500, 1300), 100),
                                                 (COLOUR_LIST[0], (1300, 1200), 100),
                                                 (COLOUR_LIST[1], (1200, 1200), 100),
                                                 (COLOUR_LIST[2], (1200, 1300), 100),
                                                 (COLOUR_LIST[3], (1300, 1300), 100),
                                                 (COLOUR_LIST[0], (1500, 1400), 100),
                                                 (COLOUR_LIST[1], (1400, 1400), 100),
                                                 (COLOUR_LIST[2], (1400, 1500), 100),
                                                 (COLOUR_LIST[3], (1500, 1500), 100),
                                                 (COLOUR_LIST[0], (1300, 1400), 100),
                                                 (COLOUR_LIST[1], (1200, 1400), 100),
                                                 (COLOUR_LIST[2], (1200, 1500), 100),
                                                 (COLOUR_LIST[3], (1300, 1500), 100),
                                                 (COLOUR_LIST[0], (1100, 800), 100),
                                                 (COLOUR_LIST[1], (1000, 800), 100),
                                                 (COLOUR_LIST[2], (1000, 900), 100),
                                                 (COLOUR_LIST[3], (1100, 900), 100),
                                                 (COLOUR_LIST[0], (900, 800), 100),
                                                 (COLOUR_LIST[1], (800, 800), 100),
                                                 (COLOUR_LIST[2], (800, 900), 100),
                                                 (COLOUR_LIST[3], (900, 900), 100),
                                                 (COLOUR_LIST[0], (1100, 1000), 100),
                                                 (COLOUR_LIST[1], (1000, 1000), 100),
                                                 (COLOUR_LIST[2], (1000, 1100), 100),
                                                 (COLOUR_LIST[3], (1100, 1100), 100),
                                                 (COLOUR_LIST[0], (900, 1000), 100),
                                                 (COLOUR_LIST[1], (800, 1000), 100),
                                                 (COLOUR_LIST[2], (800, 1100), 100),
                                                 (COLOUR_LIST[3], (900, 1100), 100),
                                                 (COLOUR_LIST[0], (1100, 1200), 100),
                                                 (COLOUR_LIST[1], (1000, 1200), 100),
                                                 (COLOUR_LIST[2], (1000, 1300), 100),
                                                 (COLOUR_LIST[3], (1100, 1300), 100),
                                                 (COLOUR_LIST[0], (900, 1200), 100),
                                                 (COLOUR_LIST[1], (800, 1200), 100),
                                                 (COLOUR_LIST[2], (800, 1300), 100),
                                                 (COLOUR_LIST[3], (900, 1300), 100),
                                                 (COLOUR_LIST[0], (1100, 1400), 100),
                                                 (COLOUR_LIST[1], (1000, 1400), 100),
                                                 (COLOUR_LIST[2], (1000, 1500), 100),
                                                 (COLOUR_LIST[3], (1100, 1500), 100),
                                                 (COLOUR_LIST[0], (900, 1400), 100),
                                                 (COLOUR_LIST[1], (800, 1400), 100),
                                                 (COLOUR_LIST[2], (800, 1500), 100),
                                                 (COLOUR_LIST[3], (900, 1500), 100),
                                                 (COLOUR_LIST[0], (600, 800), 200),
                                                 (COLOUR_LIST[1], (400, 800), 200),
                                                 (COLOUR_LIST[2], (400, 1000), 200),
                                                 (COLOUR_LIST[3], (600, 1000), 200),
                                                 (COLOUR_LIST[0], (200, 800), 200),
                                                 (COLOUR_LIST[1], (0, 800), 200),
                                                 (COLOUR_LIST[2], (0, 1000), 200),
                                                 (COLOUR_LIST[3], (200, 1000), 200),
                                                 (COLOUR_LIST[3], (400, 1200), 400),
                                                 (COLOUR_LIST[0], (300, 1200), 100),
                                                 (COLOUR_LIST[1], (200, 1200), 100),
                                                 (COLOUR_LIST[2], (200, 1300), 100),
                                                 (COLOUR_LIST[3], (300, 1300), 100),
                                                 (COLOUR_LIST[0], (300, 1400), 100),
                                                 (COLOUR_LIST[1], (200, 1400), 100),
                                                 (COLOUR_LIST[2], (200, 1500), 100),
                                                 (COLOUR_LIST[3], (300, 1500), 100),
                                                 (COLOUR_LIST[0], (100, 1200), 100),
                                                 (COLOUR_LIST[1], (0, 1200), 100),
                                                 (COLOUR_LIST[2], (0, 1300), 100),
                                                 (COLOUR_LIST[3], (100, 1300), 100),
                                                 (COLOUR_LIST[0], (100, 1400), 100),
                                                 (COLOUR_LIST[1], (0, 1400), 100),
                                                 (COLOUR_LIST[2], (0, 1500), 100),
                                                 (COLOUR_LIST[3], (100, 1500), 100),
                                                 }


def test_smash_example() -> None:
    block = board_16x16_actual_example().children[0]
    assert block.smash() is True


def test_generate_goals() -> None:
    all_goals = generate_goals(4)
    type_1 = type(all_goals[0])
    type_2 = type(all_goals[1])
    type_3 = type(all_goals[2])
    type_4 = type(all_goals[3])
    color_1 = all_goals[0].colour
    color_2 = all_goals[1].colour
    color_3 = all_goals[2].colour
    color_4 = all_goals[3].colour
    assert len(all_goals) == 4
    assert type_1 == type_2 and type_2 == type_3 and type_3 == type_4 and type_1 == type_4
    assert color_1 != color_2 and color_1 != color_3 and color_1 != color_4 and \
           color_2 != color_3 and color_2 != color_4 and color_3 != color_4


def test_create_players() -> None:
    all_players = create_players(1, 1, [2, 4])
    assert len(all_players) == 4
    assert all_players[0].id == 0
    assert all_players[1].id == 1
    assert all_players[2].id == 2
    assert all_players[3].id == 3
    assert all_players[2]._difficulty == 2
    assert all_players[3]._difficulty == 4


def test_get_block_1x1() -> None:
    block = board_one_by_one()
    assert _get_block(block, (0, 0), 0) == block
    assert _get_block(block, (750, 0), 0) is None
    assert _get_block(block, (0, 750), 0) is None
    assert _get_block(block, (750, 750), 0) is None
    assert _get_block(block, (750, 0), 0) is None
    assert _get_block(block, (750, 37), 0) is None
    assert _get_block(block, (78, 750), 0) is None
    assert _get_block(block, (42, 730), 0) == block
    assert _get_block(block, (42, 370), 1) == block


def test_get_block_2x2() -> None:
    block = board_2x2()
    assert _get_block(block, (0, 0), 0) == block
    assert _get_block(block, (0, 0), 1) == block.children[1]
    assert _get_block(block, (0, 0), 2) == block.children[1]
    assert _get_block(block, (375, 0), 1) == block.children[0]
    assert _get_block(block, (375, 0), 0) == block
    assert _get_block(block, (750, 0), 0) is None
    assert _get_block(block, (750, 0), 1) is None
    assert _get_block(block, (749, 0), 0) == block
    assert _get_block(block, (749, 0), 1) == block.children[0]
    assert _get_block(block, (375, 0), 0) == block
    assert _get_block(block, (0, 375), 1) == block.children[2]
    assert _get_block(block, (0, 375), 2) == block.children[2]
    assert _get_block(block, (750, 0), 0) is None
    assert _get_block(block, (750, 0), 1) is None
    assert _get_block(block, (750, 0), 2) is None
    assert _get_block(block, (343, 730), 2) == block.children[2]
    assert _get_block(block, (343, 730), 1) == block.children[2]
    assert _get_block(block, (343, 730), 0) == block
    assert _get_block(block, (750, 4), 1) is None
    assert _get_block(block, (375, 750), 1) is None
    assert _get_block(block, (750, 750), 2) is None
    assert _get_block(block, (375, 375), 1) == block.children[3]
    assert _get_block(block, (375, 380), 1) == block.children[3]
    assert _get_block(block, (390, 375), 1) == block.children[3]
    assert _get_block(block, (390, 380), 1) == block.children[3]
    assert _get_block(block, (750, 375), 1) is None
    assert _get_block(block, (750, 375), 0) is None
    assert _get_block(block, (375, 375), 0) == block


def test_block_fake_16x16() -> None:
    block = board_16x16()
    assert _get_block(block, (0, 0), 0) == block
    assert _get_block(block, (0, 0), 1) == block.children[1]
    assert _get_block(block, (375, 0), 0) == block
    assert _get_block(block, (375, 0), 1) == block.children[0]
    assert _get_block(block, (375, 0), 2) == block.children[0].children[1]
    assert _get_block(block, (375, 0), 3) == block.children[0].children[1]
    assert _get_block(block, (563, 0), 0) == block
    assert _get_block(block, (563, 0), 1) == block.children[0]
    assert _get_block(block, (563, 0), 2) == block.children[0].children[0]
    assert _get_block(block, (750, 0), 0) is None
    assert _get_block(block, (750, 0), 1) is None
    assert _get_block(block, (750, 0), 2) is None
    assert _get_block(block, (749, 0), 0) == block
    assert _get_block(block, (749, 0), 1) == block.children[0]
    assert _get_block(block, (749, 0), 2) == block.children[0].children[0]
    assert _get_block(block, (749, 100), 0) == block
    assert _get_block(block, (749, 125), 1) == block.children[0]
    assert _get_block(block, (749, 1), 2) == block.children[0].children[0]
    assert _get_block(block, (375, 1), 0) == block
    assert _get_block(block, (375, 22), 1) == block.children[0]
    assert _get_block(block, (375, 33), 2) == block.children[0].children[1]
    assert _get_block(block, (375, 100), 3) == block.children[0].children[1]
    assert _get_block(block, (563, 4), 0) == block
    assert _get_block(block, (563, 9), 1) == block.children[0]
    assert _get_block(block, (563, 2), 2) == block.children[0].children[0]
    assert _get_block(block, (750, 180), 0) is None
    assert _get_block(block, (750, 150), 1) is None
    assert _get_block(block, (750, 5), 2) is None
    assert _get_block(block, (375, 188), 0) == block
    assert _get_block(block, (375, 188), 1) == block.children[0]
    assert _get_block(block, (375, 188), 2) == block.children[0].children[2]
    assert _get_block(block, (563, 188), 0) == block
    assert _get_block(block, (563, 188), 1) == block.children[0]
    assert _get_block(block, (563, 188), 2) == block.children[0].children[3]
    assert _get_block(block, (750, 188), 0) is None
    assert _get_block(block, (750, 188), 1) is None
    assert _get_block(block, (750, 188), 2) is None
    assert _get_block(block, (375, 375), 0) == block
    assert _get_block(block, (375, 375), 1) == block.children[3]
    assert _get_block(block, (375, 375), 2) == block.children[3]
    assert _get_block(block, (563, 375), 0) == block
    assert _get_block(block, (563, 375), 1) == block.children[3]
    assert _get_block(block, (563, 375), 2) == block.children[3]
    assert _get_block(block, (750, 365), 0) is None
    assert _get_block(block, (750, 365), 1) is None
    assert _get_block(block, (750, 365), 2) is None
    assert _get_block(block, (750, 765), 0) is None


def test_actual_16x16_get_block() -> None:
    block = board_16x16_actual_example()
    assert _get_block(block, (800, 0), 0) == block
    assert _get_block(block, (800, 0), 1) == block.children[0]
    assert _get_block(block, (800, 0), 2) == block.children[0]
    assert _get_block(block, (1600, 0), 0) is None
    assert _get_block(block, (1600, 0), 1) is None
    assert _get_block(block, (0, 0), 0) == block
    assert _get_block(block, (0, 0), 1) == block.children[1]
    assert _get_block(block, (0, 0), 2) == block.children[1].children[1]
    assert _get_block(block, (400, 800), 0) == block
    assert _get_block(block, (400, 800), 1) == block.children[2]
    assert _get_block(block, (400, 800), 2) == block.children[2].children[0]
    assert _get_block(block, (400, 800), 3) == block.children[2].children[0].children[1]
    assert _get_block(block, (0, 1200), 0) == block
    assert _get_block(block, (0, 1200), 1) == block.children[2]
    assert _get_block(block, (0, 1200), 2) == block.children[2].children[2]
    assert _get_block(block, (0, 1200), 3) == block.children[2].children[2].children[1]
    assert _get_block(block, (0, 1200), 4) == block.children[2].children[2].children[1].children[1]
    assert _get_block(block, (0, 1200), 5) == block.children[2].children[2].children[1].children[1]
    assert _get_block(block, (400, 1200), 0) == block
    assert _get_block(block, (400, 1200), 1) == block.children[2]
    assert _get_block(block, (400, 1200), 2) == block.children[2].children[3]
    assert _get_block(block, (400, 1200), 3) == block.children[2].children[3]
    assert _get_block(block, (0, 1600), 0) is None
    assert _get_block(block, (0, 1600), 1) is None
    assert _get_block(block, (100, 1600), 0) is None
    assert _get_block(block, (100, 1600), 1) is None
    assert _get_block(block, (400, 1600), 0) is None
    assert _get_block(block, (400, 1600), 1) is None
    assert _get_block(block, (1600, 800), 0) is None
    assert _get_block(block, (1600, 1600), 1) is None
    assert _get_block(block, (1200, 1200), 0) == block
    assert _get_block(block, (1200, 1200), 1) == block.children[3]
    assert _get_block(block, (1200, 1200), 2) == block.children[3].children[3]
    assert _get_block(block, (1200, 1200), 3) == block.children[3].children[3].children[1]
    assert _get_block(block, (1200, 1200), 4) == block.children[3].children[3].children[1].children[1]
    assert _get_block(block, (1200, 1200), 5) == block.children[3].children[3].children[1].children[1]
    assert _get_block(block, (1300, 1200), 0) == block
    assert _get_block(block, (1300, 1200), 1) == block.children[3]
    assert _get_block(block, (1300, 1200), 2) == block.children[3].children[3]
    assert _get_block(block, (1300, 1200), 3) == block.children[3].children[3].children[1]
    assert _get_block(block, (1300, 1200), 4) == block.children[3].children[3].children[1].children[0]
    assert _get_block(block, (1300, 1200), 5) == block.children[3].children[3].children[1].children[0]
    assert _get_block(block, (1200, 1300), 0) == block
    assert _get_block(block, (1200, 1300), 1) == block.children[3]
    assert _get_block(block, (1200, 1300), 2) == block.children[3].children[3]
    assert _get_block(block, (1200, 1300), 3) == block.children[3].children[3].children[1]
    assert _get_block(block, (1200, 1300), 4) == block.children[3].children[3].children[1].children[2]
    assert _get_block(block, (1200, 1300), 5) == block.children[3].children[3].children[1].children[2]
    assert _get_block(block, (1300, 1300), 0) == block
    assert _get_block(block, (1300, 1300), 1) == block.children[3]
    assert _get_block(block, (1300, 1300), 2) == block.children[3].children[3]
    assert _get_block(block, (1300, 1300), 3) == block.children[3].children[3].children[1]
    assert _get_block(block, (1300, 1300), 4) == block.children[3].children[3].children[1].children[3]
    assert _get_block(block, (1300, 1300), 5) == block.children[3].children[3].children[1].children[3]
    assert _get_block(block, (1400, 1200), 0) == block
    assert _get_block(block, (1400, 1200), 1) == block.children[3]
    assert _get_block(block, (1400, 1200), 2) == block.children[3].children[3]
    assert _get_block(block, (1400, 1200), 3) == block.children[3].children[3].children[0]
    assert _get_block(block, (1400, 1200), 4) == block.children[3].children[3].children[0].children[1]
    assert _get_block(block, (1400, 1200), 5) == block.children[3].children[3].children[0].children[1]
    assert _get_block(block, (1400, 1300), 0) == block
    assert _get_block(block, (1400, 1300), 1) == block.children[3]
    assert _get_block(block, (1400, 1300), 2) == block.children[3].children[3]
    assert _get_block(block, (1400, 1300), 3) == block.children[3].children[3].children[0]
    assert _get_block(block, (1400, 1300), 4) == block.children[3].children[3].children[0].children[2]
    assert _get_block(block, (1400, 1300), 5) == block.children[3].children[3].children[0].children[2]
    assert _get_block(block, (1400, 1400), 0) == block
    assert _get_block(block, (1400, 1400), 1) == block.children[3]
    assert _get_block(block, (1400, 1400), 2) == block.children[3].children[3]
    assert _get_block(block, (1400, 1400), 3) == block.children[3].children[3].children[3]
    assert _get_block(block, (1400, 1400), 4) == block.children[3].children[3].children[3].children[1]
    assert _get_block(block, (1400, 1400), 5) == block.children[3].children[3].children[3].children[1]
    assert _get_block(block, (1200, 1400), 0) == block
    assert _get_block(block, (1200, 1400), 1) == block.children[3]
    assert _get_block(block, (1200, 1400), 2) == block.children[3].children[3]
    assert _get_block(block, (1200, 1400), 3) == block.children[3].children[3].children[2]
    assert _get_block(block, (1200, 1400), 4) == block.children[3].children[3].children[2].children[1]
    assert _get_block(block, (1200, 1400), 5) == block.children[3].children[3].children[2].children[1]
    assert _get_block(block, (1300, 1400), 0) == block
    assert _get_block(block, (1300, 1400), 1) == block.children[3]
    assert _get_block(block, (1300, 1400), 2) == block.children[3].children[3]
    assert _get_block(block, (1300, 1400), 3) == block.children[3].children[3].children[2]
    assert _get_block(block, (1300, 1400), 4) == block.children[3].children[3].children[2].children[0]
    assert _get_block(block, (1300, 1400), 5) == block.children[3].children[3].children[2].children[0]


def test_update_children_position_1x1() -> None:
    board = board_one_by_one()
    board._update_children_positions((0, 0))
    assert board.position == (0, 0)
    board._update_children_positions((1, 2))
    assert board.position == (1, 2)
    board._update_children_positions((100, 200))
    assert board.position == (100, 200)


def test_update_children_position_2x2() -> None:
    board = board_2x2()
    board._update_children_positions((0, 0))
    assert board.position == (0, 0)
    assert board.children[1].position == (0, 0)
    board._update_children_positions((10, 20))
    assert board.position == (10, 20)
    assert board.children[1].position == (10, 20)
    assert board.children[0].position == (385, 20)
    assert board.children[2].position == (10, 395)
    assert board.children[3].position == (385, 395)


def test_update_children_position_4x4() -> None:
    board = board_16x16_example_1()
    board._update_children_positions((0, 0))
    assert board.position == (0, 0)
    assert board.children[1].position == (0, 0)
    board._update_children_positions((100, 100))
    assert board.position == (100, 100)
    assert board.children[0].position == (475, 100)
    assert board.children[1].position == (100, 100)
    assert board.children[2].position == (100, 475)
    assert board.children[3].position == (475, 475)
    assert board.children[1].children[0].position == (288, 100)
    assert board.children[1].children[1].position == (100, 100)
    assert board.children[1].children[2].position == (100, 288)
    assert board.children[1].children[3].position == (288, 288)


def test_update_children_position_16x16() -> None:
    board = board_16x16_actual_example()
    board._update_children_positions((0, 0))
    assert board.position == (0, 0)
    assert board.children[1].position == (0, 0)
    assert board.children[1].children[1].position == (0, 0)
    board._update_children_positions((100, 100))
    assert board.position == (100, 100)
    assert board.children[0].position == (900, 100)
    assert board.children[1].position == (100, 100)
    assert board.children[1].children[0].position == (500, 100)
    assert board.children[1].children[1].position == (100, 100)
    assert board.children[1].children[2].position == (100, 500)
    assert board.children[1].children[3].position == (500, 500)
    assert board.children[2].position == (100, 900)
    assert board.children[2].children[1].position == (100, 900)
    assert board.children[2].children[1].children[0].position == (300, 900)
    assert board.children[2].children[1].children[1].position == (100, 900)
    assert board.children[2].children[1].children[2].position == (100, 1100)
    assert board.children[2].children[1].children[3].position == (300, 1100)
    assert board.children[2].children[3].position == (500, 1300)
    assert board.children[2].children[2].position == (100, 1300)
    assert board.children[2].children[2].children[0].position == (300, 1300)
    assert board.children[2].children[2].children[1].position == (100, 1300)
    assert board.children[2].children[2].children[2].position == (100, 1500)
    assert board.children[2].children[2].children[3].position == (300, 1500)
    assert board.children[2].children[2].children[0].children[0].position == (400, 1300)
    assert board.children[2].children[2].children[0].children[1].position == (300, 1300)
    assert board.children[2].children[2].children[0].children[2].position == (300, 1400)
    assert board.children[2].children[2].children[0].children[3].position == (400, 1400)
    assert board.children[2].children[2].children[1].children[0].position == (200, 1300)
    assert board.children[2].children[2].children[1].children[1].position == (100, 1300)
    assert board.children[2].children[2].children[1].children[2].position == (100, 1400)
    assert board.children[2].children[2].children[1].children[3].position == (200, 1400)
    assert board.children[2].children[2].children[2].children[0].position == (200, 1500)
    assert board.children[2].children[2].children[2].children[1].position == (100, 1500)
    assert board.children[2].children[2].children[2].children[2].position == (100, 1600)
    assert board.children[2].children[2].children[2].children[3].position == (200, 1600)
    assert board.children[2].children[2].children[3].children[0].position == (400, 1500)
    assert board.children[2].children[2].children[3].children[1].position == (300, 1500)
    assert board.children[2].children[2].children[3].children[2].position == (300, 1600)
    assert board.children[2].children[2].children[3].children[3].position == (400, 1600)

    assert board.children[3].position == (900, 900)
    assert board.children[3].children[1].position == (900, 900)
    assert board.children[3].children[1].children[1].position == (900, 900)
    assert board.children[3].children[1].children[1].children[1].position == (900, 900)
    assert board.children[3].children[0].position == (1300, 900)
    assert board.children[3].children[0].children[1].position == (1300, 900)
    assert board.children[3].children[0].children[1].children[1].position == (1300, 900)


def test_flatten_1x1() -> None:
    result = _flatten(board_one_by_one())

    # We are expected a "square" 2D list
    for sublist in result:
        assert len(result) == len(sublist)

    assert result == flattened_board_1x1()


def test_flatten_2x2() -> None:
    result = _flatten(board_2x2())

    # We are expected a "square" 2D list
    for sublist in result:
        assert len(result) == len(sublist)

    assert result == flattened_board_2x2()


def test_flatten_8x8() -> None:
    result = _flatten(board_8x8_example())

    # We are expected a "square" 2D list
    for sublist in result:
        assert len(result) == len(sublist)

    assert result == flattened_board_8x8()


def test_flatten_actual_16x16() -> None:
    result = _flatten(board_16x16_actual_example())

    # We are expected a "square" 2D list
    for sublist in result:
        assert len(result) == len(sublist)

    assert result == flattened_board_actual_16x16()


def test_perimeter_goal_1x1() -> None:
    correct_scores = [
        (COLOUR_LIST[0], 0),
        (COLOUR_LIST[1], 4),
        (COLOUR_LIST[2], 0),
        (COLOUR_LIST[3], 0)
    ]

    for colour, expected in correct_scores:
        goal = PerimeterGoal(colour)
        assert goal.score(board_one_by_one()) == expected


def test_perimeter_goal_2x2() -> None:
    correct_scores = [
        (COLOUR_LIST[0], 2),
        (COLOUR_LIST[1], 2),
        (COLOUR_LIST[2], 2),
        (COLOUR_LIST[3], 2)
    ]

    for colour, expected in correct_scores:
        goal = PerimeterGoal(colour)
        assert goal.score(board_2x2()) == expected


def test_perimeter_goal_4x4() -> None:
    correct_scores1 = [
        (COLOUR_LIST[0], 1),
        (COLOUR_LIST[1], 7),
        (COLOUR_LIST[2], 4),
        (COLOUR_LIST[3], 4)
    ]

    correct_scores2 = [
        (COLOUR_LIST[0], 0),
        (COLOUR_LIST[1], 7),
        (COLOUR_LIST[2], 4),
        (COLOUR_LIST[3], 5)
    ]

    correct_scores3 = [
        (COLOUR_LIST[0], 1),
        (COLOUR_LIST[1], 5),
        (COLOUR_LIST[2], 4),
        (COLOUR_LIST[3], 6)
    ]

    for colour, expected in correct_scores1:
        goal = PerimeterGoal(colour)
        assert goal.score(board_16x16_example_1()) == expected

    for colour, expected in correct_scores2:
        goal = PerimeterGoal(colour)
        assert goal.score(board_16x16_example_2()) == expected

    for colour, expected in correct_scores3:
        goal = PerimeterGoal(colour)
        assert goal.score(board_16x16_example_3()) == expected


def test_perimeter_goal_8x8() -> None:
    correct_scores = [
        (COLOUR_LIST[0], 8),
        (COLOUR_LIST[1], 6),
        (COLOUR_LIST[2], 3),
        (COLOUR_LIST[3], 15)
    ]

    for colour, expected in correct_scores:
        goal = PerimeterGoal(colour)
        assert goal.score(board_8x8_example()) == expected


def test_perimeter_goal_16x16() -> None:
    correct_scores = [
        (COLOUR_LIST[0], 24),
        (COLOUR_LIST[1], 12),
        (COLOUR_LIST[2], 14),
        (COLOUR_LIST[3], 14)
    ]

    for colour, expected in correct_scores:
        goal = PerimeterGoal(colour)
        assert goal.score(board_16x16_actual_example()) == expected


def test_blob_goal_1x1() -> None:
    correct_scores = [
        (COLOUR_LIST[0], 0),
        (COLOUR_LIST[1], 1),
        (COLOUR_LIST[2], 0),
        (COLOUR_LIST[3], 0)
    ]

    # Set up a goal for each colour and check the results
    for colour, expected in correct_scores:
        goal = BlobGoal(colour)
        assert goal.score(board_one_by_one()) == expected


def test_blob_goal_2x2() -> None:
    correct_scores = [
        (COLOUR_LIST[0], 1),
        (COLOUR_LIST[1], 1),
        (COLOUR_LIST[2], 1),
        (COLOUR_LIST[3], 1)
    ]

    # Set up a goal for each colour and check the results
    for colour, expected in correct_scores:
        goal = BlobGoal(colour)
        assert goal.score(board_2x2()) == expected


def test_blob_goal_4x4() -> None:
    correct_scores1 = [
        (COLOUR_LIST[0], 1),
        (COLOUR_LIST[1], 6),
        (COLOUR_LIST[2], 4),
        (COLOUR_LIST[3], 4)
    ]

    correct_scores2 = [
        (COLOUR_LIST[0], 1),
        (COLOUR_LIST[1], 6),
        (COLOUR_LIST[2], 4),
        (COLOUR_LIST[3], 5)
    ]
    correct_scores3 = [
        (COLOUR_LIST[0], 1),
        (COLOUR_LIST[1], 4),
        (COLOUR_LIST[2], 4),
        (COLOUR_LIST[3], 4)
    ]

    # Set up a goal for each colour and check the results
    for colour, expected in correct_scores1:
        goal = BlobGoal(colour)
        assert goal.score(board_16x16_example_1()) == expected

    for colour, expected in correct_scores2:
        goal = BlobGoal(colour)
        assert goal.score(board_16x16_example_2()) == expected

    for colour, expected in correct_scores3:
        goal = BlobGoal(colour)
        assert goal.score(board_16x16_example_3()) == expected


def test_blob_goal_8x8() -> None:
    correct_scores = [
        (COLOUR_LIST[0], 4),
        (COLOUR_LIST[1], 5),
        (COLOUR_LIST[2], 4),
        (COLOUR_LIST[3], 18)
    ]

    # Set up a goal for each colour and check the results
    for colour, expected in correct_scores:
        goal = BlobGoal(colour)
        assert goal.score(board_8x8_example()) == expected


def test_blob_goal_16x16() -> None:
    correct_scores = [
        (COLOUR_LIST[0], 84),
        (COLOUR_LIST[1], 16),
        (COLOUR_LIST[2], 16),
        (COLOUR_LIST[3], 22)
    ]

    for colour, expected in correct_scores:
        goal = BlobGoal(colour)
        assert goal.score(board_16x16_actual_example()) == expected

def test_create_copy_1x1() -> None:
    block = board_one_by_one()
    block_copy = block.create_copy()
    assert block == block_copy
    assert id(block) != id(block_copy)


def test_create_copy_fake_16x16() -> None:
    block = board_16x16()
    block_copy = block.create_copy()
    assert block == block_copy
    assert id(block) != id(block_copy)
    assert id(block.children) != id(block_copy.children)
    assert id(block.children[0]) != id(block_copy.children[0])
    assert id(block.children[1]) != id(block_copy.children[1])
    assert id(block.children[2]) != id(block_copy.children[2])
    assert id(block.children[3]) != id(block_copy.children[3])
    assert id(block.children[0].children[0]) != id(block_copy.children[0].children[0])
    assert id(block.children[0].children[1]) != id(block_copy.children[0].children[1])
    assert id(block.children[0].children[2]) != id(block_copy.children[0].children[2])
    assert id(block.children[0].children[3]) != id(block_copy.children[0].children[3])


def test_create_copy_actual_16x16() -> None:
    block = board_16x16_actual_example()
    block_copy = block.create_copy()
    assert block == block_copy
    assert id(block) != id(block_copy)
    assert id(block.children) != id(block_copy.children)
    assert id(block.children[0]) != id(block_copy.children[0])
    assert id(block.children[1]) != id(block_copy.children[1])
    assert id(block.children[2]) != id(block_copy.children[2])
    assert id(block.children[3]) != id(block_copy.children[3])
    assert id(block.children[1].children[0]) != id(block_copy.children[1].children[0])
    assert id(block.children[1].children[1]) != id(block_copy.children[1].children[1])
    assert id(block.children[1].children[2]) != id(block_copy.children[1].children[2])
    assert id(block.children[1].children[3]) != id(block_copy.children[1].children[3])
    assert id(block.children[2].children[0]) != id(block_copy.children[2].children[0])
    assert id(block.children[2].children[0].children[0]) != id(block_copy.children[2].children[0].children[0])
    assert id(block.children[2].children[0].children[1]) != id(block_copy.children[2].children[0].children[1])
    assert id(block.children[2].children[0].children[2]) != id(block_copy.children[2].children[0].children[2])
    assert id(block.children[2].children[0].children[3]) != id(block_copy.children[2].children[0].children[3])
    assert id(block.children[2].children[2]) != id(block_copy.children[2].children[2])
    assert id(block.children[2].children[2].children[0]) != id(block_copy.children[2].children[2].children[0])
    assert id(block.children[2].children[2].children[1]) != id(block_copy.children[2].children[2].children[1])
    assert id(block.children[2].children[2].children[2]) != id(block_copy.children[2].children[2].children[2])
    assert id(block.children[2].children[2].children[3]) != id(block_copy.children[2].children[2].children[3])
    assert id(block.children[2].children[2].children[0].children[2]) != id(block_copy.children[2].children[2].children[0].children[2])
    assert id(block.children[2].children[2].children[1].children[3]) != id(block_copy.children[2].children[2].children[1].children[3])
    assert id(block.children[2].children[2].children[2].children[0]) != id(block_copy.children[2].children[2].children[2].children[0])
    assert id(block.children[2].children[2].children[3].children[1]) != id(block_copy.children[2].children[2].children[3].children[1])

def test_swap_no_children() -> None:
    block = board_one_by_one()
    assert block.swap(0) is False
    assert block.swap(1) is False


def test_swap_2x2_horizontal() -> None:
    block = board_2x2()
    assert block.children[0].swap(0) is False
    assert block.swap(0) is True
    assert block == board_2x2_swap_0()


def test_swap_2x2_vertical() -> None:
    block = board_2x2()
    assert block.swap(1) is True
    assert block == board_2x2_swap_1()


def test_swap_4x4_vertical_example_test() -> None:
    block = board_16x16()
    assert block.swap(1) is True
    assert block == board_16x16_swap_1()


def test_swap_8x8_horizontal_children() -> None:
    block = board_8x8_example()
    assert block.children[1].swap(0) is True
    assert block == board_8x8_example()


def test_swap_8x8_vertical_children() -> None:
    block = board_8x8_example()
    assert block.children[1].swap(1) is True
    assert block == board_8x8_example()

def test_swap_16x16_horizontal_whole_board() -> None:
    block = board_16x16_actual_example()
    assert block.swap(0) is True
    assert block == board_actual_16x16_swap_all_horizontal()


def test_swap_16x16_vertical_whole_board() -> None:
    block = board_16x16_actual_example()
    assert block.swap(1) is True
    assert block == board_16x16_actual_example_swap_all_vertical()


def test_swap_16x16_horizontal_children() -> None:
    block = board_16x16_actual_example()
    assert block.children[3].swap(0) is True
    assert block == board_16x16_actual_example()
    assert block.children[3].children[0].swap(0) is True
    assert block == board_16x16_actual_example()


def test_swap_16x16_vertical_children() -> None:
    block = board_16x16_actual_example()
    assert block.children[3].swap(1) is True
    assert block == board_16x16_actual_example()
    assert block.children[3].children[2].swap(0) is True
    assert block == board_16x16_actual_example()


def test_swap_16x16_horizontal_children_change() -> None:
    block = board_16x16_actual_example()
    assert block.children[2].swap(0) is True
    assert block == board_16x16_swap_children_horizontal()


def test_swap_16x16_vertical_children_change() -> None:
    block = board_16x16_actual_example()
    assert block.children[2].swap(1) is True
    assert block == board_16x16_swap_children_vertical()


def test_paint_1x1() -> None:
    block = board_one_by_one()
    assert block.paint((199, 44, 58)) is False
    assert block.paint((1, 128, 181)) is True
    assert block.colour == (1, 128, 181)


def test_paint_2x2() -> None:
    block = board_2x2()
    assert block.paint((199, 44, 58)) is False
    assert block.children[0].paint((1, 128, 181)) is False
    assert block.children[1].paint((138, 151, 71)) is False
    assert block.children[2].paint((199, 44, 58)) is False
    assert block.children[3].paint((255, 211, 92)) is False
    assert block.children[0].paint((255, 211, 92)) is True
    assert block.children[1].paint((1, 128, 181)) is True
    assert block.children[2].paint((1, 128, 181)) is True
    assert block.children[3].paint((1, 128, 181)) is True
    assert block.colour is None
    assert block.children[0].colour == (255, 211, 92)
    assert block.children[1].colour == (1, 128, 181)
    assert block.children[2].colour == (1, 128, 181)
    assert block.children[3].colour == (1, 128, 181)


def test_paint_4x4() -> None:
    block = board_16x16()
    assert block.paint((199, 44, 58)) is False
    assert block.children[0].paint((1, 128, 181)) is False
    assert block.children[1].paint((1, 128, 181)) is False
    assert block.children[2].paint((1, 128, 181)) is False
    assert block.children[3].paint((1, 128, 181)) is False
    assert block.children[1].paint((138, 151, 71)) is False
    assert block.children[2].paint(COLOUR_LIST[1]) is False
    assert block.children[3].paint(COLOUR_LIST[3]) is False
    assert block.children[0].children[0].paint(COLOUR_LIST[2]) is True
    assert block.children[0].children[1].paint(COLOUR_LIST[2]) is True
    assert block.children[0].children[2].paint(COLOUR_LIST[2]) is True
    assert block.children[0].children[3].paint(COLOUR_LIST[2]) is True
    assert block.colour is None
    assert block.children[0].children[0].colour == COLOUR_LIST[2]
    assert block.children[0].children[1].colour == COLOUR_LIST[2]
    assert block.children[0].children[2].colour == COLOUR_LIST[2]
    assert block.children[0].children[3].colour == COLOUR_LIST[2]
    assert block.children[0].children[0].paint(COLOUR_LIST[2]) is False
    assert block.children[0].children[1].paint(COLOUR_LIST[2]) is False
    assert block.children[0].children[2].paint(COLOUR_LIST[2]) is False
    assert block.children[0].children[3].paint(COLOUR_LIST[2]) is False


def test_combine_1x1() -> None:
    block = board_one_by_one()
    assert block.combine() is False


def test_combine_2x2() -> None:
    block = board_2x2()
    assert block.combine() is False


def test_combine_2x2_1() -> None:
    block = board_2x2_combine_1()
    assert block.combine() is True
    assert len(block.children) == 0
    assert block.colour == COLOUR_LIST[2]
    assert block.combine() is False


def test_combine_2x2_2() -> None:
    block = board_2x2_combine_2()
    assert block.combine() is True
    assert len(block.children) == 0
    assert block.colour == COLOUR_LIST[2]
    assert block.combine() is False


def test_combine_2x2_3() -> None:
    block = board_2x2_combine_3()
    assert block.combine() is True
    assert len(block.children) == 0
    assert block.colour == COLOUR_LIST[2]
    assert block.combine() is False


def test_combine_2x2_4_5_6() -> None:
    block1 = board_2x2_combine_4()
    block2 = board_2x2_combine_5()
    block3 = board_2x2_combine_6()
    assert block1.combine() is False
    assert block2.combine() is False
    assert block3.combine() is False


def test_combine_2x2_7() -> None:
    block = board_2x2_combine_7()
    assert block.combine() is True
    assert len(block.children) == 0
    assert block.colour == COLOUR_LIST[2]
    assert block.combine() is False


def test_combine_2x2_8() -> None:
    block = board_2x2_combine_8()
    assert block.combine() is True
    assert len(block.children) == 0
    assert block.colour == COLOUR_LIST[2]
    assert block.combine() is False


def test_combine_2x2_9() -> None:
    block = board_2x2_combine_9()
    assert block.combine() is True
    assert len(block.children) == 0
    assert block.colour == COLOUR_LIST[2]
    assert block.combine() is False


def test_combine_2x2_10() -> None:
    block = board_2x2_combine_10()
    assert block.combine() is True
    assert len(block.children) == 0
    assert block.colour == COLOUR_LIST[2]
    assert block.combine() is False


def test_combine_4x4() -> None:
    block = board_16x16()
    assert block.combine() is False
    assert block.children[0].combine() is True
    assert block.children[1].combine() is False
    assert block.children[2].combine() is False
    assert block.children[3].combine() is False
    assert block.children[0].combine() is False
    assert len(block.children) == 4
    assert len(block.children[0].children) == 0
    assert len(block.children[1].children) == 0
    assert len(block.children[2].children) == 0
    assert len(block.children[2].children) == 0
    assert block.children[0].colour == COLOUR_LIST[1]


def test_combine_8x8() -> None:
    block = board_8x8_example()
    assert block.combine() is False
    assert block.children[0].combine() is False
    assert block.children[1].combine() is False
    assert block.children[2].combine() is False
    assert block.children[3].combine() is False
    assert block.children[0].children[1].combine() is False
    assert block.children[1].children[0].combine() is False
    assert block.children[1].children[1].combine() is False
    assert block.children[1].children[2].combine() is False
    assert block.children[1].children[2].children[0].combine() is False
    assert block.children[1].children[2].children[1].combine() is False
    assert block.children[1].children[2].children[2].combine() is False
    assert block.children[1].children[2].children[3].combine() is False
    assert block.children[1].children[3].combine() is False
    assert block.children[3].children[2].combine() is False


def test_rotate_1x1() -> None:
    block = board_one_by_one()
    assert block.rotate(1) is False
    assert block.rotate(3) is False


def test_rotate_2x2() -> None:
    block = board_2x2()
    assert block.rotate(1) is True
    assert block == board_2x2_clockwise_once()
    assert block.rotate(1) is True
    assert block == board_2x2_clockwise_twice()
    assert block.rotate(1) is True
    assert block == board_2x2_clockwise_three_times()
    assert block.rotate(1) is True
    assert block == board_2x2()
    assert block.rotate(3) is True
    assert block == board_2x2_clockwise_three_times()
    assert block.rotate(3) is True
    assert block == board_2x2_clockwise_twice()
    assert block.rotate(3) is True
    assert block == board_2x2_clockwise_once()
    assert block.rotate(3) is True
    assert block == board_2x2()


def test_rotate_4x4() -> None:
    block = board_16x16()
    assert block.rotate(1) is True
    assert block == board_4x4_rotate()
    assert block.rotate(3) is True
    assert block == board_16x16()


def test_rotate_8x8() -> None:
    block = board_8x8_example()
    assert block.rotate(1) is True
    assert block == board_8x8_rotate()
    assert block.rotate(3) is True
    assert block == board_8x8_example()


def test_rotate_16x16() -> None:
    block = board_16x16_actual_example()
    assert block.rotate(1) is True
    assert block == board_actual_16x16_rotate()
    assert block.rotate(3) is True
    assert block == board_16x16_actual_example()

if __name__ == '__main__':
    import pytest
    pytest.main(['-vv', 'friend_test.py'])

