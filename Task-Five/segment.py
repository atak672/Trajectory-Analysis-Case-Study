import math

class Segment:
    
    '''
    
    HELLO!!
    So the way I designed this algo is that you initialize a line segment using xy points. And minDistanceFromPoint is used by the Segment class
    to calculate the minimum distance from itself to a point q.
    
    So if a line starts at point a, x1 is the
    x coordinate of a and y1 is the y coordinate of a.
    
    And if the line ends at b, x2 is the x coordinate of b
    and y2 is the y coordinate of b.
    
    Now that we have a class which signifies a segment, minDistanceFromSeg calcualtes the minimum distance between the line segment
    and a point q (with coordiantes qx and qy on the xy plane). It then returns the minimum distance. 
    
    '''
   
    def __init__(self,x1,y1,x2,y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        
        
    def minDistanceFromPoint(self,qx,qy):
        v = (self.x2-self.x1, self.y2-self.y1)  #vector representing line segment, which is v = (x2-x1, y2-y1)
        u = (qx-self.x1, qy-self.y1)            #vector from start point of the line segment to the point q, which is u = (qx-x1, qy-y1)
        
        vu = v[0]*u[0] + v[1]*u[1]              #Calculate dot product of vectors v and u, which is v·u = (x2-x1)(qx-x1) + (y2-y1)(qy-y1)
        vv = v[0]*v[0] + v[1]*v[1]              #Calculate squared length of vector v, which is v·v = (x2-x1)^2 + (y2-y1)^2
        if vv == 0:
            return 0
        t = vu / vv                             #Calculate parameter t = v·u / v·v, which represents position of projection of point q on the line
        
        
        #Calculate the coordinates of q' which I named qx_proj, qy_proj
        #t is used to determine if it is better to calculate distance from projection or end points
        if t < 0:
            qx_proj, qy_proj = self.x1, self.y1
        elif t > 1:
            qx_proj, qy_proj = self.x2, self.y2
        else:
            qx_proj, qy_proj = self.x1 + t*(self.x2-self.x1), self.y1 + t*(self.y2-self.y1)
        
        
        d = ((qx-qx_proj)**2 + (qy-qy_proj)**2)**0.5 #d is the distance between the point q and its projection (q') on the line
        return d 
        
    # Define the distance
    def dist(self):

        # Calculate the Euclidean distance between two points
        return math.sqrt((self.x2 - self.x1)**2 + (self.y2 - self.y1)**2)
