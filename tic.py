from info import info
import os
import visualize
import json
import hashlib
import numpy

X = 1
O = -1

class State:

  def __init__(self, board):
    self.board = numpy.array(board)
    self.current_player = self.get_current_player()
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
    return State(next_board)

  def possible_actions(self):
    empty_positions = list(zip(*(numpy.array(self.board) == 0).nonzero()))
    return empty_positions

class Node:
  def __init__(self, state, parent):
    self.state = state
    self.best_action = (1, 1)
    self.best_outcome = -1
    self.parent = parent
    self.children = dict((action, None) for action in state.possible_actions())

  def create_node(board, parent=None):
    # Try to fetch a node from memory.
    state = State(board)
    if state.hash in node_from_state_hash:
      return node_from_state_hash[state.hash]

    # Fetching didn't work... create a node,
    node = Node(state, parent)

    # then save it into memory,
    node_from_state_hash[state.hash] = node

    # and make it available for use.
    return node

  def expand(self):
    for action in self.children:
      next_board = self.state.board.copy()
      next_board[action] = self.state.current_player
      child_node = Node.create_node(next_board, self)
      self.children[action] = child_node

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
      vis_node_declaration = {
        'id': state_hash,
        'level': state_level,
        'image': f'nodes/{node.state.hash}.svg',
        'shape': 'image'
      }
      vis_js_json['nodes'].append(vis_node_declaration)
      visualize.create_svg(node)

    vis_js_json['edges'] = []
    for state_hash, node in node_from_state_hash.items():
      children_hashes = node.get_children_hashes()
      info(state_hash)
      info(children_hashes)
      for child_hash in children_hashes:
        vis_edge_declaration = {'from': state_hash, 'to': child_hash}
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
