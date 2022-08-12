import numpy
import hashlib
from info import info

X = 1
O = 2

next_state_name = 0
next_node_name = 0

# Eine Action ist genauso viel Wert wie ein Tupel ((1, 1), 1): meaning Put 1 on position (1, 1)
class Action:
  def __init__(self, position, player):
    self.position = position
    self.player = player
  def __repr__(self):
    if self.player == X: player_text = 'X'
    if self.player == O: player_text = 'O'
    return f'"Put {player_text} on {self.position}"'

class State:

  def __init__(self, board, current_player):

    global next_state_name
    self.name = next_state_name
    next_state_name += 1

    self.board = board
    self.current_player = current_player

    state_text = str(self.board) + str(current_player)
    self.hash = hashlib.sha256(state_text.encode('utf-8')).hexdigest()

  def step(self, action):
    next_state = self.board.copy()
    next_state[action.position] = action.player
    return State(next_state, self._next_player())

  def _next_player(self):
    if self.current_player == X: return O
    if self.current_player == O: return X

  def possible_actions(self):
    empty_positions = list(zip(*(numpy.array(self.board) == 0).nonzero()))
    return empty_positions

  def __repr__(self):
    if self.current_player == X: player_text = 'X'
    if self.current_player == O: player_text = 'O'
    state_text = f'{self.board}\nTurn: {player_text}'
    return state_text

# def construct_tree

import json

class Node:
  def __init__(self, state):
    self.state = state
    self.best_action = None
    self.best_outcome = None
    self.children = dict((action, None) for action in state.possible_actions())

  def create_node(board, current_player):

    # Try to fetch a node from memory.
    state = State(board, current_player)
    if state.hash in node_from_state_hash:
      return node_from_state_hash[state.hash]

    # Fetching didn't work... create a node,
    node = Node(state)

    # then save it into memory,
    node_from_state_hash[state.hash] = node

    # and make it available for use.
    return node

  def __repr__(self):
    return str({
      "state": {
        "board": self.state.board,
        "current_player": self.state.current_player
      },
      "best_action": self.best_action,
      "best_outcome": self.best_outcome,
      "children": self.children
    })

node_from_state_hash = {}

node = Node.create_node(
  board = [
    [-1, -1, 1],
    [-1, -1, 1],
    [0, 0, 0]
  ],
  current_player = 'O'
)

info(node)
info(node_from_state_hash)
