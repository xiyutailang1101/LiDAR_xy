import opals
from opals import Import, Bounds
import os, csv
# By convention, we abbreviate matplotlib as mpl
import matplotlib as mpl
# select the graphics kit to use
mpl.use("TkAgg")
# import does not work recursively,
# so we need to import the sub-module, too.
# By convention, we name it plt.
import matplotlib.pyplot as plt

# change the working to the OPALS demo directory
os.chdir(os.path.join(opals.__path__[0], r'..\demo'))

hatches = ["/", "\\", "|", "-", "+", "x", "o"]
colors = ["b", "g", "r", "c", "m", "y", "k"]

# loop 3 lists at the same time
# built in function 'zip' returns a list of tuples
# where the i-th tuple contains the i-th element of each of the sequences passed as arguments to 'zip'
# the shortest list determines the number of loops

for dataset, hatch, color in zip(["G111", "G112", "G113"], hatches, colors):
    dataFn = dataset + ".las"
    odmFn = dataset + ".odm"
    boundsFn = dataset + "_bounds.xyz"

    imp = Import.Import()
    imp.inFile = dataFn
    imp.run()

    bnds = Bounds.Bounds()
    bnds.inFile = odmFn

    # set the boundary type to result in a tight fit
    # use the enumerator 'alphaShape' of the enumeration 'BoundaryType'
    bnds.boundsType = opals.Types.BoundaryType.alphaShape
    bnds.outFile = boundsFn
    bnds.run()

    # csv reader is an iterable object, reading a line of a text on each iteration
    # and returning another object that 'iterates over' the line split into tokens
    x, y = [], []
    with open(boundsFn) as fin:
        reader = csv.reader(fin, delimiter=' ', skipinitialspace=True)
        for line in reader:
            x.append(float(line[0]))
            y.append(float(line[1]))
    # plot a polygon using the lists of x and y, no fill but edges and a hatch
    plt.fill(x, y, hatch=hatch, color=color, fill=False, linewidth=2, label=dataset)

# Label the axis
plt.title('Strip boundaries')
plt.xlabel('Easting [m]')
plt.ylabel('Northing [m]')

# Insert a legend. Use defaults i.e.
# all plot-handles of the axis,
# with labels as specified in plt.fill(..).
plt.legend()
# Ensure equal scales for both coordinates.
plt.axis('scaled')
# Actually draw the figure.
plt.show()
