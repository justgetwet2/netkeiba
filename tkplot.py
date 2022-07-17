ua = {"User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 Edg/96.0.1054.57"}
from bs4 import BeautifulSoup
import pandas as pd
import pickle
import tkinter as tk
import tkinter.ttk as ttk
import requests
import warnings

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.font_manager as fm
fpath = "./fonts/Hiragino-Sans-GB-W3.ttf"
fprop = fm.FontProperties(fname=fpath, size=10)
import numpy as np

from plot_data import get_boxplot_data

# time_d = {
#     800: 48.12,
#     900: 54.92,
#     1000: 60.76,
#     1200: 74.78,
#     1300: 84.78,
#     1400: 90.49,
#     1500: 97.38,
#     1600: 102.91,
#     1650: 105.57,
#     1700: 108.89,
#     1800: 114.86,
#     2000: 132.57,
#     2100: 135.3,
#     2200: 146.94,
#     2400: 157.2,
#     2600: 167.1
# }

class AppPlot(tk.Frame):
    def __init__(self, race, master=None):
        super().__init__(master)
        self.pack()

        racename, course, distance, plot_data, xlabels = get_boxplot_data(race)

        # self.master.title(racename)

        warnings.simplefilter('ignore', UserWarning)
        fig, ax = plt.subplots()
        
        # win_time = time_d[dist]
        # if dist > 1000:
        #     win_time = win_time - 60.
        
        # ax.set_ylim(win_time - 6., win_time + 9.)
        ax.set_title(racename, fontproperties=fprop)
        ax.set_xticklabels(xlabels)
        ax.boxplot(plot_data)

        last_times = [x[0] for x in plot_data]
        ax.plot(range(1, len(xlabels)+1), last_times, "o")

        medians = [np.percentile(x, 50) for x in plot_data]
        if len(medians) > 6:
            ax.axhline(y=sorted(medians)[5], color="y", linestyle="--")
        ax.axhline(y=sorted(medians)[2], color="m", linestyle="--")
        # ax.axhline(y=win_time, color="r", linestyle="--")

        canvas = FigureCanvasTkAgg(fig, master)  # Generate canvas instance, Embedding fig in root
        canvas.draw()
        canvas.get_tk_widget().pack()


if __name__ == "__main__":

    p = "./data/jra_220717_updated.pickle"
    with open(p, "rb") as f:
        races = pickle.load(f)
    
    race = races[10]

    root = tk.Tk()
    app = AppPlot(race, master=root)
    app.mainloop()