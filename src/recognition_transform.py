# -*- coding: utf-8 -*-
"""
Created on Sun Dec  6 03:45:46 2020

@author: Rahul Jakkamsetty
"""
import os
import xml.etree.ElementTree as ET
ET.register_namespace("","http://www.w3.org/2000/svg")





def distance(x1,x2,y1,y2):
    """
    Calcualtes distance between two points.

    Parameters
    ----------
    x1 : int or float
        x_co-oridnate of first point.
    x2 : int or float
        x_co-ordinate of second point.
    y1 : int or float
        y_co-oridnate of first point.
    y2 : TYPE
        y_co-oridnate of second point.

    Returns
    -------
    float
        distance between two points.

    """
    return pow(pow(x1-x2,2)+pow(y1-y2,2),.5)
    

class Image_Recog_Transform:
    def __init__(self,path,tolerance=1,keep_original=False,fig_no=0):
        """
        Recognises the shape in the given svg file and accordingly apply transforms

        Parameters
        ----------
        path : string
            if the working directory is src, give the path as circle.svg, square.svg. triangle.svg or polyline.svg
            else give the whole path.
            path to svg file.
        tolerance : int or float, optional
            tolerance for pixel values. This is because the pixel values are not exact. The default is 1.
        keep_original : bool, optional
            This flag sets whether to keep the original object after applying transformations. The default is False.
        fig_no : int, optional
            The number of the object that you want to work on/transfrom. The default is 0.

        Returns
        -------
        None.

        """

        self.fig_no=fig_no
        self.tolerance=tolerance
        self.keep=keep_original
        
        self.path=path
        self.tree=ET.parse(self.path)
        self.root=self.tree.getroot()
        self.circle=False
        self.triangle=False
        self.square=False
     
        try:
            self.values=self.root[0].attrib['d']
            self.sp_val=list(map(lambda x: float(x),self.values[1:].split()))
            self.fin_val=list(zip(self.sp_val,self.sp_val[1:]+self.sp_val[:1]))
            self.pix_x=[];self.pix_y=[]
            for i in range(int(len(self.fin_val)/2)):
                    self.pix_x.append(self.fin_val[2*i][0])
                    self.pix_y.append(self.fin_val[2*i][1])
            self.max_x=max(self.pix_x)
            self.min_x=min(self.pix_x)
            self.max_y=max(self.pix_y)
            self.min_y=min(self.pix_y)
            if self.check_circle():
                self.draw_circle()
                print('circle')
               
            elif self.check_square():
                self.draw_square()
                print('square')
               
            elif self.check_triangle():
                self.draw_triangle()
                print('triangle')
                
            else:
                if self.check_polyline():
                    self.draw_polyline()
                    print('Polyline')
                else:
                    print('UnknownShape')
                    
        except KeyError:
            
            tag=self.root[self.fig_no].tag
            
            if 'circle' in tag:
                self.cir_center_x=float(self.root[self.fig_no].attrib['cx'])
                self.cir_center_y=float(self.root[self.fig_no].attrib['cy'])
                self.radius=float(self.root[self.fig_no].attrib['r'])
                self.circle=True
                print('circle')
            elif 'rect' in tag:
                self.min_x=float(self.root[self.fig_no].attrib['x'])
                self.min_y=float(self.root[self.fig_no].attrib['y'])
                self.side1=float(self.root[self.fig_no].attrib['width'])
                self.side2=float(self.root[self.fig_no].attrib['height'])
                self.square=True
                print('square')
            elif 'polygon' in tag:
                self.string=self.root[self.fig_no].attrib['points']
                pts_un=list(map(lambda x:float(x),self.string.split()))
                pts=list(zip(pts_un,pts_un[1:],pts_un[:1]))
                points_x=[];points_y=[]
                for i in range(int(len(self.fin_val)/2)):
                    points_x.append(pts[2*i][0])
                    points_y.append(pts[2*i][1])
                    
                
                self.centroid_x=int(sum(points_x)/3)
                self.centroid_y=int(sum(points_y)/3)
                self.triangle=True
                print('triangle')
        
        
        
    def check_is_closed(self):
        """
        This function checks whether the object is closed or not.
        
        Returns
        -------
        bool
            True means closed other wise unclosed object.

        """
        if abs(self.pix_x[0]-self.pix_x[-1])<=self.tolerance and abs(self.pix_y[0]-self.pix_y[-1])<=self.tolerance:
            return True
        else:
            return False
    def check_polyline(self):
        """
        Function to check whether read svg object is polygon.

        Returns
        -------
        bool
            True means polyline.

        """
        if self.check_is_closed():
            return False
        else:
            return True
            
    def check_circle(self):
        """
        Function to check read svg object is circle

        Returns
        -------
        bool
            True means circle.

        """
        self.radius=(self.max_x-self.min_x)/2
        self.cir_center_x=(self.max_x+self.min_x)/2
        self.cir_center_y=(self.max_y+self.min_y)/2
        if abs(distance(self.pix_x[10],self.cir_center_x,self.pix_y[10],self.cir_center_y)-self.radius) <=self.tolerance and self.check_is_closed():
            self.circle=True
            return True
        else:
            return False
    def check_square(self):
        """
        Function to check read svg object is square

        Returns
        -------
        bool
            True means square.

        """
        self.side1=self.max_x-self.min_x
        self.side2=self.max_y-self.min_y
        self.diag=distance(self.max_x,self.min_x,self.max_y,self.min_y)
        self.sq_cx=(self.max_x+self.min_x)/2
        self.sq_cy=(self.max_y+self.min_y)/2
        if abs(distance(self.pix_x[10],self.cir_center_x,self.pix_y[10],self.cir_center_y)-self.diag/2)>1 and self.side1==self.side2 and self.check_is_closed():
            self.square=True
            return True
        else:
            return False
    def validate_triangle(self):
        """
        Function to validate the object is triangle by checking the triangle rule (sides of triangle).

        Returns
        -------
        bool
            True means a valid triangle.

        """
        side1=distance(self.li[0][0],self.li[1][0],self.li[0][1],self.li[1][1])
        side2=distance(self.li[0][0],self.li[2][0],self.li[0][1],self.li[2][1])
        side3=distance(self.li[1][0],self.li[2][0],self.li[1][1],self.li[2][1])
        if side1+side2<=side3 or side1+side3<=side2 or side2+side3<=side1:
            return False
        else:
            return True
    def check_triangle(self):
        """
        Function to check whether read object is triangle

        Returns
        -------
        TYPE
            True means triangle.

        """
        y2=self.pix_y[self.pix_x.index(self.max_x)];a2=(self.max_x,y2)
        y1=self.pix_y[self.pix_x.index(self.min_x)];a1=(self.min_x,y1)
        x2=self.pix_x[self.pix_y.index(self.max_y)];a4=(x2,self.max_y)
        x1=self.pix_x[self.pix_y.index(self.min_y)];a3=(x1,self.min_y)
        comp=[];  self.li=[a1,a2,a3,a4]
        
        for i in range(len(self.li)):
            for j in self.li[i+1:]:
                comp.append(abs(self.li[i][0]-j[0])<=self.tolerance and abs(self.li[i][1]-j[1])<=self.tolerance)
                
       
        if True in comp :
            if comp.count(True)==1:
                if comp.index(True)<3:
                    self.li.pop(0)
                elif comp.index(True)==3 or comp.index(True)==4:
                    self.li.pop(1)
                else:
                    self.li.pop(2)
                self.triangle=self.validate_triangle() and self.check_is_closed()
                return self.triangle

            else:
                return False
        else:
            return False
        
    
    def draw_circle(self):
        """
        Function to write circle object to svg file.

        Returns
        -------
        None.

        """
        if not self.keep:
            self.root.remove(self.root[0])
        newe=ET.SubElement(self.root,'circle')
        newe.attrib['cx']=str(self.cir_center_x)
        newe.attrib['cy']=str(self.cir_center_y)
        newe.attrib['r']=str(self.radius)
        newe.attrib['stroke']='green'
        newe.attrib['stroke-width']=str(5)
        newe.attrib['fill']='none'
        self.tree.write(self.path)
                
    def draw_square(self):
        """
        Function to write square object to svg file.

        Returns
        -------
        None.

        """
        if not self.keep:
            self.root.remove(self.root[0])
        newe=ET.SubElement(self.root,'rect')
        newe.attrib['x']=str(self.min_x)
        newe.attrib['y']=str(self.min_y)
        newe.attrib['width']=str(self.side1)
        newe.attrib['height']=str(self.side2)
        newe.attrib['stroke']='green'
        newe.attrib['stroke-width']=str(5)
        newe.attrib['fill']='none'
        self.tree.write(self.path)
        
    def draw_triangle(self):
        """
        Function to write triangle object ot svg file.

        Returns
        -------
        None.

        """
        if not self.keep:
            self.root.remove(self.root[0])
        newe=ET.SubElement(self.root,'polygon')
        self.string=''
        cen=list(zip(*self.li))
        self.centroid_x=int(sum(cen[0])/3)
        self.centroid_y=int(sum(cen[1])/3)
        for i in self.li:
            self.string=self.string+str(i[0])+' '+str(i[1])
        
        newe.attrib['points']=self.string
        newe.attrib['stroke']='green'
        newe.attrib['stroke-width']=str(5)
        newe.attrib['fill']='none'
        self.tree.write(self.path)
    def draw_polyline(self):
        """
        Function to write polyline object ot svg file.

        Returns
        -------
        None.

        """
        if self.keep:
            newe=ET.SubElement(self.root,'path')
            newe.attrib['d']=self.values
            newe.attrib['stroke']='green'
            newe.attrib['stroke-width']=str(5)
            newe.attrib['fill']='none'
            self.tree.write(self.path)
            
            
    
        
        
    def transform(self,rotation=(0,0,0),scale=1,t_x=0,t_y=0):
        """
        Function to apply transformations like rotation, scale and translation.
        writes the object after transfromation to given svg file.

        Parameters
        ----------
        rotation : tuple, optional
            tuple[0] is rotation angle. tuple[1] is x-coordiante of the point about which rotation is done.
            tuple[2] is x-coordiante of the point about which rotation is done.
            The default is (0,0,0).
        scale : int or float, optional
            amount by which the object is scaled. The default is 1.
            The scaling is done about the center of the object. 
            If circle and square, with respect to their centers. 
            If triangle with respect to centriod and if polyline with respect to apporiximate mid point of the whole polyline.
            
        t_x : int, optional
            translation of object in x-direction. The default is 0.
        t_y : int, optional
            translation of object in y-direction. The default is 0.

        Returns
        -------
        None.

        """
        tree=ET.parse(self.path)
        root=tree.getroot()
        if scale==0: 
            scale=1
            print('scale is never zero. setting to 1')
            
       
        if self.keep:
            ntag=self.fig_no+1
        else:
            ntag=self.fig_no
        
        if self.circle:
            trans_scale_x=str(int((self.cir_center_x/scale)-self.cir_center_x))
            trans_scale_y=str(int((self.cir_center_y/scale)-self.cir_center_y))
            root[ntag].attrib['transform']="rotate("+str(rotation[0])+" "+str(rotation[1])+" "+str(rotation[2])+") scale("+str(scale)+") translate("+trans_scale_x+" "+trans_scale_y+") translate("+str(t_x)+" "+str(t_y)+")"
        elif self.square:
            trans_scale_x=str(int((self.sq_cx/scale)-self.sq_cx))
            trans_scale_y=str(int((self.sq_cy/scale)-self.sq_cy))
            root[ntag].attrib['transform']="rotate("+str(rotation[0])+" "+str(rotation[1])+" "+str(rotation[2])+") scale("+str(scale)+") translate("+trans_scale_x+" "+trans_scale_y+") translate("+str(t_x)+" "+str(t_y)+")"
        elif self.triangle:
            trans_scale_x=str(int((self.centroid_x/scale)-self.centroid_x))
            trans_scale_y=str(int((self.centroid_y/scale)-self.centroid_y))
            
            
            root[ntag].attrib['transform']="rotate("+str(rotation[0])+" "+str(rotation[1])+" "+str(rotation[2])+") scale("+str(scale)+") translate("+trans_scale_x+" "+trans_scale_y+") translate("+str(t_x)+" "+str(t_y)+")"
        else:
            md_x=(self.max_x+self.min_x)/2
            md_y=(self.max_y+self.min_y)/2
            trans_scale_x=str(int((md_x/scale)-md_x))
            trans_scale_y=str(int((md_y/scale)-md_y))
    
            root[ntag].attrib['transform']="rotate("+str(rotation[0])+" "+str(rotation[1])+" "+str(rotation[2])+") scale("+str(scale)+") translate("+trans_scale_x+" "+trans_scale_y+") translate("+str(t_x)+" "+str(t_y)+")"
        tree.write(self.path)
        return None
            
if __name__=='__main__' :
    if 'src' in os.getcwd():
        direc='../data/'
    else:
        direc=''
    figure=Image_Recog_Transform(direc+'polyline.svg',keep_original=True) #change the filename here.
    figure.transform((10,0,0))
    
    
    
            