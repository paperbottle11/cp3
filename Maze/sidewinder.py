import numpy as np
import cv2
import random

def show(img,size=500,wait=0):
    out=cv2.resize(img,(size,size),interpolation=cv2.INTER_NEAREST)
    cv2.imshow("img", out)
    cv2.waitKey(wait)

dim = (25,25)
white = (255,255,255)
red = (0,0,255)

maze = np.zeros((2*dim[0]+1, 2*dim[1]+1, 3), dtype=np.uint8)
h, w = maze.shape[:2]
maze[1::2, 1::2] = white

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
fps = 60
final_size = (1000, 1000)
video_writer = cv2.VideoWriter('sidewinder.mp4', fourcc, fps, final_size)

run_set = [(1,1)]
while run_set:
    y, x = run_set[-1]
    maze[y, x] = red
    if (random.random() > 0.5 or y-1 == 0) and x+2 < w :
        maze[y, x+1] = red
        run_set.append((y, x+2))
    else:
        y2, x2 = random.choice(run_set)
        if y2-1 != 0:
            maze[y2-1, x2] = white
        maze[y, x] = white
        maze[y2, run_set[0][1]:run_set[-1][1]] = white
        run_set.clear()
        
        if x+2 < w:
            run_set.append((y, x+2))
        elif y+2 < h:
            run_set.append((y+2, 1))
    show(maze, wait=1)
    video_writer.write(cv2.resize(maze, final_size, interpolation=cv2.INTER_NEAREST))
video_writer.release()
show(maze)
# cv2.imwrite("maze.png", maze)