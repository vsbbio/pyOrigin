# -*- coding: utf-8 -*-
from getpass import getuser
from pathlib import Path
from penplot.pyplot import plot
import datetime as dt
import PySimpleGUI as sg
import threading

print = sg.cprint

APP_NAME="PYORIGIN"
VERSION =  '0.0.3'
THEME = "Reddit"
CONTEXTO = "> MAIN"
WINDOW_SIZE=(1366,768)
SBU = (13,1)
SCB = (10,1)
STX = (18,1)
SIT = (25,1)
SLG = (150, 63)


def get_frame(names, columns=1):
    frame = [[]]
    qty = len(names)
    for idx in range(0, qty):
        if (idx+1)%columns == 0:
            frame.append([])
        col = sg.Column([[sg.Checkbox(names[idx], 
                                    key=f"{names[idx]}",
                                    default=True, 
                                    size=SBU)
                                ]], 
                            vertical_alignment='bottom',
                            element_justification='left', pad=((8,0), (0,0))
                        )
        frame[len(frame)-1].append(col)             
    return frame

def main():
    
    sg.theme(THEME)

    options = get_frame(list(path.stem for path in Path(r".\configs").glob("*.ini")))
    
    data = [[
            sg.Column([[sg.Text('Caminho Pasta', size=STX)]]),            
            sg.Column([[sg.InputText(key="master_path", size=(75,1), default_text=f"C:\\Users\\{getuser()}\\AppData\\Local", justification='right'),
                      sg.FolderBrowse(size=SBU)]]),
            sg.Column([[sg.Button('ALOHOMORA', key="-RUN-MAIN-", enable_events=True, size=SBU)]])
            ]]
    
    frame_top = [sg.Frame('', data, title_color='black', size=(1066,50))
                    ]
    frame_lef = [sg.Frame('', options, title_color='black', size=(200,768))
                    ]    
    frame_dow = [
                sg.Multiline(f" {APP_NAME} {VERSION}\n POWERED BY VSBBIO\n\n",
                            size=SLG,  
                            key='-ML-', 
                            autoscroll=True,
                            reroute_stdout=False, 
                            write_only=True, 
                            reroute_cprint=True)
                        ]

    main_tab = sg.Tab('------', 
                    [   
                        [sg.Column([frame_lef], vertical_alignment='top'),
                        sg.Column([frame_top,frame_dow], vertical_alignment='top')]
                        ]
                    
                    )

    window = sg.Window(f"{APP_NAME} {VERSION}",
                        [[sg.TabGroup([[main_tab]])]],
                        location=(0,0),
                        size=WINDOW_SIZE,
                        keep_on_top=False,
                        resizable=False,
                        auto_size_text=True
                    ) 
    
    while True:
        event, values = window.read()
        try:
            if event == sg.WINDOW_CLOSED or event == sg.WIN_CLOSED:
                break
            elif "-RUN-MAIN-" in event:
                values.update({"version":dt.datetime.now().strftime("%Y%m%d%H%M")})
                args = (values,)
                threading.Thread(target=plot, args=args, daemon=True).start()
        except Exception as e:
            print(e)
            continue    
    window.close()

if __name__ == '__main__':
    main()