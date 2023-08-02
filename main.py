# -*- coding: utf-8 -*-
"""
Created on Thu Jul 27 01:41:58 2023

@author: ARAUJO.MARIANA
"""
from penplot.pyplot import Matplotin
from glob import glob

def main():
    folder_input = input("Caminho da pasta: ")
    version = input("Controle de data/versão: ")
    master_folders = glob(fr"{folder_input}\*")
    
    for mf in master_folders:
        subclasse = mf.split("\\")[-1].upper()
        folders = glob(fr"{mf}\*")            
        for folder in folders:
            chart_name = folder.split("\\")[-1]
            plot = Matplotin()
            plot.run(folder_input, folder, subclasse, f"{chart_name}_{version}")
            
main()