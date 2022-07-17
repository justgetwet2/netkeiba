import datetime
import itertools
import numpy as np
import pandas as pd
import pickle
import tkinter as tk
import tkinter.ttk as ttk
import re
import requests

from odds_update import netkeiba_odds

# from mysoup import get_soup, get_dfs, netkeiba_url

# from tkhorse import AppHorse
from tkplot import AppPlot
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

        self.master.resizable(width=False, height=False)
        self.bgcolor = self.master.cget("background")
        style = ttk.Style()
        style.theme_use("classic")
        style.configure("c.TButton", borderwidth=0, background=self.bgcolor)
        
        self.race = race 
        self.master.title(" ".join(race[1:5]))

        self.entry_df = race[-2]
        self.head_count = len(self.entry_df)
        self.race_id = race[-3]
        self.odds_d = {}

        self.frame_left = tk.Frame(self, padx=8, pady=8)
        self.frame_left.pack(side=tk.LEFT)
        self.frame_upper_left = tk.Frame(self.frame_left, pady=8)
        self.frame_upper_left.pack(anchor=tk.NW)
        self.frame_middle_left = tk.Frame(self.frame_left)
        self.frame_middle_left.pack(anchor=tk.NW)
        self.frame_lower_left = tk.Frame(self.frame_left, width=300, height=100)
        self.frame_lower_left.pack()

        self.frame_right = tk.Frame(self, width=200, height=300)
        self.frame_right.pack()

        self.set_odds_variable()
        self.create_frame_buttons()
        self.create_frame_entry()

    def set_odds_variable(self):
        self.win_oddses = [tk.StringVar(value="") for _ in range(self.head_count)]
        self.place1_oddses = [tk.StringVar(value="") for _ in range(self.head_count)]
        self.place2_oddses = [tk.StringVar(value="") for _ in range(self.head_count)]

    def set_odds(self):
        if not self.odds_d:
            return 
        w_oddses = [self.odds_d[str(i+1)] for i in range(self.head_count)]
        p1_oddses = [self.odds_d["(" + str(i+1)] for i in range(self.head_count)]
        p2_oddses = [self.odds_d[str(i+1) + ")"] for i in range(self.head_count)]
        for i, (win, place1, place2) in enumerate(zip(w_oddses, p1_oddses, p2_oddses)):
            self.win_oddses[i].set(win)
            self.place1_oddses[i].set(place1)
            self.place2_oddses[i].set(place2)

    def update(self):
        self.odds_d = netkeiba_odds(self.race_id)
        self.set_odds()

    def create_frame_buttons(self):
        frame_buttons = tk.Frame(self.frame_upper_left)
        update_button = ttk.Button(
            frame_buttons, 
            text="update",
            style="c.TButton",
            command=lambda: self.update(),
            state=tk.NORMAL,
        )
        plot_button = ttk.Button(
            frame_buttons, 
            text="bplot",
            style="c.TButton",
            command=lambda: self.plot_window(),
            state=tk.NORMAL,
        )
        # if not self.odds_d == {}:
        #     update_button["state"] = tk.DISABLED
        update_button.pack(side=tk.LEFT, padx=4)
        # entry_button.pack(side=tk.LEFT, padx=4)
        plot_button.pack(side=tk.LEFT, padx=4)
        # calc_button.pack(side=tk.LEFT, padx=4)
        # reslut_button.pack(padx=4)

        frame_buttons.pack(anchor=tk.W)

    def create_frame_entry(self):
        frame_entry = tk.Frame(self.frame_middle_left)
        for i, row in self.entry_df.iterrows():
            wakban, umaban, horse, jockey = row["枠番"], row["馬番"], row["馬名"], row["騎手"]
            frame_horses = tk.Frame(frame_entry)
            lbl_wakban = tk.Label(frame_horses, text=wakban, width=2, anchor=tk.E)
            lbl_umaban = tk.Label(frame_horses, text=umaban, width=2, anchor=tk.E)
            lbl_horse = tk.Label(frame_horses, text=horse, width=16, padx=8, anchor=tk.W)
            # label_horse.bind("<1>", self.horse_window)
            lbl_jockey = tk.Label(frame_horses, text=jockey, width=8, padx=8, anchor=tk.W)
            # label_jockey.bind("<1>", self.jockey_window)
            lbl_win_odds = tk.Label(frame_horses, textvariable=self.win_oddses[i], width=6, anchor=tk.E)
            lbl_place1_odds = tk.Label(frame_horses, textvariable=self.place1_oddses[i], width=5, anchor=tk.E)
            lbl_bar = tk.Label(frame_horses, text="-", width=3, anchor=tk.E)
            lbl_place2_odds = tk.Label(frame_horses, textvariable=self.place2_oddses[i], width=5, anchor=tk.E)
            lbl_wakban.pack(side=tk.LEFT)
            lbl_umaban.pack(side=tk.LEFT)
            lbl_horse.pack(side=tk.LEFT)
            lbl_jockey.pack(side=tk.LEFT)
            lbl_win_odds.pack(side=tk.LEFT)
            lbl_place1_odds.pack(side=tk.LEFT)
            lbl_bar.pack(side=tk.LEFT)
            lbl_place2_odds.pack()
            frame_horses.pack(anchor=tk.NW)

        frame_entry.pack()
        
    def plot_window(self):
        root = tk.Toplevel(self)
        app = AppPlot(self.race, master=root)
        app.mainloop()

if __name__ == "__main__":

    p = "./data/jra_220716_updated.pickle"
    with open(p, "rb") as f:
        races = pickle.load(f)

    race = races[10]
    root = tk.Tk()
    app = AppRace(race, master=root)
    app.mainloop()
