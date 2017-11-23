
import numpy as np

import matplotlib.pyplot as plt
from matplotlib.path import Path
from matplotlib.spines import Spine
from matplotlib.projections.polar import PolarAxes
from matplotlib.projections import register_projection

from Drawchart import DrawChart

my_dict = {'Leadership': [5,6], 'Stronghold': [6,4], 'Foo': [3,9], 'Bar' : [5,7], 'Test1' : [6,3], 'Test2' : [7,3]}

fig = DrawChart(my_dict, 'What Makes a leader good', 'Blahchart.pdf')

fig.savefig('Blahchart.pdf')
