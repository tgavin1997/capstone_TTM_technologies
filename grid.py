import math
import numpy as np


def num_pts (width, height, points,size):
    if size ==0:
        width = 24
        height=18
    elif size == 1:
        width =24
        height=21
    elif size ==2:
        width =28
        height=24

    w=width
    h=height
    pts=points

    n_x= (math.sqrt(((w / h) * pts) + ((w - h)**2) / (4 * (h ** 2))) - ((w - h)/(2 * h)))
    n_x= round(n_x)
    print(n_x)
    n_y= pts/n_x

    n_y=round(n_y)
    print(n_y)
    pts=n_y * n_x

    delx = w/(n_x - 1)
    dely = h/(n_y - 1)
    return(n_x,n_y,delx,dely,pts)

def length(n_x,n_y,delx,dely):
    x = np.zeros(shape=n_x)

    y=  np.zeros(shape=n_y)
    return(x,y)


if __name__ == "__main__":
    bar=num_pts(18,24,400,4)

    print(bar[0])
    print(bar[1])
    print(length(bar[0],bar[1],bar[2],bar[3]))
