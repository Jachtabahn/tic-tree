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

class Tree:

  def __init__(self, state, possible_actions):
    self.state = None
    self.possible_actions = None
    self.state_value = None
    self.next_nodes = []

state_values = {}

board = State(numpy.zeros((3, 3)))

print(board)

action = Action((1, 1), X)
info(action)
next_state = board.step(action)
print(next_state)

initial_state = State(numpy.zeros((3, 3)))

info(numpy.where(initial_state.board))
possible_actions = initial_state.possible_actions()
info(possible_actions)
tic_tree = Tree(initial_state, possible_actions)
tic_tree
Tree()
