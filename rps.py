import itertools
import math
import os

import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import random
from matplotlib.widgets import TextBox, Button


num_of_rock = 1
num_of_paper = 1
num_of_scissor = 1
step = 0.05
txt_toshow = 'w'
Zoom = 0.08
xlim = 100
ylim = 100
collisionsize = Zoom * xlim / 2
winadjust = 0.025  # zoom out(1 + winadjust)%
speedrange = math.ceil(math.sqrt(((step*400) ** 2) / 2))

rbox = []
pbox = []
sbox = []
rocklist = []
paperlist = []
scissorlist = []


def getrandomsign():
    return 1 if random.random() < 0.5 else -1


def getanotherspeed(x):
    return math.sqrt((step*400) ** 2 - x ** 2)


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
            self.dir_x = random.randrange(1, speedrange) * getrandomsign()
            self.dir_y = getanotherspeed(self.dir_x) * getrandomsign()
            self.filename = 'rock.jpg'

        if name == 'paper':
            self.x = random.randrange(int(xlim * 0.95), xlim)
            self.y = random.randrange(int(ylim * 0.95), xlim)
            self.dir_x = random.randrange(1, speedrange) * getrandomsign()
            self.dir_y = getanotherspeed(self.dir_x) * getrandomsign()
            self.filename = 'paper.jpg'

        if name == 'scissor':
            self.x = random.randrange(int(xlim * 0.525), int(xlim * 0.675))
            self.y = random.randrange(int(xlim * 0.525), int(ylim * 0.675))
            self.dir_x = random.randrange(1, speedrange) * getrandomsign()
            self.dir_y = getanotherspeed(self.dir_x) * getrandomsign()
            self.filename = 'scissor.jpg'

    def update(self):
        self.x += step * self.dir_x
        self.y += step * self.dir_y
        while self.x > xlim or self.x < 0 or self.y > ylim or self.y < 0:

            if self.x >= xlim:
                self.dir_x = -1 * random.randrange(1, speedrange)
                self.dir_y = getanotherspeed(self.dir_x) * getcurrentsign(self.dir_y)
                break
            if self.x < 0:
                self.dir_x = random.randrange(1, speedrange)
                self.dir_y = getanotherspeed(self.dir_x) * getcurrentsign(self.dir_y)
                break
            if self.y >= ylim:
                self.dir_y = -1 * random.randrange(1, speedrange)
                self.dir_x = getanotherspeed(self.dir_y) * getcurrentsign(self.dir_x)
                break
            if self.y < 0:
                self.dir_y = random.randrange(1, speedrange)
                self.dir_x = getanotherspeed(self.dir_y) * getcurrentsign(self.dir_x)
                break
            self.x += step * self.dir_x
            self.y += step * self.dir_y


def driver(*args):
    idk = []
    for arg in args:
        idk.append(arg)
    for a, b in itertools.combinations(idk[0], 2):
        checkcollision(a, b)


def checkcollision(a: rps, b: rps):
    global num_of_scissor, num_of_rock, num_of_paper
    if a.name == 'rock' and b.name == 'scissor':
        if abs(a.x - b.x) < collisionsize and abs(a.y - b.y) < collisionsize:
            #print("rock and scissor collide")
            b.name = 'rock'
            b.filename = 'rock.jpg'
            num_of_rock += 1
            num_of_scissor -= 1
    elif b.name == 'rock' and a.name == 'scissor':
        if abs(a.x - b.x) < collisionsize and abs(a.y - b.y) < collisionsize:
            #print("rock and scissor collide")
            a.name = 'rock'
            a.filename = 'rock.jpg'
            num_of_rock += 1
            num_of_scissor -= 1
    elif a.name == 'rock' and b.name == 'paper':
        if abs(a.x - b.x) < collisionsize and abs(a.y - b.y) < collisionsize:
            #print("rock and paper collide")
            a.name = 'paper'
            a.filename = 'paper.jpg'
            num_of_paper += 1
            num_of_rock -= 1
    elif b.name == 'rock' and a.name == 'paper':
        if abs(a.x - b.x) < collisionsize and abs(a.y - b.y) < collisionsize:
            #print("rock and paper collide")
            b.name = 'paper'
            b.filename = 'paper.jpg'
            num_of_paper += 1
            num_of_rock -= 1
    elif a.name == 'paper' and b.name == 'scissor':
        if abs(a.x - b.x) < collisionsize and abs(a.y - b.y) < collisionsize:
            #print("paper and scissor collide")
            a.name = 'scissor'
            a.filename = 'scissor.jpg'
            num_of_scissor += 1
            num_of_paper -= 1
    elif b.name == 'paper' and a.name == 'scissor':
        if abs(a.x - b.x) < collisionsize and abs(a.y - b.y) < collisionsize:
            #print("paper and scissor collide")
            b.name = 'scissor'
            b.filename = 'scissor.jpg'
            num_of_scissor += 1
            num_of_paper -= 1
def submitr(text):
    global num_of_rock, rocklist, rbox, scissorlist, paperlist
    if (int(text)) < 0:
        count = abs(int(text))

        for v in rocklist:
            if v.name == 'rock' and count > 0:
                rocklist.remove(v)
                count -= 1
                num_of_rock -= 1


        for v in paperlist:
            if v.name == 'rock' and count > 0:
                paperlist.remove(v)
                count -= 1
                num_of_rock -= 1

        for v in scissorlist:
            if v.name == 'rock' and count > 0:
                scissorlist.remove(v)
                count -= 1
                num_of_rock -= 1
    else:
        for i in range(int(text)):
            rocklist.append(rps('rock'))
            num_of_rock += 1
def submitp(text):
    global num_of_paper, paperlist, pbox, scissorlist, rocklist
    if (int(text)) < 0:
        count = abs(int(text))
        for v in rocklist:
            if v.name == 'paper' and count > 0:
                rocklist.remove(v)
                count -= 1
                num_of_paper -= 1
                print('rock--')

        for v in paperlist:
            if v.name == 'paper' and count > 0:
                paperlist.remove(v)
                count -= 1
                num_of_paper -= 1
                print('paper--')

        for v in scissorlist:
            if v.name == 'paper' and count > 0:
                scissorlist.remove(v)
                count -= 1
                num_of_paper -= 1
                print('scissor--')
    else:
        for i in range(int(text)):
            paperlist.append(rps('paper'))
            num_of_paper += 1
def submits(text):
    global num_of_scissor, scissorlist, sbox, rocklist, paperlist
    print(text)
    if (int(text)) < 0:
        count = abs(int(text))
        print(type(count))
        for v in rocklist:
            if v.name == 'scissor' and count > 0:
                rocklist.remove(v)
                count -= 1
                num_of_scissor -= 1

        for v in paperlist:
            if v.name == 'scissor' and count > 0:
                paperlist.remove(v)
                count -= 1
                num_of_scissor -= 1

        for v in scissorlist:
            if v.name == 'scissor' and count > 0:
                scissorlist.remove(v)
                count -= 1
                num_of_scissor -= 1
    else:
        for i in range(int(text)):
            scissorlist.append(rps('scissor'))
            num_of_scissor += 1
def submitspeed(text):
    global step, speedrange
    step = float(text)/1000
    speedrange = math.ceil(math.sqrt(((step * 400) ** 2) / 2))
def updatetext(str):
    global txt_toshow
    txt_toshow=str
def click_exit(event):
    try:
        os.system("taskkill /im rps.exe")
    except:
        exit()


fig, axes = plt.subplots(figsize=(10, 10))
plt.subplots_adjust(bottom=0.2)

rtext_box = TextBox(plt.axes([0.1, 0.1, 0.05, 0.05]), 'rock+-')
rtext_box.on_submit(submitr)
ptext_box = TextBox(plt.axes([0.25, 0.1, 0.05, 0.05]), 'paper+-')
ptext_box.on_submit(submitp)
stext_box = TextBox(plt.axes([0.4, 0.1, 0.05, 0.05]), 'scissor+-')
stext_box.on_submit(submits)
speedtext_box = TextBox(plt.axes([0.55, 0.1, 0.05, 0.05]), 'set speed')
speedtext_box.on_submit(submitspeed)
exit_button = Button(plt.axes([0.9, 0.1, 0.05, 0.05]),'exit')
exit_button.on_clicked(click_exit)
axes.xaxis.set_visible(False)
axes.yaxis.set_visible(False)
axes.margins(1000 * (1 + winadjust))
plt.xlim([0 - xlim * winadjust, xlim * (1 + winadjust)])
plt.ylim([0 - ylim * winadjust, ylim * (1 + winadjust)])
axes.set_ylim(bottom=-3)
axes.set_xlim(left=-3)

for i in range(num_of_rock):
    rocklist.append(rps('rock'))
for i in range(num_of_paper):
    paperlist.append(rps('paper'))
for i in range(num_of_scissor):
    scissorlist.append(rps('scissor'))

while True:
    allobj = []
    for i in range(len(rocklist)):
        rocklist[i].update()
        allobj.append(rocklist[i])
        rbox.append(AnnotationBbox(OffsetImage(plt.imread(rocklist[i].filename), zoom=Zoom),
                                   (rocklist[i].x, rocklist[i].y), frameon=False))
        axes.add_artist(rbox[i])

    for i in range(len(paperlist)):
        paperlist[i].update()
        allobj.append(paperlist[i])
        pbox.append(AnnotationBbox(OffsetImage(plt.imread(paperlist[i].filename), zoom=Zoom),
                                   (paperlist[i].x, paperlist[i].y), frameon=False))
        axes.add_artist(pbox[i])

    for i in range(len(scissorlist)):
        scissorlist[i].update()
        allobj.append(scissorlist[i])
        sbox.append(AnnotationBbox(OffsetImage(plt.imread(scissorlist[i].filename), zoom=Zoom),
                                   (scissorlist[i].x, scissorlist[i].y), frameon=False))
        axes.add_artist(sbox[i])

    driver(allobj)
    tx = fig.text(0.65, 0.1,
                  "number of rock is: {}\nnumber of paper is: {}\nnumber of scissor is: {}\ncurrent speed is: {}".format(
                      num_of_rock, num_of_paper, num_of_scissor, step * 1000), fontsize=10)
    plt.pause(0.01)
    plt.draw()
    tx.remove()
    for i in range(len(rbox)):
        axes.artists.remove(rbox[i])

    for i in range(len(pbox)):
        axes.artists.remove(pbox[i])

    for i in range(len(sbox)):
        axes.artists.remove(sbox[i])

    rbox.clear()
    pbox.clear()
    sbox.clear()



