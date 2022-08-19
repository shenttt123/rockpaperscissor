import itertools
import math
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import random

speed = 2  # min is 2
num_of_rock = 3
num_of_paper = 8
num_of_scissor = 8

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
    print(a.name, b.name)
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


fig, ax = plt.subplots(figsize=(10, 10))

ax.axes.xaxis.set_visible(False)
ax.axes.yaxis.set_visible(False)
plt.xlim([0 - xlim * winadjust, xlim * (1 + winadjust)])
plt.ylim([0 - ylim * winadjust, ylim * (1 + winadjust)])

rocklist = []
paperlist = []
scissorlist = []


for i in range(num_of_rock):
    rocklist.append(rps('rock'))
for i in range(num_of_paper):
    paperlist.append(rps('paper'))
for i in range(num_of_scissor):
    scissorlist.append(rps('scissor'))


rbox = [0] * num_of_rock
pbox = [0] * num_of_paper
sbox = [0] * num_of_scissor
while True:
    allobj = []
    for i in range(num_of_rock):
        rocklist[i].update()
        allobj.append(rocklist[i])
        rbox[i] = AnnotationBbox(OffsetImage(plt.imread(rocklist[i].filename), zoom=Zoom),
                                 (rocklist[i].x, rocklist[i].y), frameon=False)
        ax.add_artist(rbox[i])

    for i in range(num_of_paper):
        paperlist[i].update()
        allobj.append(paperlist[i])
        pbox[i] = AnnotationBbox(OffsetImage(plt.imread(paperlist[i].filename), zoom=Zoom),
                                 (paperlist[i].x, paperlist[i].y), frameon=False)
        ax.add_artist(pbox[i])

    for i in range(num_of_scissor):
        scissorlist[i].update()
        allobj.append(scissorlist[i])
        sbox[i] = AnnotationBbox(OffsetImage(plt.imread(scissorlist[i].filename), zoom=Zoom),
                                 (scissorlist[i].x, scissorlist[i].y), frameon=False)
        ax.add_artist(sbox[i])

    driver(allobj)

    plt.pause(0.01)
    plt.draw()

    for i in range(num_of_rock):
        ax.artists.remove(rbox[i])
    for i in range(num_of_paper):
        ax.artists.remove(pbox[i])
    for i in range(num_of_scissor):
        ax.artists.remove(sbox[i])
