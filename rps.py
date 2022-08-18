import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import random
import math
step = 0.3
num_pairs = 1
###############################################
paths = ['rock.jpg', 'paper.jpg', 'scissor.jpg']
plt.rcParams["figure.figsize"] = [5, 4.5]
plt.rcParams["figure.autolayout"] = True
plt.xticks(range(11))
plt.yticks(range(11))
fig, axes = plt.subplots()


def getImage(path):
    return OffsetImage(plt.imread(path, format="jpg"), zoom=.06)
def getdistance(x,y):
    pass

class oneset():
    x = [random.randrange(0,10), random.randrange(0,10), random.randrange(0,10)]
    y = [random.randrange(0,10), random.randrange(0,10), random.randrange(0,10)]

    def updatexy(self):
        for i in range(3):
            sign = random.randrange(0, 2)
            if sign == 0:
                self.x[i] += step
            elif sign == 1:
                self.x[i] -= step
            if self.x[i] > 9.5:
                self.x[i] = 9.5
            elif self.x[i] < 0.5:
                self.x[i] = 0.5
        for i in range(3):
            sign = random.randrange(0, 2)
            if sign == 0:
                self.y[i] += step
            elif sign == 1:
                self.y[i] -= step
            if self.y[i] > 9.5:
                self.y[i] = 9.5
            elif self.y[i] < 0.5:
                self.y[i] = 0.5


rpssets = []
for i in range(num_pairs):
    rpssets.append(oneset())

while True:

    for i in range(num_pairs):
        ab = [0, 0, 0]
        rpssets[i].updatexy()
        count = 0
        for x0, y0, path in zip(rpssets[i].x, rpssets[i].y, paths):
            print(count)
            ab[count] = AnnotationBbox(getImage(path), (x0, y0), frameon=False)
            axes.add_artist(ab[count])
            count += 1
    plt.pause(0.1)
    plt.draw()
    for v in ab:
        axes.artists.remove(v)
