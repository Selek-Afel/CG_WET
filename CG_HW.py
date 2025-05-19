import ComputationalGeometryLib as CG
import sys
from sortedcontainers import SortedList

# array that stores the priority queues of events for each test case
event_points = []

# array that stores the number of intersections for each test case
# (initially set to 0)
intersections = []

# array that stores the event trees for each test case
# used for checking if the intersection point is inside the event tree
# (initially set to empty)
segment_pairs = []

def above_and_below(seg, status): # (Segment, AVLtree) -> Segment
    # Check for intersections with the segment above and below
    lower_index = status.bisect_left(seg)-1
    upper_index = status.bisect_right(seg)
    if lower_index >= 0:
        below = status[lower_index]
    else:
        below = None
    if upper_index < len(status):
        above = status[upper_index]
    else:
        above = None
    return below, above

def swap_segments_at_intersection(status, seg1, seg2, intersection): # (AVLtree, Segment, Segment, Point) -> void
    # Swap the segments in the status
    # This is done to maintain the order of the segments in the status
    status.remove(seg1)
    status.remove(seg2)
    seg1.p = intersection
    seg2.p = intersection
    status.add(seg1)
    status.add(seg2)
    
# Read the input from standard input
lines = sys.stdin.readlines()

test_cases = int(lines[0].strip())
index = 1

# Read the input file
for i in range(test_cases):
    n = int(lines[index].strip())
    if n == -1:
        break
    index += 1
    segments = 0
    event_points.append(CG.CG24PriorityQueue())
    for j in range(n):
        x1, y1, x2, y2 = map(float, lines[index].strip().split())
        index += 1
        p1 = CG.Point(x1, y1, None, None, None)
        p2 = CG.Point(x2, y2, None, None, None)
        if p1.x < p2.x:
            p1.eventType = CG.EventType.START
            p2.eventType = CG.EventType.END
        elif p1.x > p2.x:
            p1.eventType = CG.EventType.END
            p2.eventType = CG.EventType.START
        # assuming no vertical lines
        seg = CG.Segment(p1, p2, segments)
        p1.segment = seg
        p2.segment = p1.segment
        event_points[i].insert(p1)
        event_points[i].insert(p2)
        segments += 1
    

# Sweep line algorithm
intersection_pts = []
for i in range(test_cases):
    intersections.append(0)
    intersection_pts.append([])
    segment_pairs.append(SortedList()) # for event points
    status = SortedList() # AVL tree for the status of the segments
    while not event_points[i].empty():
        event = event_points[i].pop()
        
        
        if event.eventType == CG.EventType.START:
            status.add(event.segment)
            # Check for intersections with the segment above and below
            below, above = above_and_below(event.segment, status)
            if above is not None: # Check for intersection with the segment above
                intersection = CG.intersection(event.segment, above)
                if intersection is not None and segment_pairs[i].count((intersection.segment.id, intersection.segment2.id)) == 0:
                    event_points[i].insert(intersection)
                    segment_pairs[i].add((intersection.segment.id, intersection.segment2.id))
            if below is not None: # Check for intersection with the segment below
                intersection = CG.intersection(event.segment, below)
                if intersection is not None and segment_pairs[i].count((intersection.segment.id, intersection.segment2.id)) == 0:
                    event_points[i].insert(intersection)
                    segment_pairs[i].add((intersection.segment.id, intersection.segment2.id))
        
        
        elif event.eventType == CG.EventType.END:
            # Check for intersections with the segment above and below
            below, above = above_and_below(event.segment, status)
            status.remove(event.segment)
            if above is not None and below is not None:
                intersection = CG.intersection(above, below)
                if intersection is not None and segment_pairs[i].count((intersection.segment.id, intersection.segment2.id)) == 0:
                    event_points[i].insert(intersection)
                    segment_pairs[i].add((intersection.segment.id, intersection.segment2.id))
        
        
        elif event.eventType == CG.EventType.INTERSECTION:
            intersection_pts[i].append(event)
            intersections[i] += 1
            # Check for intersections with the segments above and below
            # This comparison is calculated based on the start of the segments
            if(event.segment < event.segment2):
                lower_index = status.bisect_left(event.segment)-1
                upper_index = status.bisect_right(event.segment2)
                if upper_index < len(status):
                    above = status[upper_index]
                    intersection = CG.intersection(above, event.segment)
                    if intersection is not None and segment_pairs[i].count((intersection.segment.id, intersection.segment2.id)) == 0:
                        event_points[i].insert(intersection)
                        segment_pairs[i].add((intersection.segment.id, intersection.segment2.id))
                if lower_index >= 0:
                    below = status[lower_index]
                    intersection = CG.intersection(below, event.segment2)
                    if intersection is not None and segment_pairs[i].count((intersection.segment.id, intersection.segment2.id)) == 0:
                        event_points[i].insert(intersection)
                        segment_pairs[i].add((intersection.segment.id, intersection.segment2.id))
            else:
                lower_index = status.bisect_left(event.segment2)-1
                upper_index = status.bisect_right(event.segment)
                if upper_index < len(status):
                    above = status[upper_index]
                    intersection = CG.intersection(above, event.segment2)
                    if intersection is not None and segment_pairs[i].count((intersection.segment.id, intersection.segment2.id)) == 0:
                        event_points[i].insert(intersection)
                        segment_pairs[i].add((intersection.segment.id, intersection.segment2.id))
                if lower_index >= 0:
                    below = status[lower_index]
                    intersection = CG.intersection(below, event.segment)
                    if intersection is not None and segment_pairs[i].count((intersection.segment.id, intersection.segment2.id)) == 0:
                        event_points[i].insert(intersection)
                        segment_pairs[i].add((intersection.segment.id, intersection.segment2.id))
                        
            # Swap the segments in the status
            # This is done to maintain the order of the segments in the status
            swap_segments_at_intersection(status, event.segment, event.segment2, event)
    print(intersections[i], '\n')

    # for pt in intersection_pts[i]:
    #     print(pt.x, " ", pt.y, " \n")