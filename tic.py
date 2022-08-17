from info import info
import hashlib
import json
import numpy
import os
import time
import visualize

def is_among_list(special, arrays):
  for array in arrays:
    if (special == array).all():
      return True
  return False

X = 1
O = -1

possible_winning_rows = [[(r, c) for c in range(3)] for r in range(3)]
possible_winning_columns = [[(r, c) for r in range(3)] for c in range(3)]
main_diagonal = [(r, r) for r in range(3)]
side_diagonal = [(r, 2-r) for r in range(3)]

possible_winning_streaks = possible_winning_rows + possible_winning_columns + [main_diagonal, side_diagonal]

class State:

  def __init__(self, board):
    self.board = board
    self.current_player = self.get_current_player()
    self.winning_streak, self.immediate_result = self.determine_winning_streak()
    # What comes out of .hexdigest() is of type str.
    self.hash = int(hashlib.sha256(str(self.board).encode('utf-8')).hexdigest(), 16)

  def determine_winning_streak(self):
    for possible_winning_streak in possible_winning_streaks:
      sum_of_possibly_winning_token_numbers = sum(self.board[position] for position in possible_winning_streak)
      if sum_of_possibly_winning_token_numbers == 3:
        return possible_winning_streak, X
      if sum_of_possibly_winning_token_numbers == -3:
        return possible_winning_streak, O
    return None, None

  def token_to_player(self, token):
    if token == X: return 'X'
    if token == O: return 'O'

  def get_current_player(self):
    sum_of_all_token_numbers = self.board.sum()
    if sum_of_all_token_numbers > 0:
      return O
    else:
      return X

  def step(self, action):
    next_board = self.board.copy()
    next_board[action] = self.current_player
    next_state = State(next_board)
    return next_state

  def possible_actions(self):

    if self.winning_streak is not None:
      return []

    empty_positions = list(zip(*(self.board == 0).nonzero()))

    distinct_boards = []
    non_reducable_actions = []
    for empty_position in empty_positions:

      next_board = self.board.copy()
      next_board[empty_position] = self.current_player

      # Rotate and reflect the board in all possible ways.
      # There are 8 results of rotations and reflections.
      # All of these can be achieved by concatenating one rotation and one reflection.
      # The rotation will be the counter-clock wise rotation by one corner.
      # The reflection will be along the middle row.
      boards_where_each_state_has_the_same_best_action = []
      states_with_the_same_best_action = []
      for number_of_rotations in range(4):
        rotated_board = numpy.rot90(next_board, k = number_of_rotations)
        reflected_board = numpy.flipud(rotated_board)
        boards_where_each_state_has_the_same_best_action.append(rotated_board)
        boards_where_each_state_has_the_same_best_action.append(reflected_board)

        rotated_state = State(rotated_board)
        reflected_state = State(reflected_board)
        states_with_the_same_best_action.append(rotated_state)
        states_with_the_same_best_action.append(reflected_state)
      hash_minimal_state_with_the_same_best_action = min(states_with_the_same_best_action, key = lambda state: state.hash)
      hash_minimal_board = hash_minimal_state_with_the_same_best_action.board
      if not is_among_list(hash_minimal_board, distinct_boards):
        distinct_boards.append(hash_minimal_board)
        non_reducable_actions.append(empty_position)

    return non_reducable_actions

how_many = 0
class Node:

  def __init__(self, state, parent, last_action):
    self.state = state
    self.last_action = last_action
    self.parent = parent

    self.best_action = None
    self.best_future_result = None

    self.children = dict((action, None) for action in state.possible_actions())

  def get_untried_actions(self):
    untried_actions = [action for action, child_node in self.children.items() if child_node is None]
    return untried_actions

  def get_tried_actions(self):
    tried_actions = [action for action, child_node in self.children.items() if child_node is not None]
    return tried_actions

  def create_root_node():
    state = State(board = numpy.array([
      [0, 0, 0],
      [0, 0, O],
      [0, X, X]
    ]))

    # Try to fetch a node from memory.
    if state.hash in node_from_state_hash:
      return node_from_state_hash[state.hash]

    # Fetching didn't work... create a node,
    node = Node(state, parent=None, last_action=None)

    # then save it into memory,
    node_from_state_hash[state.hash] = node

    # and make it available for use.
    return node

  def create_child_node(self, last_action):

    next_board = self.state.board.copy()
    next_board[last_action] = self.state.current_player
    state = State(next_board)

    # Try to fetch a node from memory.
    if state.hash in node_from_state_hash:
      return node_from_state_hash[state.hash]

    # Fetching didn't work... create a node,
    node = Node(state, self, last_action)

    # then save it into memory,
    node_from_state_hash[state.hash] = node

    # and make it available for use.
    return node

  def expand(self):
    for action in self.children:
      child_node = self.create_child_node(action)
      self.children[action] = child_node

      global how_many
      if how_many < 10000000000000000000:
        child_node.expand()
        print(f'Computed: {how_many} Tic Tac Toe game tree nodes.')
        how_many += 1

        if child_node.children:
          # We initialize the outcome and action that we estimate to be the best possible from this state.
          if self.best_future_result is None:
            self.best_future_result = child_node.best_future_result
            self.best_action = action

          # Maximizer.
          if self.state.current_player == X and child_node.best_future_result > self.best_future_result:
            self.best_future_result = child_node.best_future_result
            self.best_action = action

          # Minimizer.
          if self.state.current_player == O and child_node.best_future_result < self.best_future_result:
            self.best_future_result = child_node.best_future_result
            self.best_action = action

      # Is the child_node a leaf, where we have a winner?
      if child_node.state.immediate_result is not None:

        # We initialize the outcome and action that we estimate to be the best possible from this state.
        if self.best_future_result is None:
          self.best_future_result = child_node.state.immediate_result
          self.best_action = action

        # Maximizer.
        if self.state.current_player == X and child_node.state.immediate_result > self.best_future_result:
          self.best_future_result = child_node.state.immediate_result
          self.best_action = action

        # Minimizer.
        if self.state.current_player == O and child_node.state.immediate_result < self.best_future_result:
          self.best_future_result = child_node.state.immediate_result
          self.best_action = action

      # Is the child_node a leaf, where we have no winner?
      if child_node.state.immediate_result is None and len(child_node.children) == 0:

        # We initialize the outcome and action that we estimate to be the best possible from this state.
        if self.best_future_result is None:
          self.best_future_result = 0
          self.best_action = action

        # Maximizer.
        if self.state.current_player == X and 0 > self.best_future_result:
          self.best_future_result = 0
          self.best_action = action

        # Minimizer.
        if self.state.current_player == O and 0 < self.best_future_result:
          self.best_future_result = 0
          self.best_action = action

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
    representation = ''
    representation += f'state.board: {self.state.board}\n'
    representation += f'state.current_player: {self.state.current_player}\n'
    representation += f'state.hash: {self.state.hash}\n'
    representation += f'best_action: {self.best_action}\n'
    representation += f'best_future_result: {self.best_future_result}\n'
    return representation

  def get_children_hashes_and_actions(self):
    children_hashes = []
    for action, child_node in self.children.items():
      if child_node is not None:
        children_hashes.append((child_node.state.hash, action))
    return children_hashes

  def create_vis_js_json(self):

    if not os.path.exists('nodes'):
      os.mkdir('nodes')

    vis_js_json = {}

    vis_js_json['nodes'] = []
    visualized_how_many = 0
    for state_hash, node in node_from_state_hash.items():
      visualized_how_many += 1
      state_level = node.determine_level()

      # This vis.js configuration applies to this specific node.
      vis_node_declaration = {
        'id': state_hash,
        'level': state_level,
        'image': f'nodes/{node.state.hash}.svg',
        'title': str(node)
      }
      vis_js_json['nodes'].append(vis_node_declaration)

      visualize.create_svg(node)
      print(f'Visualized: {visualized_how_many} Tic Tac Toe game tree nodes.')

    vis_js_json['edges'] = []
    for state_hash, node in node_from_state_hash.items():
      children_hashes = node.get_children_hashes_and_actions()
      for child_hash, action in children_hashes:

        edge_color = '#000000'

        # X gewinnt über diesen Zug.
        if node.best_future_result == X and node.best_action == action:
          edge_color = '#115ab2'
          note = 'X will win'

        # O gewinnt über diesen Zug.
        if node.best_future_result == O and node.best_action == action:
          edge_color = '#b21111'
          note = 'O will win'

        # Keiner gewinnt über diesen Zug.
        if node.best_future_result == 0 and node.best_action == action:
          edge_color = '#9e928a'
          note = 'There will be draw'

        next_board = node.state.board.copy()
        next_board[action] = node.state.current_player
        next_state = State(next_board)
        # Try to fetch a node from memory.
        assert next_state.hash in node_from_state_hash
        next_node = node_from_state_hash[next_state.hash]

        note = None
        if next_node.best_future_result == X:
          note = 'X will win'
        if next_node.best_future_result == O:
          note = 'O will win'
        if next_node.best_future_result == 0:
          note = 'There will be a draw'

        if next_node.state.immediate_result == X:
          note = 'X will win'
        if next_node.state.immediate_result == O:
          note = 'O will win'
        if next_node.state.immediate_result is None and len(next_node.children) == 0:
          note = 'There will be a draw'

        # This vis.js configuration applies to this specific edge.
        vis_edge_declaration = {
          'from': state_hash,
          'to': child_hash,
          'color': edge_color,
          'title': f'htmlTitle("<b>{action}</b>: {note}")'
        }
        vis_js_json['edges'].append(vis_edge_declaration)

    return vis_js_json


start_time = time.time()
node_from_state_hash = {}
root = Node.create_root_node()
root.expand()
vis_js_json = root.create_vis_js_json()
with open('tree_info.js', 'w') as file:
  print('tree_info=', end = '', file=file)
  javascript_code = json.dumps(vis_js_json, indent = 2)

  # Without this, we will not get nice colors in the text that appears,
  # when the user moves the mouse over a game tree node.
  javascript_code = javascript_code.replace('"htmlTitle', 'htmlTitle')
  javascript_code = javascript_code.replace(')"', ')')
  javascript_code = javascript_code.replace('\\"', '"')

  print(javascript_code, end = '', file=file)

print('Computed: Tic Tac Toe game tree.')
print(f'Done in {time.time() - start_time} s.')
