"""
asdf
     asdf 
	 		sdfg
	dfg


	fdg abcdefghijklmnopqrstuvwxyz
"""
from heapq import *

class PQueue:
	def __init__(self):
		self.pq = []                         # list of entries arranged in a heap
		self.entry_finder = {}               # mapping of tasks to entries

	def add(self,item, priority):
		'Add a new task or update the priority of an existing task'
		if item in self.entry_finder:
			if priority>self.entry_finder[item][0]:
				return 
			self.remove(item)
		entry = [priority,item,True]
		self.entry_finder[item] = entry
		heappush(self.pq, entry)

	def remove(self,item):
		'Mark an existing task as REMOVED.  Raise KeyError if not found.'
		entry = self.entry_finder.pop(item)
		entry[-1] = False

	def pop(self,):
		'Remove and return the lowest priority task. Raise KeyError if empty.'
		while self.pq:
			priority, item, is_alive = heappop(self.pq)
			if is_alive:
				del self.entry_finder[item]
				return priority,item
		raise KeyError('pop from an empty priority queue')

# pq=PQueue()
# pq.add(6,7)
# pq.add(5,4)
# print(pq.pop())
# input()


import cv2
import numpy as np
import time

def show(img,wait=1):
	img=cv2.resize(img,None,fx=4,fy=4,interpolation=cv2.INTER_NEAREST)
	cv2.imshow("img", img)
	cv2.waitKey(wait)
	# ~ cv2.destroyAllWindows() 

def get_costs():
	X,Y=np.mgrid[:100,:100]*1.0
	X-=50.0
	Y-=50.0
	cost=X**2+Y**2
	cost*=-1
	cost-=cost.min()
	cost/=cost.max()
	cost*=254
	cost=np.uint8(cost+1)
	return cost

img=np.zeros((100,100),dtype=np.uint8)


start=(10,10)
end=(90,90)



explored=set()
cost_map=get_costs()
show(cost_map,0)
pq=PQueue()
pq.add(start,0)
# pq = [(0,start)]
costs=np.uint64(cost_map*0)

start_time=time.time()
while pq:
	cost,location=pq.pop()
	costs[location]=cost
	#cost,location=pq.pop(0)
	if location in explored:
		img[location]=255
		show(img)
		continue
	explored.add(location)
	if location == end:
		break
	for dx,dy in [(1,0),(-1,0),(0,-1),(0,1)]:
		x,y=location
		x+=dx
		y+=dy
		if 0 <= x < 100 > y >= 0:
			new_cost=cost+cost_map[x,y]
			pq.add((x,y),new_cost)

costs=costs*1.0
costs/=costs.max()
costs*=255
show(np.uint8(costs),0)
print(time.time()-start_time)