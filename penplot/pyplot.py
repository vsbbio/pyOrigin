# -*- coding: utf-8 -*-

from matplotlib import rcParams, cycler
from configparser import ConfigParser
from scipy import signal
from glob import glob
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import PySimpleGUI as sg

print = sg.cprint

config = ConfigParser()

def plot(args):
    master_path = args["master_path"]
    version = args["version"]
    master_folders = glob(rf"{master_path}\*")
    for mf in master_folders:
        subclasse = mf.split("\\")[-1].upper()
        if args.get(subclasse, False):
            print(f"\nCONFIGURAÇÃO: {subclasse.upper()}")
            folders = glob(fr"{mf}\*")            
            for folder in folders:
                chart_name = folder.split("\\")[-1]
                plot = Matplotin()
                plot.run(master_path, folder, subclasse, chart_name, version)
    print("PROGRAMA FINALIZADO")
        

class Matplotin:
    def __init__(self, style=r"penplot\style.ini"):
        config.read(style, encoding="utf8")
        self.params = eval(config["origin"]["ELM"])
        self.figure = eval(config["origin"]["FIG"])
        self.colors = config["origin"]["COLOR"].split("\n")
        self.plt = plt
        
        for e in self.params:
            rcParams[e] = self.params[e]        
        rcParams["axes.prop_cycle"] = cycler("color", self.colors)
        rcParams.update(self.figure)
        
    def run(self, save_path, main_path, subclasse, chart_name, version):
        self.save_path = save_path
        self.main_path = main_path
        self.subclasse = subclasse
        self.version = version
        self.chart_name = chart_name
        self.__config__()
        self.__read__()
        self.__plot__()
        self.__save__()
        
    
    def __config__(self):
        config.read(rf"configs\{self.subclasse}.ini", encoding="utf8")
        cp = config["DEFAULT"]
        self.file_type = cp["EXTENSION"]
        self.start_row = int(cp["START_ROW"]) - 1
        self.idx_cols = []
        for c in cp["COLUMNS"].split(","):
            self.idx_cols.append(int(c) - 1)
        self.div_cols = []
        for d in cp["COL_DIV"].split(","):
            self.div_cols.append(int(d))        
        self.columns = []
        for n in cp["COL_NAMES"].split(","):
            self.columns.append(n)
        self.sep = str(cp["SEPARATOR"]).replace('"', '').replace("\\n","\n").replace("\\t","\t")
        self.reps = cp["REPLACES"].split(",")
        self.x_invert= True if cp["X_INVERT"] == "True" else False
        self.x_limit = True if cp["X_LIMIT"] == "True" else False
        self.x_max = int(cp["X_MAX"])
        self.x_min= int(cp["X_MIN"])
        self.x_per= int(cp["X_PER"])
        self.y_label= True if cp["Y_LABEL"] == "True" else False
        self.y_col = int(cp["Y_COLUMN"]) - 1
        self.y_label_axis= True if cp["Y_LABEL_AXIS"] == "True" else False
        self.y_invert= True if cp["Y_INVERT"] == "True" else False
        self.y_limit= True if cp["Y_LIMIT"] == "True" else False
        self.y_max= int(cp["Y_MAX"])
        self.y_min= int(cp["Y_MIN"])
        self.y_per= int(cp["Y_PER"])
        self.y_offset= True if cp["Y_OFFSET"] == "True" else False
        self.y_smooth = True if cp["Y_SMOOTH"] == "True" else False
        self.y_smooth_window_lenght = cp["Y_SMOOTH_WINDOW_LENGHT"]
        self.y_smooth_polyorder = cp["Y_SMOOTH_POLYORDER"]
        self.y_smooth_mode = cp["Y_SMOOTH_MODE"]
   
    
    def __read__(self):               
        paths = glob(f"{self.main_path}\\*.{self.file_type}")
        self.df = pd.DataFrame(columns=self.columns)    
        for f in paths:
            filename = f.split("\\")[-1].split(".")[0]
            with open(f) as file:
                txt = file.readlines()
                list_temp = []
                for row in txt[self.start_row:]:
                    if row != "\n":
                        for c in self.reps:
                            c = c.replace('"', '').replace("\\n","\n").replace("\\t","\t")
                            row_temp = row.replace(c,"")
                        
                        row_temp = row_temp.split(self.sep)
                        temp = [filename]
                        for i in range(0, len(self.idx_cols)):
                            val = float(row_temp[self.idx_cols[i]])
                            div = self.div_cols[i]
                            temp.append(val/div)
                        list_temp.append(temp)
                        
            df_temp = pd.DataFrame(columns=self.columns, data=list_temp)
            self.df = pd.concat([self.df, df_temp], ignore_index=True)
    
    def __plot__(self):        
        self.fig, self.ax = plt.subplots()    
        
        if self.x_limit:
            df = self.df[(self.df[self.columns[1]] <= self.x_max) & 
                         (self.df[self.columns[1]] >= self.x_min)
                         ].copy()
            plt.xticks(np.arange(self.x_min, self.x_max, self.x_per))
            
        else:
            df = self.df.copy()    
        
        if self.y_offset:
            offset = 0
            df_t = pd.DataFrame()
            for k in list(df[self.columns[0]].unique()):
                df_temp = df[df[self.columns[0]] == k].copy()
                df_temp[f"Offset {self.columns[self.y_col]}"] = df_temp[self.columns[self.y_col]] + offset
                df_t = pd.concat([df_t, df_temp], ignore_index=True)
                offset = max(df_temp[f"Offset {self.columns[self.y_col]}"])
            
            df[f"Offset {self.columns[self.y_col]}"] = df_t[f"Offset {self.columns[self.y_col]}"]
        
        if self.y_smooth:
            self.y_col = signal.savgol_filter(self.y_col, 
                                              window_length=self.y_smooth_window_lenght,
                                              polyorder=self.y_smooth_polyorder,
                                              mode=self.y_smooth_mode
                                              )
            
        gby = df.groupby(self.columns[0])    
        gby.plot(
            title=f"{self.subclasse}_{self.chart_name}",
            x=self.columns[1],
            y= f"Offset {self.columns[self.y_col]}" if self.y_offset else self.columns[self.y_col],
            xlabel=self.columns[1],
            ylabel=self.columns[self.y_col],
            legend=False,
            ax=self.ax)    
        
        if self.x_invert:
            self.ax.invert_xaxis()
        
        if self.y_invert:
            self.ax.invert_yaxis()        
        
        self.ax.tick_params(labelleft=self.y_label_axis, left=self.y_label)
        self.ax.legend(gby.indices.keys(),
                       loc='upper left',
                       bbox_to_anchor=(-0.01, 1.08),
                       ncol=len(gby.indices.keys()),
                       fancybox=True,
                       framealpha=0.0)
        
    def __save__(self):
        self.fig.tight_layout()
        self.fig.savefig(f"{self.save_path}\\{self.subclasse}_{self.chart_name}_{self.version}.png", dpi=300)
        self.df.to_excel(f"{self.main_path}\\{self.subclasse}_{self.chart_name}.xlsx", index=True)
        plt.close()
        print(f">> Gráfico: {self.chart_name} - OK")