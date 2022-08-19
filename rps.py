import itertools
import math
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import random

speed = 3  # min is 2
num_of_pairs = 3

step = 1
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
            self.dir_x = random.randrange(1, speedrange)
            self.dir_y = getanotherspeed(self.dir_x)
            self.filename = 'rock.jpg'
        if name == 'paper':
            self.x = random.randrange(int(xlim * 0.95), xlim)
            self.y = random.randrange(int(ylim * 0.95), xlim)
            self.dir_x = random.randrange(1, speedrange)
            self.dir_y = getanotherspeed(self.dir_x)
            self.filename = 'paper.jpg'
        if name == 'scissor':
            self.x = random.randrange(int(xlim * 0.525), int(xlim * 0.675))
            self.y = random.randrange(int(xlim * 0.525), int(ylim * 0.675))
            self.dir_x = random.randrange(1, speedrange)
            self.dir_y = getanotherspeed(self.dir_x)
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
    print('driver....')
    for arg in args:
        print('hi',arg)

    for a, b in itertools.combinations(args, 2):
        print('hello?')
        print(a.name,b.name)
        checkcollision(a, b)


def checkcollision(a: rps, b: rps):
    if a.name == 'rock' and b.name == 'scissor':
        if abs(a.x - b.x) < collisionsize and abs(a.y - b.y) < collisionsize:
            print("rock and scissor collide")
            b.name = 'rock'
            b.filename = 'rock.jpg'


    elif a.name == 'rock' and b.name == 'paper':
        if abs(a.x - b.x) < collisionsize and abs(a.y - b.y) < collisionsize:
            print("rock and paper collide")
            a.name = 'paper'
            a.filename = 'paper.jpg'


    elif a.name == 'paper' and b.name == 'scissor':
        if abs(a.x - b.x) < collisionsize and abs(a.y - b.y) < collisionsize:
            print("paper and scissor collide")
            a.name = 'scissor'
            a.filename = 'scissor.jpg'



fig, ax = plt.subplots(figsize=(10, 10))

ax.axes.xaxis.set_visible(False)
ax.axes.yaxis.set_visible(False)
plt.xlim([0 - xlim * winadjust, xlim * (1 + winadjust)])
plt.ylim([0 - ylim * winadjust, ylim * (1 + winadjust)])

rocklist = []
paperlist = []
scissorlist = []

for i in range(num_of_pairs):
    rocklist.append(rps('rock'))
    paperlist.append(rps('paper'))
    scissorlist.append(rps('scissor'))

rbox = [0] * num_of_pairs
sbox = [0] * num_of_pairs
pbox = [0] * num_of_pairs
while True:
    allobj = []
    for i in range(num_of_pairs):
        rocklist[i].update()
        paperlist[i].update()
        scissorlist[i].update()
        allobj.append(rocklist[i])
        allobj.append(paperlist[i])
        allobj.append(scissorlist[i])
        rbox[i] = AnnotationBbox(OffsetImage(plt.imread(rocklist[i].filename), zoom=Zoom),
                                 (rocklist[i].x, rocklist[i].y), frameon=False)
        pbox[i] = AnnotationBbox(OffsetImage(plt.imread(paperlist[i].filename), zoom=Zoom),
                                 (paperlist[i].x, paperlist[i].y), frameon=False)
        sbox[i] = AnnotationBbox(OffsetImage(plt.imread(scissorlist[i].filename), zoom=Zoom),
                                 (scissorlist[i].x, scissorlist[i].y), frameon=False)
        ax.add_artist(rbox[i])
        ax.add_artist(pbox[i])
        ax.add_artist(sbox[i])

    driver(allobj)

    plt.pause(0.01)
    plt.draw()

    for i in range(num_of_pairs):
        ax.artists.remove(rbox[i])
        ax.artists.remove(pbox[i])
        ax.artists.remove(sbox[i])