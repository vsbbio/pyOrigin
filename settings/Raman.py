# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.

"""
import glob
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

classe = "RAMAN"


def read_save(save_path, main_path, chart_name="Raman_chart", file_type="TXT"):
    paths = glob.glob(f"{main_path}\\*.{file_type}")
    columns=["Sample", "Raman shift", "Intensity (a.u.)"]
    dfd = pd.DataFrame(columns=columns)    
    for f in paths:
        filename = f.split("\\")[-1].split(".")[0]
        with open(f) as file:
            txt = file.readlines()
            list_temp = []
            for row in txt:
                if row != "\n":
                    row_temp = row.replace("\n", "").split("\t")
                    list_temp.append([filename, float(row_temp[0]), float(row_temp[1])])
            
        df_temp = pd.DataFrame(columns=columns, data=list_temp)
        dfd = pd.concat([dfd, df_temp], ignore_index=True)
    

    ################SAVING CHARTS
    fig, ax = plt.subplots()    
    figsize = (10.72,8.205)
    x_max = 1600
    x_min = 350
    per = 100
    
    df = dfd[(dfd[columns[1]] <= x_max) & (dfd[columns[1]] >= x_min)]
    
    gby = df.groupby(columns[0])
    gby.plot(
        title=f"{classe}_{chart_name}",
        x=columns[1],
        y=columns[2],
        xlabel=columns[1],
        ylabel=columns[2],
        figsize=figsize, 
        xlim=(x_min, x_max),
        legend=False,
        ax=ax)    
    
    ax.tick_params(labelleft=False, left=False)
    ax.legend(gby.indices.keys(),loc='upper left', bbox_to_anchor=(-0.01, 1.06),
              ncol=len(gby.indices.keys()))
    
    plt.title(f"{classe}_{chart_name}", loc='center', y=1.08)    
    plt.xticks(np.arange(x_min, x_max, per))    
    
    fig.savefig(f"{save_path}\\{classe}_{chart_name}.png")
    df.to_excel(f"{main_path}\\{classe}_{chart_name}.xlsx", index=True)