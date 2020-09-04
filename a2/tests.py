from typing import List, Optional, Tuple
import os
import pygame
import pytest

from block import Block
from blocky import _block_to_squares
from goal import BlobGoal, PerimeterGoal, _flatten, generate_goals
from player import _get_block, create_players, RandomPlayer, SmartPlayer, HumanPlayer
from renderer import Renderer
from settings import COLOUR_LIST


@pytest.fixture
def board_4x4() -> Block:
    """Create a reference board with a size of 750 and a max_depth of 2.
    """
    # Level 0
    colours = [COLOUR_LIST[0], COLOUR_LIST[2], COLOUR_LIST[1], COLOUR_LIST[3]]
    board = Block((0, 0), 750, colours[0], 0, 2)

    return board


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


@pytest.fixture
def flattened_board_4x4() -> List[List[Tuple[int, int, int]]]:
    """Create a list of the unit cells inside the reference board."""
    return [
        [COLOUR_LIST[0], COLOUR_LIST[0], COLOUR_LIST[0], COLOUR_LIST[0]],
        [COLOUR_LIST[0], COLOUR_LIST[0], COLOUR_LIST[0], COLOUR_LIST[0]],
        [COLOUR_LIST[0], COLOUR_LIST[0], COLOUR_LIST[0], COLOUR_LIST[0]],
        [COLOUR_LIST[0], COLOUR_LIST[0], COLOUR_LIST[0], COLOUR_LIST[0]]
    ]


def test_block_flatten(board_4x4, flattened_board_4x4) -> None:
    """Test that flattening the reference board results in the expected list
        of colours.
        """
    result = _flatten(board_4x4)

    assert len(result) == 4
    # We are expected a "square" 2D list
    for sublist in result:
        assert len(result) == len(sublist)

    assert result == flattened_board_4x4


@pytest.fixture
def board_16x16() -> Block:
    """Create a reference board with a size of 750 and a max_depth of 2.
    """
    # Level 0
    board = Block((0, 0), 750, None, 0, 2)

    # Level 1
    colours = [None, COLOUR_LIST[1], COLOUR_LIST[3], COLOUR_LIST[2]]
    set_children(board, colours)

    # Level 2
    colours = [COLOUR_LIST[0], COLOUR_LIST[1], COLOUR_LIST[1], COLOUR_LIST[3]]
    set_children(board.children[0], colours)

    return board


@pytest.fixture
def flattened_board_2x2() -> List[List[Tuple[int, int, int]]]:
    """Create a list of the unit cells inside the reference board."""
    return [
        [COLOUR_LIST[1], COLOUR_LIST[3]],
        [COLOUR_LIST[0], COLOUR_LIST[2]],
    ]


@pytest.fixture
def board_2x2() -> Block:
    board = Block((0, 0), 750, None, 0, 1)
    colours = [COLOUR_LIST[0], COLOUR_LIST[1], COLOUR_LIST[3], COLOUR_LIST[2]]
    set_children(board, colours)
    return board


def test_block_flatten2x2(board_2x2, flattened_board_2x2) -> None:
    """Test that flattening the reference board results in the expected list
        of colours.
        """
    result = _flatten(board_2x2)

    assert len(result) == 2
    # We are expected a "square" 2D list
    for sublist in result:
        assert len(result) == len(sublist)

    assert result == flattened_board_2x2


def test_generate_goals() -> None:
    """Test generate_goals_method"""
    goal_list = generate_goals(4)
    assert len(goal_list) == 4
    colour_list = [goal.colour for goal in goal_list]
    colour_set = set(colour_list)
    assert len(colour_list) == len(colour_set)
    for i in range(0, len(colour_list)):
        assert colour_list[i] in colour_set


def test_blocks_to_squares(board_4x4) -> None:
    "Test blocks to squares method"
    bts = _block_to_squares(board_4x4)
    assert isinstance(bts, list) is True
    assert isinstance(bts[0][1], tuple) is True
    assert isinstance(bts[0][2], int) is True
    for block in bts:
        assert len(block) == 3
    assert len(bts) == 1


def test_blocks_to_squares(board_16x16) -> None:
    "Test blocks to squares method"
    bts = _block_to_squares(board_16x16)
    assert isinstance(bts, list) is True
    assert isinstance(bts[0][1], tuple) is True
    assert isinstance(bts[0][2], int) is True
    for block in bts:
        assert len(block) == 3
    assert len(bts) == 7


def test_get_block(board_16x16) -> None:
    new_block = _get_block(board_16x16, (0, 0), 1)
    assert new_block.colour == COLOUR_LIST[1]
    assert new_block.level == 1
    block2 = _get_block(board_16x16, (350, 0), 8)
    assert block2.colour == COLOUR_LIST[1]
    assert block2.level == 1


def test_create_players() -> None:
    new_players = create_players(0, 0, [1, 2, 3, 4])
    assert len(new_players) == 4
    for i in range(0, len(new_players)):
        assert isinstance(new_players[i], SmartPlayer) is True
    new_players2 = create_players(1, 1, [1, 2])
    assert len(new_players2) == 4
    for i in range(0, len(new_players)):
        if i <= 0:
            assert isinstance(new_players2[i], HumanPlayer) is True
        if 0 < i <= 1:
            assert isinstance(new_players2[i], RandomPlayer) is True
        if i > 1:
            assert isinstance(new_players2[i], SmartPlayer) is True
