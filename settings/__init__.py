# -*- coding: utf-8 -*-
"""
Created on Thu Jul 27 01:38:38 2023

@author: ARAUJO.MARIANA
"""

from core.DRX_OFFSET import read_save as drx
from core.DTA import read_save as dta
from core.FTIR import read_save as ftir
from core.GRAN import read_save as gran
from core.Raman import read_save as raman
from core.TGA import read_save as tga


charts = dict(
       DRX=drx,
       DTA=dta,
       FTIR=ftir,
       GRANULOMETRIA=gran,
       RAMAN=raman,
       TGA=tga
       )