# -*- coding: utf-8 -*-
"""
Created on Thu Dec 10 01:21:00 2020

@author: Rahul Jakkamsetty
"""


import math
import xml.etree.ElementTree as ET
import cv2 as cv
import numpy as np

import copy

class Point:
    
    def __init__(self,x,y,r=False,shape='None'):
        """
        Point class.

        Parameters
        ----------
        x : int
            x-coordinate.
        y : int
            y-coordinate.
        r : int, optional
            if circle, it's radius. The default is False.
        shape : string, optional
            shape of object to which this point belongs. The default is 'None'.

        Returns
        -------
        None.

        """
        self.x=x
        self.y=y
        self.r=r
        self.shape=shape
        
        
        
    def rotate(self,rotation):
        
        angle_rad = rotation[0]*math.pi/180
        
        self.x=(math.cos(angle_rad)*(self.x-rotation[1])-math.sin(angle_rad)*(self.y-rotation[2]))+rotation[1]
        self.y=(math.sin(angle_rad)*(self.x-rotation[1])+math.cos(angle_rad)*(self.y-rotation[2]))+rotation[2]
        
    def scale(self,scale):
        self.x=(self.x-scale[1])*scale[0]+scale[1]
        self.y=(self.y-scale[2])*scale[0]+scale[2]
        if self.r:
            self.r=self.r*scale[0]
        
    def translate(self,t_x,t_y):
        self.x=self.x+t_x
        self.y=self.y+t_y
        
    def distance(self,px,py): #no where used. since you have asked I have written this as well.
        dx= self.x-px
        dy= self.y-py
        
        return math.hypot((dx,dy))
    def get_points(self):
        if self.r:
            return (int(self.x),int(self.y),int(self.r))
        else:
            return [int(self.x),int(self.y)]
    
class Object:
    
    def __init__(self,path,keep_original=False):
        """
        Class of the object/Image.

        Parameters
        ----------
        path : string. 
            path to the svg file. circle_with_tag.svg, square_with_tag.svg, triangle_with_tag.svg, polyline_with_tag.svg
        keep_original : bool, optional
            if True, it keeps the original shape in the image. The default is False.

        Returns
        -------
        None.

        """
        tree=ET.parse(path)
        root=tree.getroot()
        tag=root[0].tag
        self.width=int(root.attrib['width'])
        self.height=int(root.attrib['height'])
        self.ko=keep_original
        
        if 'circle' in tag:
            x=int(root[0].attrib['cx'])
            y=int(root[0].attrib['cy'])
            r=int(root[0].attrib['r'])
            self.co_ordinates=Point(x,y,r,'circle')
        elif 'rect' in tag:
            x=int(root[0].attrib['x'])
            y=int(root[0].attrib['y'])
            x_diag=x+int(root[0].attrib['width'])
            y_diag=y+int(root[0].attrib['height'])
            self.co_ordinates=[Point(x,y,shape='square'),Point(x_diag,y_diag,shape='square')]
            
        elif 'polygon' in tag:
            string=root[0].attrib['points']
            pts=string.split()
            self.co_ordinates=[Point(float(pts[i]),float(pts[i+1]),shape='triangle') for i in range(0,len(pts),2)] #list comprehension
                
        elif 'polyline' in tag:
            string=root[0].attrib['points']
            pts=string.split()
            self.co_ordinates=[Point(float(pts[i]),float(pts[i+1]),shape='polyline') for i in range(0,len(pts),2)]
        else:
            print('Unknown_shape')
        
        if self.ko:
            self.copy_coordinates=copy.deepcopy(self.co_ordinates)
            
    def write_png(self,points,copy=False):
        """
        saves the transformation/original image to png

        Parameters
        ----------
        points : list of object/object
            objects of Point class
        copy : bool, optional
            if True, doesn't keep original. The default is False.

        Returns
        -------
        None.

        """
        if copy:
            self.img=np.zeros((self.width,self.height,3),dtype=np.uint8)
        if type(points)==list:
            if points[0].shape=='square':
                outputs=[i.get_points() for i in points]
                cv.rectangle(self.img,tuple(outputs[0]),tuple(outputs[1]),(0,255,0),3)
            elif points[0].shape=='triangle':
                outputs=[i.get_points() for i in points]
                cv.polylines(self.img,[np.array(outputs)],True,(0,255,0),3)
            else:
                outputs=[i.get_points() for i in points]
                cv.polylines(self.img,[np.array(outputs)],False,(0,255,0),3)
        else:
            co_od=points.get_points()        
            cv.circle(self.img,(co_od[:2]),co_od[2],(0,255,0),2)
           
    
                
    def transform(self,rotation=(0,0,0),scale=(1,0,0),t_x=0,t_y=0):
        """
        Transformation on the object. Just call the methods of point objects.
        Transfromation order: translation ==> scaling ==> rotation

        Parameters
        ----------
        rotation : tuple, optional
            tuple[0] is rotation angle. tuple[1] is x-coordiante of the point about which rotation is done.
            tuple[2] is y-coordiante of the point about which rotation is done. The default is (0,0,0).
        scale : tuple, optional
            Amount by which the object is scaled.  tuple[0] is scaling factor. tuple[1] is x-coordiante of the point about which scaling is done.
            tuple[2] is y-coordiante of the point about which scaling is done. The default is (1,0,0).
        t_x : int, optional
            translation of object in x-direction. The default is 0.
        t_y : int, optional
            translation of object in y-direction. The default is 0.

        Returns
        -------
        None.

        """
        
        if type(self.co_ordinates)==list:
            [i.translate(t_x,t_y) for i in self.co_ordinates]
            [i.scale(scale) for i in self.co_ordinates]
            [i.rotate(rotation) for i in self.co_ordinates]
            
      
            
        else:
            self.co_ordinates.translate(t_x, t_y)
            self.co_ordinates.scale(scale)
            self.co_ordinates.rotate(rotation)
            
            
        if self.ko:
            self.write_png(self.copy_coordinates,self.ko)
            self.write_png(self.co_ordinates)
           
            try:
                cv.imwrite('../data/'+self.co_ordinates[0].shape+'.png',self.img)
            except TypeError:
                cv.imwrite('../data/'+self.co_ordinates.shape+'.png',self.img)
        else:
            self.write_png(self.co_ordinates,True)
            try:
                cv.imwrite('../data/'+self.co_ordinates[0].shape+'.png',self.img)
            except TypeError:
                cv.imwrite('../data/'+self.co_ordinates.shape+'.png',self.img)
            
if __name__=='__main__':
    
    figure=Object('../data/circle_with_tag.svg',True)
    figure.transform((0,0,0),(2,500,500))
    print('Image saved.')
    
                
    
                
                
                                            
            
            
        