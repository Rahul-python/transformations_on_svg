# -*- coding: utf-8 -*-
# usr/bin/python3
"""
Created on Sun Dec  6 03:41:38 2020

@author: Rahul Jakkamsetty

This file creates four svg files.

This doesn't  use standard xml library to create xml file but writes the svg file using the binary files.

numpy is only used to create array of zeros of requried image size.

opencv is used to draw shapes and then find contours.

binary file operations are used to write to svg file.

"""





import cv2 as cv
import numpy as np




def write_to_svg(path,out,size,thickness=1):
    """
    opens a file in binary w+ mode and write svg/xml syntax to file.

    Parameters
    ----------
    path : string
        path to the file you want to save the svg file.
    out : ndarray
        contours found by cv.findCountours.
    size : list
        size of the image.
    thickness : int, optional
        thickness of the edge of the image. The default is 1.

    Returns
    -------
    None.

    """
    c = max(out,key=cv.contourArea)

    f = open(path, 'w+')


    f.write('<svg viewBox="-2000 -2000 6000 6000" fill="white" fill-opacity="0" width="' + str(size[0])+'" height="'+str(size[1])+'" xmlns="http://www.w3.org/2000/svg" version="1.1">')
    f.write('<path d="M')

    for i in range(len(c)):
        x, y = c[i][0] 
        f.write(str(x) + ' ' + str(y)+' ')

    f.write('" stroke ="green" stroke-width="'+str(thickness)+'"/>')
    f.write('</svg>')
    f.close()


if __name__== '__main__':

    size=[1000,1000,3] #image size
    im=np.zeros(size,dtype=np.uint8) #blank image

    thickness=1
    circle=cv.circle(im,(500,500),200,(0,255,0),thickness) # draw circle

    im = np.zeros(size, dtype=np.uint8)
    square = cv.rectangle(im, (100, 100), (500, 500), (0, 255, 0), thickness=thickness) # draw square

    im = np.zeros(size, dtype=np.uint8)
    triangle_cood = np.array([[[240, 500], [380, 230], [190, 280]]], np.int32)
    triangle=cv.polylines(im, [triangle_cood], True, (0,255,0), thickness=thickness) # draw triangle

    im = np.zeros(size, dtype=np.uint8)
    pts=np.array([[100,100],[10,50],[900,500],[340,250]],np.int32)
    
    polyline=cv.polylines(im,[pts],isClosed=False,color=(0,255,0),thickness=thickness) # draw polylines
    
    #convertin to 2D gray images.
    circle_out = cv.cvtColor(circle,cv.COLOR_RGB2GRAY)
    square_out = cv.cvtColor(square, cv.COLOR_RGB2GRAY)
    triangle_out = cv.cvtColor(triangle, cv.COLOR_RGB2GRAY)
    polyline_out = cv.cvtColor(polyline,cv.COLOR_RGB2GRAY)
    
    #edge detection not requried, because the images are similar to binary
    
    co, _ = cv.findContours(circle_out, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
    so, _ = cv.findContours(square_out, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
    to, _ = cv.findContours(triangle_out, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
    po, _ = cv.findContours(polyline_out, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)   
    po=[po[0][:int(len(po[0])/2)+1]] # for unclosed figures find contours two copies of points for single point. so halving.

    direc='../data/'
    write_to_svg(direc+'circle.svg', co, size, thickness=5)
    write_to_svg(direc+'square.svg', so, size, thickness=5)
    write_to_svg(direc+'triangle.svg', to, size, thickness=5)
    write_to_svg(direc+'polyline.svg', po, size, thickness=5)
    
    print('writing Done')


