from enum import Enum
from Lib import heapq

class EventType(Enum):
    START = 1
    END   = 2
    INTERSECTION = 3
# An enum to identify the type of event in the sweep line algorithm.
class Point:
    x : float # float
    y : float # float
    eventType : EventType # EventType
    segment : 'Segment' # The segment associated with the event.
    segment2 : 'Segment' # The second segment associated with the event.
    
    def __init__(self, x = 0, y = 0, event = EventType.START, segment = None, segment2 = None):
        self.eventType = event
        self.x = x
        self.y = y
        self.segment = segment
        self.segment2 = segment2
    # def
    def __lt__(self, other): # (Point) -> bool
        if self.x == other.x:
            return self.y < other.y
        else:
            return self.x < other.x
    # def
    def __eq__(self, other): # (Point) -> bool
        if(other is None):
            return (self is None)
        return (self.x == other.x and self.y == other.y)
    # def
    def __ne__(self, other): # (Point) -> bool
        return not self.__eq__(other)
    # def
    def __gt__(self, other): # (Point) -> bool
        return not (self < other or self == other) # if self is not less than other and not equal to other
    # def
    def __le__(self, other): # (Point) -> bool
        return not self.__gt__(other) # if self is not greater than other
    # def
    def __ge__(self, other): # (Point) -> bool
        return not self.__lt__(other) # if self is not less than other
    # def
# def
    
# class

class Segment:
    id : int # to overcome numerical error when we find a point on an ...
    #    # already-known segment we identify segments with unique ID.
    #    # binary search with numerical errors is guaranteed to find an ...
    #    # index whose distance from the correct one is O(1) (here it is 2).
    #
    p : Point # Point, after input we compare and swap to guarantee that p.x <= q.x
    q : Point # Point
    _a : float # double, slope of the segment
    _b : float # double, y-intercept of the segment
    
    def __init__(self,p,q, id = 0):
        self.id = id
        if p.x > q.x:
            p,q = q,p
        self.p = p
        self.q = q
        self._a = (self.p.y - self.q.y) / (self.p.x - self.q.x)
        self._b = self.p.y - (self._a * self.p.x)
        self.treeNode = None
    # def
    
    # line: y = ax + b. it is guaranteed that the line is not vertical (a is finite)
    def a(self): # () -> double
        return self._a
    # def
    
    def b(self): # () -> double
        return self._b
    # def
    
    # the y-coordinate of the point on the segment whose x-coordinate ..
    #   is given. Segment boundaries are NOT enforced here.
    def calc(self, x):
        return (self.a() * (x))+self.b()
    # def
    def __lt__(self, other): # (Segment) -> bool
        if(self.id == other.id):
            return False
        if self.p.x < other.p.x:
            return other.__gt__(self) # if self is to the left of other
        else:
            if(self.p.x == other.p.x):
                return self.p.y < other.p.y
            return self.p.y < other.calc(self.p.x) # if self is below other
    # def
    def __eq__(self, other):
        return (self.id == other.id)
    # def
    def __ne__(self, other):
        return not self.__eq__(other)
    # def
    def __gt__(self, other): # (Segment) -> bool
        if self.id == other.id:
            return False
        if self.p.x < other.p.x:
            return other.__lt__(self)
        else:
            if self.p.x == other.p.x:
                return self.p.y > other.p.y
            return self.p.y > other.calc(self.p.x)
    # if self is above other
    # def
    
    def __le__(self, other): # (Segment) -> bool
        return self.__eq__(other) or self.__lt__(other) # if self is not above other
    # def
    def __ge__(self, other): # (Segment) -> bool
        return self.__eq__(other) or self.__gt__(other) # if self is not below other
    # def
            
            
# class

def is_left_turn(a, b, c): # (Point,Point,Point) -> bool
    x1 = a.x
    x2 = b.x
    x3 = c.x
    y1 = a.y
    y2 = b.y
    y3 = c.y
    return ((x1 * (y2 - y3)) + (x2 * (y3 - y1)) + (x3 * (y1 - y2))) > 0
# def
def intersection(s1, s2): # (segment,segment) -> Point | None
    if ((is_left_turn(s1.p, s1.q, s2.p) != is_left_turn(s1.p, s1.q, s2.q)) and
        (is_left_turn(s2.p, s2.q, s1.p) != is_left_turn(s2.p, s2.q, s1.q))):
        
        a1 = s1.a()
        a2 = s2.a()

        b1 = s1.b()
        b2 = s2.b()

        # commutation consistency: sort by a (then by b)
        if a1 > a2 or (a1 == a2 and b1 > b2):
            a1,a2 = a2,a1
            b1,b2 = b2,b1
        # if

        #
        # a1 x + b1 = y
        # a2 x + b2 = y
        # (a1 - a2)x + (b1-b2) = 0
        # x = (b2-b1)/(a1-a2)
        #

        x = (b2 - b1) / (a1 - a2)
        y = a1 * x + b1
        if(s1.id < s2.id):
            return Point(x, y, EventType.INTERSECTION, s1, s2)
        else:
            return Point(x, y, EventType.INTERSECTION, s2, s1)
    else:
        return None
    #else
#def

def intersects(s1, s2): # (Segment,Segment) -> bool
    return not(intersection(s1, s2) is None)
#def


class CG24PriorityQueue:
    arr  : any # any[]
    
    def __init__(self, priorityMax=True, tiebreakerMax=True, tiebreaker2Max=True):
        self.arr  = []
    # def
    
    def insert(self, data): # (any, double[, double[, double]]) -> void
        heapq.heappush(self.arr, data)
    # def
    
    def empty(self): # () -> bool
        return len(self.arr) == 0
    # def
    
    def pop(self): # () -> any
        if self.empty():
            return None
        else:
            return heapq.heappop(self.arr)
    # def
# class

    