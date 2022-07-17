import datetime
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pickle

from mysoup import get_soup, get_dfs

def get_floattime(s: str) -> float:
    ftime = 0.0
    if type(s) ==str and ":" in s:
        a, b = s.split(":")
        ftime = int(a) * 60 + float(b)
    else:
        ftime = float(s)
    return ftime

def get_boxplot_data(race: tuple) -> tuple:

    racename = race[3]
    course = race[4][0]
    distance = race[4][1:].split("m")[0]
    entry_df = race[-2]
    print(racename, course, distance)

    race_dt = datetime.datetime.strptime(race[0], "%y/%m/%d")

    data = []
    for i in range(len(entry_df)):
        # if i: continue
        umaban = entry_df.loc[i, "馬番"]
        horse = entry_df.loc[i, "馬名"]
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
            row_course, row_distance = row["距離"][0], row["距離"][1:]
            if row_course != course or baba == "不":
                continue
            diff_distance = abs(int(row_distance) - int(distance))
            if diff_distance > 0:
                continue
            # print(row.to_list()[1:15])
            s = row["タイム"]
            f = get_floattime(s)
            ftimes.append(f)
        
        if len(ftimes) > 7:
            ftimes = ftimes[:7]
        print(umaban, horse, ftimes)
        
        median = 999.9
        if ftimes:
            median = np.percentile(ftimes, 50)
        data.append((umaban, median, ftimes))
    
    sorted_data = sorted(data, key=lambda x: x[1])
    if len(data) > 6:
        tmp_data = sorted_data[5][1] # 6th
    else:
        tmp_data = sorted_data[2][1] # 3rd
    plot_data = []
    xlabels = []
    for t in sorted_data:
        times = t[2]
        if t[1] == 999.9:
            times = [tmp_data]
        plot_data.append(times)
        xlabels.append(t[0])
    
    return racename, course, distance, plot_data, xlabels

if __name__ == "__main__":

    p = "./data/jra_220717_updated.pickle"
    with open(p, "rb") as f:
        races = pickle.load(f)

    race = races[8]
    racename, course, distance, plot_data, xlabels = get_boxplot_data(race)

    import warnings
    warnings.simplefilter('ignore', UserWarning)
    # UserWarning: FixedFormatter should only be used together with FixedLocator
    fig, ax = plt.subplots()

    medians = [np.percentile(x, 50) for x in plot_data]
    sixth_time = sorted(medians)[5] 
    third_time = sorted(medians)[2]

    plt.axhline(y=sorted(medians)[5], color="orange", linestyle="--")
    plt.axhline(y=sorted(medians)[2], color="purple", linestyle="--") 

    ax.set_xticklabels(xlabels)
    ax.boxplot(plot_data)
    plt.show()
