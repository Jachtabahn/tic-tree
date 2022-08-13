from info import info
import os
import visualize
import json
import hashlib
import numpy

X = 1
O = -1

possible_winning_rows = [[(r, c) for c in range(3)] for r in range(3)]
possible_winning_columns = [[(r, c) for r in range(3)] for c in range(3)]
main_diagonal = [(r, r) for r in range(3)]
side_diagonal = [(r, 2-r) for r in range(3)]

possible_winning_streaks = possible_winning_rows + possible_winning_columns + [main_diagonal, side_diagonal]

info(possible_winning_streaks)

class State:

  def __init__(self, board):
    self.board = numpy.array(board)
    self.current_player = self.get_current_player()
    self.winning_streak = self.determine_winning_streak()
    state_text = str(self.board) + str(self.current_player)
    self.hash = int(hashlib.sha256(state_text.encode('utf-8')).hexdigest(), 16)
    # for clearer reading
    # content-based
    # naming_renaming
    # You might want to only take a prefix of that hexdigest
    # for better viewing of the code in the .js file.
    # If the prefix is too short,
    # you will get an error below under
    # `node_from_state_hash[state.hash] = node`.

  def determine_winning_streak(self):
    for possible_winning_streak in possible_winning_streaks:
      sum_of_token_numbers = sum(self.board[position] for position in possible_winning_streak)
      if sum_of_token_numbers == 3:
        return possible_winning_streak
      if sum_of_token_numbers == -3:
        return possible_winning_streak
    return None

  def token_to_player(self, token):
    if token == X: return 'X'
    if token == O: return 'O'

  def get_current_player(self):
    sum_of_token_numbers = self.board.sum()
    if sum_of_token_numbers > 0:
      return O
    else:
      return X

  def step(self, action):
    next_board = self.board.copy()
    next_board[action] = self.current_player
    next_state = State(next_board)
    return next_state

  def possible_actions(self):
    if self.winning_streak is None:
      empty_positions = list(zip(*(numpy.array(self.board) == 0).nonzero()))
      return empty_positions
    return []

class Node:

  def __init__(self, state, parent, last_action):
    self.state = state
    self.last_action = last_action
    self.parent = parent

    self.best_action = None
    self.best_outcome = None

    self.children = dict((action, None) for action in state.possible_actions())

  def get_untried_actions(self):
    untried_actions = [action for action, child_node in self.children.items() if child_node is None]
    return untried_actions

  def get_tried_actions(self):
    tried_actions = [action for action, child_node in self.children.items() if child_node is not None]
    return tried_actions

  def create_node(board, parent=None, last_action=None):
    # Try to fetch a node from memory.
    state = State(board)
    if state.hash in node_from_state_hash:
      return node_from_state_hash[state.hash]

    # Fetching didn't work... create a node,
    node = Node(state, parent, last_action)

    # then save it into memory,
    node_from_state_hash[state.hash] = node

    # and make it available for use.
    return node

  def expand(self):
    for action in self.children:
      next_board = self.state.board.copy()
      next_board[action] = self.state.current_player
      child_node = Node.create_node(next_board, self, action)
      self.children[action] = child_node
      # Einen Rahmen um den Endzustand herum zeichnen
      child_node.expand()

  def determine_level(self):
    level = 0
    parent = self.parent
    while parent is not None:

      assert type(parent) == Node
      # type(node) == Node
      # True
      # type(node) == int
      # False

      parent = parent.parent
      level += 1
    return level

  def __repr__(self):
    return str({
      'state': {
        'board': self.state.board,
        'current_player': self.state.current_player,
        'hash': self.state.hash
      },
      'best_action': self.best_action,
      'best_outcome': self.best_outcome,
      'children': self.children
    })

  def get_children_hashes(self):
    children_hashes = []
    for action, child_node in self.children.items():
      if child_node is not None:
        children_hashes.append(child_node.state.hash)
    return children_hashes

  def create_vis_js_json(self):

    # Makes a folder for storing the png images
    if not os.path.exists('nodes'):
      os.mkdir('nodes')

    vis_js_json = {}

    vis_js_json['nodes'] = []
    for state_hash, node in node_from_state_hash.items():
      state_level = node.determine_level()
      info(state_level)

      # This vis.js configuration applies to this specific node.
      vis_node_declaration = {
        'id': state_hash,
        'level': state_level,
        'image': f'nodes/{node.state.hash}.svg'
      }
      vis_js_json['nodes'].append(vis_node_declaration)

      visualize.create_svg(node)

    vis_js_json['edges'] = []
    for state_hash, node in node_from_state_hash.items():
      children_hashes = node.get_children_hashes()
      info(state_hash)
      info(children_hashes)
      for child_hash in children_hashes:

        # This vis.js configuration applies to this specific edge.
        vis_edge_declaration = {
          'from': state_hash,
          'to': child_hash
        }
        vis_js_json['edges'].append(vis_edge_declaration)

    return vis_js_json

node_from_state_hash = {}

node = Node.create_node(
  board = [
    [O, X, O],
    [X, X, O],
    [0, 0, 0]
  ]
)

node.expand()

info(node)

vis_js_json = node.create_vis_js_json()
info(vis_js_json)
with open('tree_info.js', 'w') as file:
  print('tree_info=', end = '', file=file)
  print(json.dumps(vis_js_json, indent = 2), end = '', file=file)
