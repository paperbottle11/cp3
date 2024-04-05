import numpy as np
import cv2

def show(img,size=500,wait=0,):
    out=cv2.resize(img,(size,size),interpolation=cv2.INTER_NEAREST)
    cv2.imshow("img", out)
    cv2.waitKey(wait)

def check_white(img, y, x):
    return (img[y, x][0] == 255 and img[y, x][1] == 255 and img[y, x][2] == 255)

def check_green(img, y, x):
    return (img[y, x][0] == 0 and img[y, x][1] == 255 and img[y, x][2] == 0)

maze = cv2.imread("maze.png")
maze[1,1] = (255,0,0)
show(maze)

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
fps = 60
final_size = (1000, 1000)
video_writer = cv2.VideoWriter('right.mp4', fourcc, fps, final_size)

green_index = np.where((maze[:,:,1] == 255) & (maze[:,:,0] == 0) & (maze[:,:,2] == 0))
yf, xf = green_index[0][0], green_index[1][0]
maze[yf, xf] = (255,255,255)

deque = [(1,1,1)]
while deque:
    y, x, length = deque[-1]
    if len(deque) > 1: maze[deque[-2][0], deque[-2][1]] = (255,0,0)
    maze[y, x] = (0,0,255)
    if y == yf and x == xf:
        out = maze * 1
        out[yf, xf] = (0,255,0)
        show(out, wait=1)
        print(length)
        video_writer.write(cv2.resize(out, final_size, interpolation=cv2.INTER_NEAREST))
        break
    
    if check_white(maze, y+1, x):
        deque.append((y+1, x, length+1))
    elif check_white(maze, y, x-1):
        deque.append((y, x-1, length+1))
    elif check_white(maze, y-1, x):
        deque.append((y-1, x, length+1))
    elif check_white(maze, y, x+1):
        deque.append((y, x+1, length+1))
    else:
        deque.pop()
    out = maze * 1
    out[yf, xf] = (0,255,0)
    show(out, wait=1)
    video_writer.write(cv2.resize(out, final_size, interpolation=cv2.INTER_NEAREST))

show(maze)
for point in reversed(deque):
    maze[point[0], point[1]] = (0,255,0)
    show(maze, wait=1)
    video_writer.write(cv2.resize(maze, final_size, interpolation=cv2.INTER_NEAREST))
video_writer.release()