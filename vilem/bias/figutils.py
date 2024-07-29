COLORS = [
    "#b22",  # red
    "#3a5",  # green
    "#00a",  # blue
    "#ec1",  # yellow
]


import matplotlib as mpl
import matplotlib.pyplot as plt
import os

os.makedirs("computed/", exist_ok=True)

mpl.rcParams["axes.prop_cycle"] = plt.cycler(color=COLORS)
mpl.rcParams["legend.fancybox"] = False
mpl.rcParams["legend.edgecolor"] = "None"
mpl.rcParams["legend.fontsize"] = 9
mpl.rcParams["legend.borderpad"] = 0.1
mpl.rcParams["legend.labelspacing"] = 0.2