"""
======================================
Radar chart (aka spider or star chart)
======================================

This example creates a radar chart, also known as a spider or star chart [1]_.

Although this example allows a frame of either 'circle' or 'polygon', polygon
frames don't have proper gridlines (the lines are circles instead of polygons).
It's possible to get a polygon grid by setting GRIDLINE_INTERPOLATION_STEPS in
matplotlib.axis to the desired number of vertices, but the orientation of the
polygon is not aligned with the radial axes.

.. [1] http://en.wikipedia.org/wiki/Radar_chart
"""
import numpy as np
import xlrd
import matplotlib.pyplot as plt
from matplotlib.path import Path
from matplotlib.spines import Spine
from matplotlib.projections.polar import PolarAxes
from matplotlib.projections import register_projection

def DrawChart(mydict, title, save):
    
    def radar_factory(num_vars, frame='circle'):
        """Create a radar chart with `num_vars` axes.

        This function creates a RadarAxes projection and registers it.

        Parameters
        ----------
        num_vars : int
            Number of variables for radar chart.
        frame : {'circle' | 'polygon'}
        Shape of frame surrounding axes.

    """
    # calculate evenly-spaced axis angles
        theta = np.linspace(0, 2*np.pi, num_vars, endpoint=False)
    # rotate theta such that the first axis is at the top
        theta += np.pi/2

        def draw_poly_patch(self):
            verts = unit_poly_verts(theta)
            return plt.Polygon(verts, closed=True, edgecolor='k')

        def draw_circle_patch(self):
            # unit circle centered on (0.5, 0.5)
            return plt.Circle((0.5, 0.5), 0.5)

        patch_dict = {'polygon': draw_poly_patch, 'circle': draw_circle_patch}
        if frame not in patch_dict:
            raise ValueError('unknown value for `frame`: %s' % frame)

        class RadarAxes(PolarAxes):

            name = 'radar'
        # use 1 line segment to connect specified points
            RESOLUTION = 1
        # define draw_frame method
            draw_patch = patch_dict[frame]

            def fill(self, *args, **kwargs):
            #"""Override fill so that line is closed by default"""
                closed = kwargs.pop('closed', True)
                return super(RadarAxes, self).fill(closed=closed, *args, **kwargs)

            def plot(self, *args, **kwargs):
  #          """Override plot so that line is closed by default"""
                lines = super(RadarAxes, self).plot(*args, **kwargs)
                for line in lines:
                    self._close_line(line)

            def _close_line(self, line):
                x, y = line.get_data()
                # FIXME: markers at x[0], y[0] get doubled-up
                if x[0] != x[-1]:
                    x = np.concatenate((x, [x[0]]))
                    y = np.concatenate((y, [y[0]]))
                    line.set_data(x, y)

            def set_varlabels(self, labels):
                self.set_thetagrids(np.degrees(theta), labels)

            def _gen_axes_patch(self):
                return self.draw_patch()

            def _gen_axes_spines(self):
                if frame == 'circle':
                    return PolarAxes._gen_axes_spines(self)

                spine_type = 'circle'
                verts = unit_poly_verts(theta)
            # close off polygon by repeating first vertex
                verts.append(verts[0])
                path = Path(verts)

                spine = Spine(self, spine_type, path)
                spine.set_transform(self.transAxes)
                return {'polar': spine}

        register_projection(RadarAxes)
        return theta


    def unit_poly_verts(theta):
        """Return vertices of polygon for subplot axes.

        This polygon is circumscribed by a unit circle centered at (0.5, 0.5)
        """
        x0, y0, r = [0.5] * 3
        verts = [(r*np.cos(t) + x0, r*np.sin(t) + y0) for t in theta]
        return verts

    
    def getAvg(list):
        value = 0
        for i in list:
            value = value + i
        return value/float(len(list))
    
    def ideal():
        ideal_list = list()
        for key in mydict:
            ideal_list.append(mydict[key][0])

        return ideal_list
    
    def example_data():
        #var, var2, var3, var4, var5, var6 = input()
        attribute = list()
        
        for key in mydict:
            attribute.append(key)

        mylist = list()

        for key in mydict:
            mylist.append(mydict[key][1])
        
        ideal_list = ideal()

        total = getAvg(mylist)
        ideal_num = getAvg(ideal_list)

        attribute_arr = np.array(attribute)
        mylist_arr = np.array(mylist)

        ideal_list_arr = np.array(ideal_list)
        
        data = [attribute,(title, [mylist, ideal_list])]
        
         
        return data


    if __name__ == '__main__':
        N = int(len(mydict))

        theta = radar_factory(N, frame='polygon')

        data = example_data()
        spoke_labels = data.pop(0)

        fig, axes = plt.subplots(figsize=(9, 9), nrows=1, ncols=1,
                                 subplot_kw=dict(projection='radar'))
        #fig.subplots_adjust(wspace=0.25, hspace=0.20, top=0.85, bottom=0.05)

        colors = ['b', 'r', 'g', 'm', 'y']
        # Plot the four cases from the example data on separate axes
        for ax, (title, case_data) in zip(range(1), data):
            axes.set_rgrids([1, 2, 3, 4,5, 6,7, 8, 9,10])
            axes.set_title(title, weight='bold', size='medium', position=(0.5, 1.1),
                         horizontalalignment='center', verticalalignment='center')
            for d, color in zip(case_data, colors):
                axes.plot(theta, d, color=color)
                axes.fill(theta, d, facecolor=color, alpha=0.25)
            axes.set_varlabels(spoke_labels)

        # add legend relative to top-left plot
        #ax = axes[0, 0]
        labels = ('Your Chart', 'Ideal Chart')
        legend = axes.legend(labels, loc=(0.9, .95),
                           labelspacing=0.1, fontsize='small')


        plt.savefig(save)


class AttributeInfo:
    Attribute_name = ""
    IdealVal = 0
    Val = 0


Test = AttributeInfo()

Test.Attribute_name = "Hi"
Test.IdealVal = 3
Test.Val = 4

print(Test.Attribute_name)
print(Test.IdealVal)
print(Test.Val)

#my_dict = {'Leadership': [5,6], 'Stronghold': [6,4], 'Foo': [3,9], 'Bar' : [5,7], 'Test1' : [6,3], 'Test2' : [7,3]}

dicts = {}

workbook = xlrd.open_workbook("testinfo.xlsx")
worksheet = workbook.sheet_by_index(0)

rows = worksheet.nrows

cols = worksheet.ncols

names = list()
ideal = list()
value = list()

for i in range(rows):
    for j in range(cols):
        if i == 0:
            names.append(format(worksheet.cell(i,j).value))

        elif i == 1:
            ideal.append(format(worksheet.cell(i,j).value))

        elif i == 2:
            value.append(format(worksheet.cell(i,j).value))

for i in range(cols):
    name = names[i]
    idea = ideal[i]
    val = value[i]

    dicts[name] = [idea, val]

print(dicts)

#DrawChart(my_dict, 'What Makes a leader good', 'Blahchart.pdf')


