import matplotlib.pyplot as plt
import numpy as np

import datetime
import pickle
import tkinter as tk
import tkinter.ttk as ttk

from mysoup import get_soup, get_dfs

def get_floattime(s):
    ftime = 0.0
    if type(s) ==str and ":" in s:
        a, b = s.split(":")
        ftime = int(a) * 60 + float(b)
    else:
        ftime = float(s)
    return ftime

if __name__ == "__main__":

    p = "./data/jra_220717_updated.pickle"
    with open(p, "rb") as f:
        races = pickle.load(f)

    race = races[7]
    print(race[:-2])
    surface = race[4][0]
    distance = race[4][1:].split("m")[0]
    print(surface, distance)

    race_dt = datetime.datetime.strptime(race[0], "%y/%m/%d")

    entry_df = race[-2]
    plot_data = []
    for i in range(len(entry_df)):
        # if i: continue
        print(entry_df.loc[i, "馬名"])
        url = entry_df.loc[i, "馬url"]
        dfs = get_dfs(url)
        dfs = [df for df in dfs if df.columns[0] == "日付"]
        df = dfs[0]
        ftimes = []
        for j, row in df.iterrows():
            # if j: continue
            row_dt = datetime.datetime.strptime(row["日付"], "%Y/%m/%d")
            td = race_dt - row_dt
            if td.days < 1:
                continue
            baba = row["馬\u0020\u0020場"]
            row_surface, row_distance = row["距離"][0], row["距離"][1:]
            if row_surface != surface or baba == "不":
                continue
            diff_distance = abs(int(row_distance) - int(distance))
            if diff_distance > 0:
                continue
            # print(row["人\u0020\u0020気"])
            # print(row.to_list()[1:15])
            s = row["タイム"]
            f = get_floattime(s)
            ftimes.append(f)
        if not ftimes:
            ftimes = [100.0]
        plot_data.append(ftimes)

    fig, ax = plt.subplots()
    ax.boxplot(plot_data)
    plt.show()
