from bokeh.models.annotations import Label
from info import info
import bokeh.io
import bokeh.models
import numpy

def create_svg(node):

  # last action
  # so einen dünnen Faden drum herum machen

  plot = bokeh.models.Plot(
    width = 300,
    height = 300,
    output_backend = 'svg',

    # If you comment out this option,
    # the vis.js tree arrows will come too close to the grid part of the Tic Tac Toe board.
    # min_border = 0,

    toolbar_location = None,
    background_fill_alpha = 0,
    outline_line_alpha = 0
  )

  # Orangene Felder: Die noch nicht ausprobierten Züge
  # =====================================================================
  untried_actions = node.get_untried_actions()
  source = bokeh.models.ColumnDataSource({
    'x': [action[1] + 0.5 for action in untried_actions],
    'y': [2 - action[0] + 0.5 for action in untried_actions],
    'w': [1] * len(untried_actions),
    'h': [1] * len(untried_actions)
  })
  glyph = bokeh.models.Rect(
    x = 'x',
    y = 'y',
    width = 'w',
    height = 'h',
    line_alpha = 0,
    fill_color = '#ff8129',
    fill_alpha = 0.5
  )
  plot.add_glyph(source, glyph)
  # =====================================================================

  # Graue Felder: Die bereits ausprobierten Züge
  # =====================================================================
  tried_actions = node.get_tried_actions()
  source = bokeh.models.ColumnDataSource({
    'x': [action[1] + 0.5 for action in tried_actions],
    'y': [2 - action[0] + 0.5 for action in tried_actions],
    'w': [1] * len(tried_actions),
    'h': [1] * len(tried_actions)
  })
  glyph = bokeh.models.Rect(
    x = 'x',
    y = 'y',
    width = 'w',
    height = 'h',
    line_alpha = 0,
    fill_color = '#9e928a',
    fill_alpha = 0.5
  )
  plot.add_glyph(source, glyph)
  # =====================================================================

  # Grünes Feld: Der beste Zug
  # =====================================================================
  if node.best_action is not None:
    source = bokeh.models.ColumnDataSource({
      'x': [node.best_action[1] + 0.5],
      'y': [2 - node.best_action[0] + 0.5],
      'w': [1],
      'h': [1]
    })
    glyph = bokeh.models.Rect(
      x = 'x',
      y = 'y',
      width = 'w',
      height = 'h',
      line_alpha = 0,
      fill_color = '#48f000'
    )
    plot.add_glyph(source, glyph)

    # Grauer Teil: Das beste Resultat
    source = bokeh.models.ColumnDataSource({
      'x': [node.best_action[1] + 0.5],
      'y': [2 - node.best_action[0] + 0.5],
      'w': [0.4],
      'h': [0.1]
    })
    glyph = bokeh.models.Rect(
      x = 'x',
      y = 'y',
      width = 'w',
      height = 'h',
      line_alpha = 0,
      fill_color = '#9e928a'
    )
    plot.add_glyph(source, glyph)

    # Dreieck: Das beste Resultat
    if node.best_outcome == 1:
      source = bokeh.models.ColumnDataSource({
        'x': [node.best_action[1] + 0.5],
        'y': [2 - node.best_action[0] + 0.5 + 0.15],
      })
      triangle = bokeh.models.Scatter(
        x = 'x',
        y = 'y',
        line_alpha = 0,
        fill_color = '#115ab2',
        size = 25,
        angle = 0,
        marker = 'triangle'
      )
      plot.add_glyph(source, triangle)

    if node.best_outcome == -1:
      source = bokeh.models.ColumnDataSource({
        'x': [node.best_action[1] + 0.5],
        'y': [2 - node.best_action[0] + 0.5 - 0.15],
      })
      triangle = bokeh.models.Scatter(
        x = 'x',
        y = 'y',
        line_alpha = 0,
        fill_color = '#b21111',
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
    'w': [0.1, 0.1, 3, 3],
    'h': [3, 3, 0.1, 0.1]
  })
  glyph = bokeh.models.Rect(
    x = 'x',
    y = 'y',
    width = 'w',
    height = 'h',
    fill_color='#646464',
    line_width=0
  )
  plot.add_glyph(source, glyph)
  # =====================================================================

  # Die bereits gemachten Züge auf dem Spielbrett: Der Spielzustand
  # =====================================================================
  for row_index, row in enumerate(node.state.board):
    for column_index, token in enumerate(row):

      if token in [1, -1]:
        draw_symbol = node.state.token_to_player(token)

        color = '#000000'
        if node.last_action == (row_index, column_index):
          color = '#b21111'
        if node.state.winning_streak is not None and (row_index, column_index) in node.state.winning_streak:
          if draw_symbol == 'X':
            color = '#008f0b'
          if draw_symbol == 'O':
            color = '#b21111'

        token_text = Label(
          x = column_index + 0.1,
          y = 2 - row_index - 0.05 * row_index,
          text = draw_symbol,
          text_font_size = '50pt',
          text_color = color
        )
        plot.add_layout(token_text)
  # =====================================================================



  bokeh.io.export_svg(plot, filename=f'nodes/{node.state.hash}.svg')
