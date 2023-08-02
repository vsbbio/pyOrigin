# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.

"""
import glob
import pandas as pd
import matplotlib.pyplot as plt

classe = "GRAN"

def read_save(save_path, main_path, chart_name="GRAN_chart", file_type="TXT"):
    paths = glob.glob(f"{main_path}\\*.{file_type}")
    columns=["Sample", "Tamanho de partícula (μm)", "Normal", "Logarítimica"]
    df = pd.DataFrame()    
    for f in paths:
        filename = f.split("\\")[-1].split(".")[0]
        with open(f) as file:
            txt = file.readlines()
            list_temp = []
            for row in txt:
                if row != "\n":
                    row_temp = row.split(",")
                    list_temp.append([filename, float(row_temp[0])/1000, float(row_temp[1]), float(row_temp[2])])
            
        df_temp = pd.DataFrame(columns=columns, data=list_temp)
        df = pd.concat([df, df_temp], ignore_index=True)
    

    ################SAVING CHARTS
    fig, ax = plt.subplots()    
    figsize = (10.72,8.205)
    
    gby = df.groupby(columns[0])    
    gby.plot(
        title=f"{classe}_{chart_name}",
        x=columns[1],
        y=columns[2],
        xlabel=columns[1],
        ylabel="Volume (%)",
        figsize=figsize, 
        legend=False,
        ax=ax)
        
    ax.tick_params(labelleft=False, left=False)
    ax.legend(gby.indices.keys(),loc='upper left', bbox_to_anchor=(-0.01, 1.06),
              ncol=len(gby.indices.keys()))
    
    plt.title(f"{classe}_{chart_name}", loc='center', y=1.08)    
    fig.savefig(f"{save_path}\\{classe}_NORM_{chart_name}.png")
    df.to_excel(f"{main_path}\\{classe}_{chart_name}.xlsx", index=True)

    fig, ax = plt.subplots()
    gby.plot(
        title=f"{classe}_{chart_name}",
        x=columns[1],
        y=columns[3],
        xlabel=columns[1],
        ylabel="Volume (%)",
        figsize=figsize, 
        legend=False,
        ax=ax)
        
    ax.tick_params(labelleft=False, left=False)
    ax.legend(gby.indices.keys(),loc='upper left', bbox_to_anchor=(-0.01, 1.06),
              ncol=len(gby.indices.keys()))
    
    plt.title(f"{classe}_{chart_name}", loc='center', y=1.08)    
    fig.savefig(f"{save_path}\\{classe}_LOG_{chart_name}.png")
    
   