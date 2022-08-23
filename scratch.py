import time
import PySimpleGUI as sg
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


layout = [
    [sg.T('Graph: y=sin(x)')],
    [sg.B('Plot'), sg.B('Exit')],
    [sg.T('Controls:')],
    [sg.T('Figure:')],
    [sg.Column(
        layout=[
            [sg.Canvas(key='fig_cv',

                       size=(400 * 2, 400)
                       )]
        ],
        background_color='#DAE0E6',
        pad=(0, 0)
    )],
    [sg.B('Alive?')]
]

window = sg.Window('Graph with controls', layout)

while True:
    event, values = window.read()
    print(event, values)
    if event in (sg.WIN_CLOSED, 'Exit'):  # always,  always give a way out!
        break
    elif event == 'Plot':

        fig, axes = plt.subplots(figsize=(10, 10))
        #plt.ion()
        plt.title('y=sin(x)')
        plt.xlabel('X')
        plt.ylabel('Y')
        figure_canvas_agg = FigureCanvasTkAgg(fig, master=window['fig_cv'].TKCanvas)
        figure_canvas_agg.get_tk_widget().pack(side='right', fill='both', expand=1)
        start = time.time()
        while True:
            x = np.linspace(0, time.time() - start)
            y = np.sin(x)
            plt.plot(x, y)

            fig.canvas.draw()
            fig.canvas.flush_events()

window.close()
