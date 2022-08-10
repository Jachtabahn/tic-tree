import numpy
from info import info

X = 1
O = 2

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

  def __init__(self, board, current_player=X):
    self.board = board
    self.current_player = current_player

  def step(self, action):
    next_state = self.board.copy()
    next_state[action.position] = action.player
    return State(next_state, self._next_player())

  def _next_player(self):
    if self.current_player == X: return O
    if self.current_player == O: return X

  def possible_actions(self):
    empty_positions = list(zip(*(self.board == 0).nonzero()))
    next_player = self._next_player()
    possible_actions = [Action(position, next_player) for position in empty_positions]
    return possible_actions

  def __repr__(self):
    if self.current_player == X: player_text = 'X'
    if self.current_player == O: player_text = 'O'
    state_text = f'{self.board}\nTurn: {player_text}'
    return state_text

# def construct_tree

import json

class Tree:
  def __init__(self, board, current_player, best_action, best_outcome, tried_actions, untried_actions):
    self.board = None
    self.current_player = None
    self.best_action = []
    self.best_outcome = []
    self.tried_actions = None
    self.untried_actions = None

  def __repr__(self):
    return json.dumps(self.__dict__)

tree = Tree(
  board = [
    [-1, -1, 1],
    [-1, -1, 1],
    [0, 0, 0]
  ],
  current_player = 'O',
  tried_actions = [
    [2, 0],
    [2, 1],
    [2, 2],
  ],
  untried_actions = [
  ],
  best_action = [2, 2],
  best_outcome = 1
)

info(tree)
