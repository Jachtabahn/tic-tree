import numpy as np

from bokeh.io import curdoc, show, export_svg
from bokeh.models import ColumnDataSource, Grid, LinearAxis, Plot, Rect
from bokeh.layouts import row
from bokeh.colors import RGB
from bokeh.models.annotations import Label


state = {
  "board": [
    [-1, 1, -1],
    [0, -1, 1],
    [0, 1, 0]
  ],
  "current_player": "O",
  "tried_actions": [
    [1, 0],
    [2, 2]
  ],
  "untried_actions": [
    [2, 0]
  ],
  "best_action": [1, 0],
  "best_outcome": -0.2
}

x = [1, 2, 1.5, 1.5]
y = [1.5, 1.5, 2, 1]
w = [0.2, 0.2, 3, 3]
h = [3, 3, 0.2, 0.2]

source = ColumnDataSource(dict(x=x, y=y, w=w, h=h))

plot = Plot(
    title=None, width=300, height=300,
    min_border=0, toolbar_location=None, output_backend="svg")

glyph = Rect(x="x", y="y", width="w", height="h", fill_color="#cab2d6")
plot.add_glyph(source, glyph)

mytext = Label(x=0, y=-0.1, text='X', text_font_size='50pt')
plot.add_layout(mytext)

mytext = Label(x=1.1, y=1, text='O', text_font_size='50pt')
plot.add_layout(mytext)

mytext = Label(x=0, y=2, text='X', text_font_size='50pt')
plot.add_layout(mytext)

plot.axis.visible = False
plot.grid.visible = False
plot.background_fill_alpha = 0

export_svg(plot, filename="tic_state.svg")

# manipulate SVG by removing the first <path> object
