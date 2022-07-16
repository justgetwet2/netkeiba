import datetime
import itertools
import numpy as np
import pandas as pd
import pickle
import tkinter as tk
import tkinter.ttk as ttk
import re
import requests

from mysoup import get_soup, get_dfs, netkeiba_url

# from tkhorse import AppHorse
# from tkplot import AppPlot
# from tkentry import AppEntry
# from tkcalc import AppCalc
# from tkresult import AppResult

# # from scrape_odds import odds_dict
# from odds_dict import OddsDict
# from synthetic_odds import SyntOdds

class AppRace(tk.Frame):
    def __init__(self, race, master=None):
        super().__init__(master)
        self.pack()

        self.race = race 
        self.master.title(" ".join(race[1:5]))

        tk.Frame(self, width=600, height=300).pack()