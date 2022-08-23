import time
import PySimpleGUI as sg
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.widgets import TextBox, Button

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
fig, axes = plt.subplots(figsize=(10, 10))
plt.title('y=sin(x)')
plt.xlabel('X')
plt.ylabel('Y')
buttonlocation = plt.axes([0.9, 0.1, 0.05, 0.05])
exit_button = Button(buttonlocation, 'exit')

ce =False
def click_exit(event):
    global ce
    plt.close()
    print('hello???')

    ce = False
    start1()

    return ce

exit_button.on_clicked(click_exit)

def start1():
    while not ce:
        event, values = window.read()
        print(event, values)
        if event in (sg.WIN_CLOSED, 'Exit'):  # always,  always give a way out!
            break
        elif event == 'Plot':
            start = time.time()
            while True:
                x = np.linspace(0, time.time() - start)
                y = np.sin(x)
                plt.plot(x, y)
                plt.draw()
                plt.pause(0.01)
    window.close()

start1()