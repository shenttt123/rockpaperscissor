import itertools
import math
import os
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import random
from matplotlib.widgets import TextBox, Button
import PySimpleGUI as sg

num_of_rock = 0
num_of_paper = 0
num_of_scissor = 0
step = 0.05
txt_toshow = 'w'
Zoom = 0.08
xlim = 100
ylim = 100
collisionsize = Zoom * xlim / 2
winadjust = 0.025  # zoom out(1 + winadjust)%
dirrange = math.ceil(math.sqrt(((step * 1000) ** 2) / 2))
rpsbox = []
rpslist = []


def getrandomsign():
    return 1 if random.random() < 0.5 else -1


def getanotherdirection(x):
    return math.sqrt((step * 1000) ** 2 - x ** 2)


def getcurrentsign(x):
    if x > 0:
        return 1
    elif x < 0:
        return -1


class rps:
    def __init__(self, name):
        self.name = name
        if name == 'rock':
            self.x = random.randrange(0, int(xlim * 0.05))
            self.y = random.randrange(0, int(ylim * 0.05))
            self.dir_x = random.randrange(1, dirrange) * getrandomsign()
            self.dir_y = getanotherdirection(self.dir_x) * getrandomsign()
            self.filename = 'rock.jpg'

        if name == 'paper':
            self.x = random.randrange(int(xlim * 0.95), xlim)
            self.y = random.randrange(int(ylim * 0.95), xlim)
            self.dir_x = random.randrange(1, dirrange) * getrandomsign()
            self.dir_y = getanotherdirection(self.dir_x) * getrandomsign()
            self.filename = 'paper.jpg'

        if name == 'scissor':
            self.x = random.randrange(int(xlim * 0.525), int(xlim * 0.675))
            self.y = random.randrange(int(xlim * 0.525), int(ylim * 0.675))
            self.dir_x = random.randrange(1, dirrange) * getrandomsign()
            self.dir_y = getanotherdirection(self.dir_x) * getrandomsign()
            self.filename = 'scissor.jpg'

    def update(self):
        self.x += step * self.dir_x
        self.y += step * self.dir_y
        while self.x > xlim or self.x < 0 or self.y > ylim or self.y < 0:

            if self.x >= xlim:
                self.dir_x = -1 * random.randrange(1, dirrange)
                self.dir_y = getanotherdirection(self.dir_x) * getcurrentsign(self.dir_y)
                self.x = xlim
                break
            if self.x < 0:
                self.dir_x = random.randrange(1, dirrange)
                self.dir_y = getanotherdirection(self.dir_x) * getcurrentsign(self.dir_y)
                self.x = 0
                break
            if self.y >= ylim:
                self.dir_y = -1 * random.randrange(1, dirrange)
                self.dir_x = getanotherdirection(self.dir_y) * getcurrentsign(self.dir_x)
                self.y = ylim
                break
            if self.y < 0:
                self.dir_y = random.randrange(1, dirrange)
                self.dir_x = getanotherdirection(self.dir_y) * getcurrentsign(self.dir_x)
                self.y = 0
                break


def driver(allobjlist):
    for a, b in itertools.combinations(allobjlist, 2):
        checkcollision(a, b)


def checkcollision(a: rps, b: rps):
    global num_of_scissor, num_of_rock, num_of_paper
    if a.name == 'rock' and b.name == 'scissor':
        if abs(a.x - b.x) < collisionsize and abs(a.y - b.y) < collisionsize:
            # print("rock and scissor collide")
            b.name = 'rock'
            b.filename = 'rock.jpg'
            num_of_rock += 1
            num_of_scissor -= 1
    elif b.name == 'rock' and a.name == 'scissor':
        if abs(a.x - b.x) < collisionsize and abs(a.y - b.y) < collisionsize:
            # print("rock and scissor collide")
            a.name = 'rock'
            a.filename = 'rock.jpg'
            num_of_rock += 1
            num_of_scissor -= 1
    elif a.name == 'rock' and b.name == 'paper':
        if abs(a.x - b.x) < collisionsize and abs(a.y - b.y) < collisionsize:
            # print("rock and paper collide")
            a.name = 'paper'
            a.filename = 'paper.jpg'
            num_of_paper += 1
            num_of_rock -= 1
    elif b.name == 'rock' and a.name == 'paper':
        if abs(a.x - b.x) < collisionsize and abs(a.y - b.y) < collisionsize:
            # print("rock and paper collide")
            b.name = 'paper'
            b.filename = 'paper.jpg'
            num_of_paper += 1
            num_of_rock -= 1
    elif a.name == 'paper' and b.name == 'scissor':
        if abs(a.x - b.x) < collisionsize and abs(a.y - b.y) < collisionsize:
            # print("paper and scissor collide")
            a.name = 'scissor'
            a.filename = 'scissor.jpg'
            num_of_scissor += 1
            num_of_paper -= 1
    elif b.name == 'paper' and a.name == 'scissor':
        if abs(a.x - b.x) < collisionsize and abs(a.y - b.y) < collisionsize:
            # print("paper and scissor collide")
            b.name = 'scissor'
            b.filename = 'scissor.jpg'
            num_of_scissor += 1
            num_of_paper -= 1


def submitr(text):
    global num_of_rock, rpslist
    if (int(text)) < 0:
        count = abs(int(text))
        for v in rpslist:
            if v.name == 'rock' and count > 0:
                rpslist.remove(v)
                count -= 1
                num_of_rock -= 1
    else:
        for i in range(int(text)):
            rpslist.append(rps('rock'))
            num_of_rock += 1


def submitp(text):
    global num_of_paper, rpslist
    if (int(text)) < 0:
        count = abs(int(text))
        for v in rpslist:
            if v.name == 'paper' and count > 0:
                rpslist.remove(v)
                count -= 1
                num_of_paper -= 1
                print('rock--')

    else:
        for i in range(int(text)):
            rpslist.append(rps('paper'))
            num_of_paper += 1


def submits(text):
    global num_of_scissor, rpslist
    print(text)
    if (int(text)) < 0:
        count = abs(int(text))
        print(type(count))
        for v in rpslist:
            if v.name == 'scissor' and count > 0:
                rpslist.remove(v)
                count -= 1
                num_of_scissor -= 1
    else:
        for i in range(int(text)):
            rpslist.append(rps('scissor'))
            num_of_scissor += 1


def submitspeed(text):
    global step, dirrange
    step = abs(float(text) / 1000)
    dirrange = math.ceil(math.sqrt(((step * 400) ** 2) / 2))


def updatetext(str):
    global txt_toshow
    txt_toshow = str


def click_exit(event):

    try:
        quit()
        print('hello')
        os.system("taskkill /im rps.exe")
    except:
        quit()


def start():
    # fig.set_size_inches(204  / float(fig.get_dpi()), 204 / float(fig.get_dpi()))
    fig, axes = plt.subplots(figsize=(10, 10))
    plt.subplots_adjust(bottom=0.2)
    plt.xlim([0 - xlim * winadjust, xlim * (1 + winadjust)])
    plt.ylim([0 - ylim * winadjust, ylim * (1 + winadjust)])
    axes.xaxis.set_visible(False)
    axes.yaxis.set_visible(False)
    axes.margins(1000 * (1 + winadjust))
    axes.set_ylim(bottom=-3)
    axes.set_xlim(left=-3)
    rtext_box = TextBox(plt.axes([0.1, 0.1, 0.05, 0.05]), 'rock+-')
    ptext_box = TextBox(plt.axes([0.25, 0.1, 0.05, 0.05]), 'paper+-')
    stext_box = TextBox(plt.axes([0.41, 0.1, 0.05, 0.05]), 'scissor+-')
    speedtext_box = TextBox(plt.axes([0.6, 0.1, 0.05, 0.05]), 'set speed')
    exit_button = Button(plt.axes([0.9, 0.1, 0.05, 0.05]), 'exit')

    rtext_box.on_submit(submitr)
    ptext_box.on_submit(submitp)
    stext_box.on_submit(submits)
    speedtext_box.on_submit(submitspeed)
    exit_button.on_clicked(click_exit)

    figure_canvas_agg = FigureCanvasTkAgg(fig, master=window['fig_cv'].TKCanvas)
    figure_canvas_agg.get_tk_widget().pack(side='right', fill='both', expand=1)

    while True:
        for i in range(len(rpslist)):
            rpslist[i].update()
            rpsbox.append(AnnotationBbox(OffsetImage(plt.imread(rpslist[i].filename), zoom=Zoom),
                                         (rpslist[i].x, rpslist[i].y), frameon=False))
            axes.add_artist(rpsbox[i])

        driver(rpslist)

        tx = fig.text(0.65, 0.1,
                      "number of rock is: {}\nnumber of paper is: {}\nnumber of scissor is: {}\ncurrent speed is: {}".format(
                          num_of_rock, num_of_paper, num_of_scissor, step * 1000), fontsize=10)
        plt.draw()
        fig.canvas.flush_events()

        tx.remove()
        for i in range(len(rpsbox)):
            axes.artists.remove(rpsbox[i])
        rpsbox.clear()
        if num_of_rock == 0 and num_of_paper == 0 and num_of_scissor != 0:
            break
        if num_of_rock == 0 and num_of_paper != 0 and num_of_scissor == 0:
            break
        if num_of_rock != 0 and num_of_paper == 0 and num_of_scissor == 0:
            break


def open_window():
    layout = [[sg.Text(rpslist[0].name.capitalize() + " Win!", font=20, key="new")], [sg.B('Restart', key='restart')]]
    window = sg.Window("Second Window", layout, modal=True)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        elif event == 'restart':
            plt.close()
            start()
            break

#############################
layout = [
    [sg.Text('Please enter numbers of rock paper and scissor')],
    [sg.Text('Rock', size=(12, 2)), sg.InputText(size=3)],
    [sg.Text('Paper', size=(12, 2)), sg.InputText(size=3)],
    [sg.Text('Scissor', size=(12, 2)), sg.InputText(size=3)],
    [sg.Submit('Start', key='start'), sg.Cancel()],
    [sg.Column(layout=[[sg.Canvas(key='fig_cv')]])]
]
window = sg.Window("rock paper scissor", layout)

while True:
    event, values = window.read()
    if event == 'start':
        num_of_rock = int(values[0])
        num_of_paper = int(values[1])
        num_of_scissor = int(values[2])
        for i in range(num_of_rock):
            rpslist.append(rps('rock'))
        for i in range(num_of_paper):
            rpslist.append(rps('paper'))
        for i in range(num_of_scissor):
            rpslist.append(rps('scissor'))
        start()
        open_window()

    elif event == sg.WIN_CLOSED:
        break

window.close()
