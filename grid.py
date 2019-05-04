import math
import numpy as np


def num_pts (width, height, points,size=4):
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

    n_y= pts/n_x

    n_y=round(n_y)

    pts=n_y * n_x

    delx = w/(n_x - 1)
    dely = h/(n_y - 1)
    return(delx,dely,pts)

def matrix(width,height,delx,dely,pts):
    length =round(width/delx + 1)
    x = np.ndarray(shape=length)

    y=  np.ndarray(shape=(height/dely + 1))
    return(x,y)


if __name__ == "__main__":
    print(num_pts(30,20,400))
    print(matrix(30,20,.25,.25,100))
