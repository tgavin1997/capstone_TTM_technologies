import math
import numpy as np


def num_pts (width, height, points):
    l_1= 15                     #length from the base to the right                     #length from the base to the left
    w= width
    h= height - 4
    pts= points

    n_x= (math.sqrt(((w / h) * pts) + ((w - h)**2) / (4 * (h ** 2))) - ((w - h)/(2 * h)))
    n_x= round(n_x)
    print(n_x)
    n_y= pts/n_x

    n_y=round(n_y)
    pts=n_y * n_x
    print(n_y)
    print(pts)

    #print(pts)
    delx = w/(n_x )          #the spacing between the x points
    dely = h/(n_y -1)          #the spacing beween the y points
    print(delx)
    #x = np.zeros(shape=n_x)     #creates an array of zeros with length values = of # of points in x direction

    #y=  np.zeros(shape=n_y)     #creates an array of zeros with length values = of # of points in y direction

    if (w > l_1):
        offset= -(w - l_1)
        x=np.arange(offset,l_1,delx)
        y=np.arange(3,height,dely)
    elif(w < l_1):
        offset = l_1 - w
        x=np.arange(offset, l_1,delx)
        y=np.arange(1,height,dely)

    pts = (x.size) * (y.size)
    print(pts)
    return(x,y)


if __name__ == "__main__":
        print(num_pts(10,10,20))


