import math
import numpy as np


def num_pts (width, height, points):
    l_1= 15                     #length from the base to the right                     #length from the base to the left
    w= width
    h= height
    pts= points

    n_x= (math.sqrt(((w / h) * pts) + ((w - h)**2) / (4 * (h ** 2))) - ((w - h)/(2 * h)))
    n_x= round(n_x)
    n_y= pts/n_x

    n_y=round(n_y)
    pts=n_y * n_x

    delx = w/(n_x - 1)          #the spacing between the x points
    dely = h/(n_y - 1)          #the spacing beween the y points

    #x = np.zeros(shape=n_x)     #creates an array of zeros with length values = of # of points in x direction

    #y=  np.zeros(shape=n_y)     #creates an array of zeros with length values = of # of points in y direction

    if (w > l_1):
        offset= -(w - l_1)
        x=np.arange(offset,l_1,delx)
        y=np.arange(1,height,dely)
    elif(w < l_1):
        offset = l_1 - w
        x=np.arange(offset, l_1,delx)
        y=np.arange(1,height,dely)


    return(x,y)


if __name__ == "__main__":
        print(num_pts(18,24,400))


