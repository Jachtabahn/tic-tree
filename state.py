from bokeh.plotting import figure, curdoc
from bokeh.events import Tap
from bokeh.models import ColumnDataSource, Grid, LinearAxis, Plot, Text


from bokeh.plotting import figure, show

factors = ["foo 123", "bar:0.2", "baz-10"]
x = ["foo 123", "foo 123", "foo 123", "bar:0.2", "bar:0.2", "bar:0.2", "baz-10",  "baz-10",  "baz-10"]
y = ["foo 123", "bar:0.2", "baz-10",  "foo 123", "bar:0.2", "baz-10",  "foo 123", "bar:0.2", "baz-10"]
colors = [
    "#0B486B", "#79BD9A", "#CFF09E",
    "#79BD9A", "#0B486B", "#79BD9A",
    "#CFF09E", "#79BD9A", "#0B486B"
]

plot = figure(title="Categorical Heatmap", tools="hover", toolbar_location=None,
           x_range=factors, y_range=factors)

r = plot.rect(x, y, color=colors, width=1, height=1)

from info import info
import numpy

glyph = Text(x="x", y="y", text="text", text_color="#96deb3", text_font_size='6cm')

def callback(event):
    info(event)
    info(dir(event))

    x = [event.x]
    y = [event.y]
    text = ['X']
    info(x)
    info(y)
    source = ColumnDataSource(dict(x=x, y=y, text=text))
    plot.add_glyph(source, glyph)

plot.on_event(Tap, callback)

curdoc().add_root(plot)
