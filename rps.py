import itertools
import math
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import random

from matplotlib.widgets import TextBox

speed = 20  # min is 2
num_of_rock = 30
num_of_paper = 1
num_of_scissor = 2

step = 0.05
Zoom = 0.08
xlim = 100
ylim = 100
collisionsize = xlim / 20
winadjust = 0.025  # zoom out(1 + winadjust)%
speedrange = math.ceil(math.sqrt((speed ** 2) / 2))


def getrandomsign():
    return 1 if random.random() < 0.5 else -1


def getanotherspeed(x):
    return math.sqrt(speed ** 2 - x ** 2)


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
    if a.name == 'rock' and b.name == 'scissor':
        if abs(a.x - b.x) < collisionsize and abs(a.y - b.y) < collisionsize:
            print("rock and scissor collide")
            b.name = 'rock'
            b.filename = 'rock.jpg'
    elif b.name == 'rock' and a.name == 'scissor':
        if abs(a.x - b.x) < collisionsize and abs(a.y - b.y) < collisionsize:
            print("rock and scissor collide")
            a.name = 'rock'
            a.filename = 'rock.jpg'
    elif a.name == 'rock' and b.name == 'paper':
        if abs(a.x - b.x) < collisionsize and abs(a.y - b.y) < collisionsize:
            print("rock and paper collide")
            a.name = 'paper'
            a.filename = 'paper.jpg'
    elif b.name == 'rock' and a.name == 'paper':
        if abs(a.x - b.x) < collisionsize and abs(a.y - b.y) < collisionsize:
            print("rock and paper collide")
            b.name = 'paper'
            b.filename = 'paper.jpg'
    elif a.name == 'paper' and b.name == 'scissor':
        if abs(a.x - b.x) < collisionsize and abs(a.y - b.y) < collisionsize:
            print("paper and scissor collide")
            a.name = 'scissor'
            a.filename = 'scissor.jpg'
    elif b.name == 'paper' and a.name == 'scissor':
        if abs(a.x - b.x) < collisionsize and abs(a.y - b.y) < collisionsize:
            print("paper and scissor collide")
            b.name = 'scissor'
            b.filename = 'scissor.jpg'


def submitr(text):
    global num_of_rock, rocklist, rbox
    for i in range(text):
        rocklist.append(rps('rock'))
        num_of_rock += 1
        rbox.append(AnnotationBbox(OffsetImage(plt.imread(rocklist[i].filename), zoom=Zoom),
                                   (rocklist[i].x, rocklist[i].y), frameon=False))


def submitp(text):
    global num_of_paper, paperlist, pbox
    for i in range(text):
        paperlist.append(rps('paper'))
        num_of_paper += 1
        pbox.append(AnnotationBbox(OffsetImage(plt.imread(paperlist[i].filename), zoom=Zoom),
                                   (paperlist[i].x, paperlist[i].y), frameon=False))


def submits(text):
    global num_of_scissor, scissorlist, sbox
    for i in range(text):
        scissorlist.append(rps('scissor'))
        num_of_scissor += 1
        sbox.append(AnnotationBbox(OffsetImage(plt.imread(scissorlist[i].filename), zoom=Zoom),
                                   (scissorlist[i].x, scissorlist[i].y), frameon=False))


fig, axes = plt.subplots(figsize=(10, 10))
plt.subplots_adjust(bottom=0.2)

rtext_box = TextBox(plt.axes([0.1, 0.1, 0.05, 0.05]), 'scissor')
rtext_box.on_submit(submitr)
ptext_box = TextBox(plt.axes([0.45, 0.1, 0.05, 0.05]), 'scissor')
ptext_box.on_submit(submitp)
stext_box = TextBox(plt.axes([0.8, 0.1, 0.05, 0.05]), 'scissor')
stext_box.on_submit(submits)

axes.xaxis.set_visible(False)
axes.yaxis.set_visible(False)
axes.margins(1000 * (1 + winadjust))
plt.xlim([0 - xlim * winadjust, xlim * (1 + winadjust)])
plt.ylim([0 - ylim * winadjust, ylim * (1 + winadjust)])
axes.set_ylim(bottom=-3)
axes.set_xlim(left=-3)

rocklist = []
paperlist = []
scissorlist = []

for i in range(num_of_rock):
    rocklist.append(rps('rock'))
for i in range(num_of_paper):
    paperlist.append(rps('paper'))
for i in range(num_of_scissor):
    scissorlist.append(rps('scissor'))

rbox = []
pbox = []
sbox = []
while True:
    allobj = []
    for i in range(num_of_rock):
        rocklist[i].update()
        allobj.append(rocklist[i])
        rbox.append(AnnotationBbox(OffsetImage(plt.imread(rocklist[i].filename), zoom=Zoom),
                                   (rocklist[i].x, rocklist[i].y), frameon=False))
        axes.add_artist(rbox[i])

    for i in range(num_of_paper):
        paperlist[i].update()
        allobj.append(paperlist[i])
        pbox.append(AnnotationBbox(OffsetImage(plt.imread(paperlist[i].filename), zoom=Zoom),
                                   (paperlist[i].x, paperlist[i].y), frameon=False))
        axes.add_artist(pbox[i])

    for i in range(num_of_scissor):
        scissorlist[i].update()
        allobj.append(scissorlist[i])
        sbox.append(AnnotationBbox(OffsetImage(plt.imread(scissorlist[i].filename), zoom=Zoom),
                                   (scissorlist[i].x, scissorlist[i].y), frameon=False))
        axes.add_artist(sbox[i])

    driver(allobj)

    plt.pause(0.01)
    plt.draw()


    try:
        for value in rbox:
            axes.artists.remove(value)
        for value in pbox:
            axes.artists.remove(value)
        for value in sbox:
            axes.artists.remove(value)
    except:
        pass

    rbox.clear()
    pbox.clear()
    sbox.clear()
