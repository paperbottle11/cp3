import numpy as np
import cv2
import heapq

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

def show(img,wait=0):
	img=cv2.resize(img,None,fx=1,fy=1,interpolation=cv2.INTER_NEAREST)
	cv2.imshow("img",img)
	cv2.waitKey(wait)

def normalize(x):
	x=x*1.0
	x-=x.min()
	x/=x.max()
	x*=255.999
	return np.uint8(x)

terrain = cv2.imread("terrain.png")
h,w, _ = terrain.shape
map = np.zeros((w,h),dtype=np.uint8)

cost_key = {(0,0,0): 255,
			 (255,0,0): 50,
			 (0,255,0): 15,
			 (255,255,255): 5,
			 (128,128,128): 1}
for k,v in cost_key.items():
	map[np.all(terrain==k,axis=-1)]=v

costs=map*0.0-1

starty,startx = 15,75
endy,endx =250,700
costs[starty,startx]=0

def heuristic(x,y):
	return (abs(x-endx)+abs(y-endy))*.9
def trace_heuristic(x,y):
	return (abs(x-startx)+abs(y-starty))*.9

queue=PriorityQueue()
queue.add(0,(starty,startx))

i=0
show(normalize(costs))
while queue:
	i+=1
	cx,cy=queue.pop()
	if cx==endy and cy==endx:
		break
	ccost=costs[cx,cy]
	if i%1000==0:
		show(normalize(costs),1)
	for dx,dy in (1,0),(-1,0),(0,1),(0,-1):
		px=cx+dx
		py=cy+dy
		if px<0 or px>=w or py<0 or py>=h:
			continue
		pcost=ccost+map[px,py]
		if costs[px,py]==-1 or pcost<costs[px,py]:
			costs[px,py]=pcost
			queue.add(pcost+heuristic(px,py),(px,py))


path=[(endy,endx)]
traced = terrain.copy()
traced[endy,endx] = [0,0,255]
while path[0]!=(starty,startx):
	x,y=path[0]
	cost_list = {}
	for dx,dy in (1,0),(-1,0),(0,1),(0,-1):
		px=x+dx
		py=y+dy
		if px<0 or px>=w or py<0 or py>=h or (px,py) in path or costs[px,py] == -1:
			continue
		cost_list[costs[px,py] + trace_heuristic(px,py)] = (dx,dy)
	path.insert(0,(x+cost_list[min(cost_list)][0],y+cost_list[min(cost_list)][1]))
	traced[path[0][0],path[0][1]] = [0,0,255]
	show(traced,1)
show(traced)