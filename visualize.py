from bokeh.models.annotations import Label
from info import info
import bokeh.io
import bokeh.models
import numpy

# last action
# so einen dünnen Faden drum herum machen

state = {
  'board': [
    [-1, -1, 1],
    [-1, -1, 1],
    [0, 0, 0]
  ],
  'current_player': 'O',
  'tried_actions': [
    [2, 0],
    [2, 1],
    [2, 2],
  ],
  'untried_actions': [
  ],
  'best_action': [2, 2],
  'best_outcome': 1
}

# PYTHON HACK: Convert a dict object into a an object where the dict keys are attributes
# See: https://stackoverflow.com/questions/59250557/how-to-convert-a-python-dict-to-a-class-object
# =====================================================================
class ObjectFromDict:
  def __init__(self, dictionary):
    for key, value in dictionary.items():
      setattr(self, key, value)
state = ObjectFromDict(state)
# =====================================================================

assert state.best_action in state.tried_actions

plot = bokeh.models.Plot(
  width = 300,
  height = 300,
  output_backend = "svg",
  min_border = 0,
  toolbar_location = None,
  background_fill_alpha = 0,
  outline_line_alpha = 0
)

# Orangene Felder: Die noch nicht ausprobierten Züge
# =====================================================================
source = bokeh.models.ColumnDataSource({
  'x': [action[1] + 0.5 for action in state.untried_actions],
  'y': [2 - action[0] + 0.5 for action in state.untried_actions],
  'w': [1] * len(state.untried_actions),
  'h': [1] * len(state.untried_actions)
})
glyph = bokeh.models.Rect(
  x = "x",
  y = "y",
  width = "w",
  height = "h",
  line_alpha = 0,
  fill_color = "#ff8129"
)
plot.add_glyph(source, glyph)
# =====================================================================

# Graue Felder: Die bereits ausprobierten Züge
# =====================================================================
source = bokeh.models.ColumnDataSource({
  'x': [action[1] + 0.5 for action in state.tried_actions],
  'y': [2 - action[0] + 0.5 for action in state.tried_actions],
  'w': [1] * len(state.tried_actions),
  'h': [1] * len(state.tried_actions)
})
glyph = bokeh.models.Rect(
  x = "x",
  y = "y",
  width = "w",
  height = "h",
  line_alpha = 0,
  fill_color = "#9e928a"
)
plot.add_glyph(source, glyph)
# =====================================================================

# Grünes Feld: Der beste Zug
# =====================================================================
source = bokeh.models.ColumnDataSource({
  'x': [state.best_action[1] + 0.5],
  'y': [2 - state.best_action[0] + 0.5],
  'w': [1],
  'h': [1]
})
glyph = bokeh.models.Rect(
  x = "x",
  y = "y",
  width = "w",
  height = "h",
  line_alpha = 0,
  fill_color = "#48f000"
)
plot.add_glyph(source, glyph)

# Grauer Teil: Das beste Resultat
source = bokeh.models.ColumnDataSource({
  'x': [state.best_action[1] + 0.5],
  'y': [2 - state.best_action[0] + 0.5],
  'w': [0.4],
  'h': [0.1]
})
glyph = bokeh.models.Rect(
  x = "x",
  y = "y",
  width = "w",
  height = "h",
  line_alpha = 0,
  fill_color = "#9e928a"
)
plot.add_glyph(source, glyph)

# Dreieck: Das beste Resultat
if state.best_outcome == 1:
  source = bokeh.models.ColumnDataSource({
    'x': [state.best_action[1] + 0.5],
    'y': [2 - state.best_action[0] + 0.5 + 0.15],
  })
  triangle = bokeh.models.Scatter(
    x = "x",
    y = "y",
    line_alpha = 0,
    fill_color = "#115ab2",
    size = 25,
    angle = 0,
    marker = 'triangle'
  )
  plot.add_glyph(source, triangle)

if state.best_outcome == -1:
  source = bokeh.models.ColumnDataSource({
    'x': [state.best_action[1] + 0.5],
    'y': [2 - state.best_action[0] + 0.5 - 0.15],
  })
  triangle = bokeh.models.Scatter(
    x = "x",
    y = "y",
    line_alpha = 0,
    fill_color = "#b21111",
    size = 25,
    angle = numpy.pi,
    marker = 'triangle'
  )
  plot.add_glyph(source, triangle)
# =====================================================================

# Das Gitter des Bretts
# =====================================================================
source = bokeh.models.ColumnDataSource({
  'x': [1, 2, 1.5, 1.5],
  'y': [1.5, 1.5, 2, 1],
  'w': [0.2, 0.2, 3, 3],
  'h': [3, 3, 0.2, 0.2]
})
glyph = bokeh.models.Rect(
  x = "x",
  y = "y",
  width = "w",
  height = "h",
  fill_color="#000000"
)
plot.add_glyph(source, glyph)
# =====================================================================

# Die bereits gemachten Züge auf dem Spielbrett: Der Spielzustand
# =====================================================================
for row_index, row in enumerate(state.board):
  for column_index, token in enumerate(row):
    if token in [1, -1]:
      draw_symbol = None
      if token == -1 and state.current_player == 'X':
        draw_symbol = 'O'
      if token == 1 and state.current_player == 'X':
        draw_symbol = 'X'
      if token == -1 and state.current_player == 'O':
        draw_symbol = 'X'
      if token == 1 and state.current_player == 'O':
        draw_symbol = 'O'
      assert draw_symbol is not None

      color = None
      if token == -1:
        color = '#b21111'
      if token == 1:
        color = '#115ab2'

      token_text = Label(
        x = column_index + 0.1,
        y = 2 - row_index - 0.05 * row_index,
        text = draw_symbol,
        text_font_size = '50pt',
        text_color = color
      )
      plot.add_layout(token_text)
# =====================================================================



bokeh.io.export_svg(plot, filename="tic_state.svg")
