import pickle
import math
import cv2
import numpy as np
import heapq
import pygame
import sys

class PriorityQueue:
	def __init__(self):
		self.q=[]
		self.lookup={}
		self.i=0
		
	def add(self,cost,elem): 
		if elem in self.lookup:
			if self.lookup[elem][0]>cost:
				self.remove(elem)
			else:
				return
		entry=[cost,-self.i,elem]
		self.i+=1
		heapq.heappush(self.q,entry)
		self.lookup[elem]=entry
	
	def pop(self):
		elem=False
		while not elem:
			cost,_,elem=heapq.heappop(self.q)   
		self.lookup.pop(elem)
		return elem
	
	def remove(self,elem):
		entry=self.lookup.pop(elem)
		entry[-1]=False
		
	def __len__(self):
		return len(self.lookup)

def find_closest(point,nodes):
    x1,y1=point
    dist=100000000
    closest=None
    for x2,y2 in nodes:
        d=math.hypot(x1-x2,y1-y2)
        if d<dist:
            dist=d
            closest=(x2,y2)
    return closest

def scale_point(point):
    x,y=point
    x=(x-minx)/(maxx-minx)*width
    y=length-(y-miny)/(maxy-miny)*length
    return x,y

def draw_line(point1,point2,color=(0,0,0),width=1):
    scaled_point1=scale_point(point1)
    scaled_point2=scale_point(point2)
    pygame.draw.line(screen, color, scaled_point1, scaled_point2, width)

def draw_point(point, color=(0,0,0), width=1):
    scaled_point=scale_point(point)
    pygame.draw.circle(screen, color, scaled_point, width)

def heuristic(x,y):
	return (abs(x-end[0])+abs(y-end[1]))*.9

def haversine(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1/10**5, lon1/10**5, lat2/10**5, lon2/10**5])

    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2) ** 2
    c = 2 * np.arcsin(np.sqrt(a))

    radius_earth_km = 6371.0
    distance_km = radius_earth_km * c

    return distance_km

# Initialize Pygame
pygame.init()

# Set up the canvas
width=270*2
length=240*2
canvas_size = (width, length)
screen = pygame.display.set_mode(canvas_size)
pygame.display.set_caption("Draw Lines")

nodes=pickle.load(open("roads_processed.pickle","rb"))

maxx=-10000000000
maxy=-10000000000
minx=10000000000
miny=10000000000
for x,y in nodes:
    if x<minx:
        minx=x
    if x>maxx:
        maxx=x
    if y<miny:
        miny=y
    if y>maxy:
        maxy=y

# Set up colors (BGR)
WHITE = (255, 255, 255)
ORANGE = (0, 140, 255)
BLACK = (0, 0, 0)

screen.fill(WHITE)
for point1 in nodes:
    for point2 in nodes[point1]:
        draw_line(point1,point2)     
pygame.display.flip()

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
fps = 30
video_writer = cv2.VideoWriter('output.mp4', fourcc, fps, canvas_size)

road_width = 5
city_width = 7

# Hot Springs
start = (-9305798, 3451807)
start = find_closest(start,nodes)
draw_point(start,(0,0,255),city_width)

# Blytheville
end = (-8991892, 3589060)
end = find_closest(end,nodes)
draw_point(end,(0,255,0),city_width)

# Little Rock
draw_point((-9232533, 3473500), ORANGE, city_width)
# Jonesboro
draw_point((-9068983, 3582350), ORANGE, city_width)

explored = set()
queue = PriorityQueue()
queue.add(heuristic(*start),start)

# A* Search Algorithm
i=0
last_point = start
distance_km = 0
running=True
while queue and running:
    point=queue.pop()
    distance_km += haversine(last_point[1], last_point[0], point[1], point[0])
    if point == end:
          break
    explored.add(point)
    last_point = point
    for point2 in nodes[point]:
        if point2 not in explored:
            queue.add(heuristic(*point2), point2)
            draw_line(point,point2,(255,0,0),road_width)
            
            # Save the frame
            i+=1
            if i%8==0:
                pygame.display.flip()
                frame = pygame.surfarray.array3d(screen)
                frame = np.swapaxes(frame, 0, 1)
                video_writer.write(frame)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

video_writer.release()

# Calculations
print("KM:", distance_km)
distance_M = distance_km*0.621371
print("Miles:", distance_M)

# Assumed constants
human_mph = 4
sleep_hours = 6
number_meals = 3
meal_time = 0.5

hours = distance_M / human_mph
print("Walking Hours:", hours)
days = hours % 24

hours += days * sleep_hours
hours += days * number_meals * meal_time

print("Total hours:", hours)

# Hot Springs to Blytheville
# KM: 681.8671826327146
# Miles: 423.69249313967254
# Walking Hours: 105.92312328491813
# Total hours: 180.34654792180416

# Quit Pygame
pygame.quit()
sys.exit()
