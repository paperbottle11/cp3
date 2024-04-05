import numpy as np
import cv2
import random

def show(img,size=500,wait=0):
    out=cv2.resize(img,(size,size),interpolation=cv2.INTER_NEAREST)
    cv2.imshow("img", out)
    cv2.waitKey(wait)

def get_neighbors(point, maze):
    y, x = point
    for dx, dy in [(1,0),(0,1),(-1,0),(0,-1)]:
        yp = y+2*dy
        xp = x+2*dx
        if xp < 0 or yp < 0 or xp >= maze.shape[1] or yp >= maze.shape[0] or maze[yp,xp,0] == 255 or maze[yp,xp,0] == 0:
            continue
        yield yp, xp

dim = (25,25)
white = (255,255,255)
gray = (150,150,150)
red = (0,0,255)

maze = np.zeros((2*dim[0]+1, 2*dim[1]+1, 3), dtype=np.uint8)
h, w = maze.shape[:2]
maze[1::2, 1::2] = gray

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
fps = 60
final_size = (1000, 1000)
video_writer = cv2.VideoWriter('recursiveBacktrack.mp4', fourcc, fps, final_size)

deque = [(1,1)]
while deque:
    node = deque[-1]
    y, x = node
    neighbors = list(get_neighbors(node, maze))
    if neighbors:
        y2, x2 = random.choice(neighbors)
        maze[y,x] = red
        maze[y2,x2] = red
        maze[(y+y2)//2, (x+x2)//2] = red
        deque.append((y2, x2))
        show(maze, wait=1)
        video_writer.write(cv2.resize(maze, final_size, interpolation=cv2.INTER_NEAREST))
    else:
        maze[y,x] = white
        deque.pop()
        if deque:
            maze[(deque[-1][0]+y)//2, (deque[-1][1]+x)//2] = white

show(maze)