import numpy as np
import cv2
import pickle

def makePretty(img):
    out=np.zeros((512,512,3),dtype=np.uint8)
    out[img==0]=(255,200,200)
    out[img==1]=(40,60,100)
    return out

def show(img, wait=0):
    if img.dtype != np.uint8:
        img = normalize(img)
    cv2.imshow("img", img)
    cv2.waitKey(wait)

def save(path, img):
    if img.dtype != np.uint8:
        img = normalize(img)
    cv2.imwrite(path, img)

def normalize(img):
    if img.dtype == bool:
        return np.uint8(255 * img)
    img = img * 1.0
    output = img - img.min()
    output = img / img.max()
    return np.uint8(255 * output)

def loadCave(filename):
    cave_bytes=np.fromfile(filename, dtype=np.uint8)
    cave_bits=np.unpackbits(cave_bytes)
    cave=np.reshape(cave_bits,(512,512,512))
    return cave

def saveCave(cave,filename):
	np.packbits(np.uint8(np.ravel(cave))).tofile(filename)

cave=loadCave("input.cave")
import time
start=time.time()
ogCave=cave*1
dirt_before = ogCave.sum()
print("dirt before", dirt_before)
print("air before",(1-ogCave).sum())
x,y,z=200,200,200
size=41
wall=5
buff=5

def makeDwelling(cave, x,y,z):
    cave = cave.copy()
    centerDirt = cave[x-size//2:x+size//2+1,y-size//2:y+size//2+1,z-size//2:z+size//2+1].sum()
    cave[x-size//2-wall:x+size//2+1+wall,y-size//2-wall:y+size//2+1+wall,z-size//2-wall:z+size//2+1+wall] = 1
    cave[x-size//2:x+size//2+1,y-size//2:y+size//2+1,z-size//2:z+size//2+1] = 0
    return cave, centerDirt

def fillDirt(cave, dirt_amount):
    # Get the coordinates of existing dirt pieces
    dirt_coords = np.argwhere(cave == 1)

    # Randomly select coordinates in the empty space adjacent to at least two other dirt pieces
    while dirt_amount > 0:
        empty_coords = np.argwhere(cave == 0)
        selected_coord = None

        for coord in empty_coords:
            # show(cv2.circle(makePretty(cave[:,:,coord[2]]), (coord[1], coord[0]), 10, (0, 0, 255), 5), 1)
            # Check if the empty coordinate is adjacent to at least two other dirt pieces
            if np.sum(np.abs(dirt_coords - coord) == 1) >= 2:
                selected_coord = coord
                break

        if selected_coord is not None:
            # show(cv2.circle(makePretty(cave[:,:,selected_coord[2]]), (selected_coord[1], selected_coord[0]), 10, (0, 255, 0), 5), 1)
            cave[selected_coord[0], selected_coord[1], selected_coord[2]] = 1
            dirt_coords = np.vstack([dirt_coords, selected_coord])
            dirt_amount -= 1
            print("dirt left:", dirt_amount, end="\r")
        else:
            # If no suitable empty coordinate is found, break the loop
            break

def fillDirt2(ogCave, x, y, z, dirt_amount):
    original_cave = ogCave.copy()
    tempCave = ogCave.copy()
    tempCave[x-size//2-wall:x+size//2+1+wall,y-size//2-wall:y+size//2+1+wall,z-size//2-wall:z+size//2+1+wall] = 1

    slice = tempCave[x-size//2-wall-buff:x+size//2+1+wall+buff,y-size//2-wall-buff:y+size//2+1+wall+buff,z-size//2-wall-buff:z+size//2+1+wall+buff]

    spaces = np.argwhere(slice == 0)
    spaces[:, 0] += x-size//2-wall-buff
    spaces[:, 1] += y-size//2-wall-buff
    spaces[:, 2] += z-size//2-wall-buff
    
    first_dirt = 0
    # find the first space that is next to a dirt piece
    for i in range(len(spaces)):
        spacex, spacey, spacez = spaces[i]
        if np.sum(np.abs(original_cave[spacex-1:spacex+2, spacey-1:spacey+2, spacez-1:spacez+2] - 1)) > 0:
            first_dirt = i
            break

    original_cave[spaces[first_dirt:dirt_amount,0], spaces[first_dirt:dirt_amount,1], spaces[first_dirt:dirt_amount, 2]] = 1
    return original_cave

# results = {}
# for z in range((size+wall)//2, 512-(size+wall)//2, 20):
#     for y in range((size+wall)//2, 512-(size+wall)//2, 20):
#         for x in range((size+wall)//2, 512-(size+wall)//2, 20):
#             _, centerDirt = makeDwelling(cave, x,y,z)
#             print("center:", centerDirt, end="\r")
#             out = makePretty(cave[:,:,z])
#             cv2.rectangle(out, (y-size//2,x-size//2), (y+size//2,x+size//2), (0,255,0), 3)
#             show(out, 1)
#             results[(x,y,z)] = centerDirt

# with open("results.pkl", "wb") as f:
#     pickle.dump(results, f)

# with open("results.pkl", "rb") as f:
#     results = pickle.load(f)

# locations = []
# results = list(results.items())
# np.random.seed(2456785)
# while len(locations) < 4:
#     j = np.random.randint(len(results))
#     x, y, z = results.pop(j)[0]
#     if x < 100 or y < 100 or z < 100:
#         continue
#     newCave, centerDirt = makeDwelling(cave, x,y,z)
#     dirt_after = newCave.sum()
#     dirt_needed = dirt_before - dirt_after
#     if dirt_needed > 0:
#         newCave = fillDirt2(newCave, x, y, z, dirt_needed)
#     else:
#         continue

#     cost = int(np.abs(newCave*1.0-ogCave).sum())
#     if cost > 80000:
#         continue
#     dirt_after = newCave.sum()
#     if dirt_after - dirt_before != 0:
#         continue
#     print(f"cost of {len(locations)}:", cost)
    # show(makePretty(newCave[:,:,z]))
    # show(makePretty(newCave[:,:,0]))
    # def side_change(val):
    #     cv2.imshow("side view", makePretty(newCave[:,val,:].T))
    # cv2.imshow("side view", makePretty(newCave[:,0,:].T))
    # cv2.createTrackbar('slider', "side view", y, 511, side_change)
    # def top_change(val):
    #     cv2.imshow("top view", makePretty(newCave[:,:,val]))
    # cv2.imshow("top view", makePretty(newCave[:,:,0].T))
    # cv2.createTrackbar('slider', "top view", z, 511, top_change)
    # cv2.waitKey(0)

    # saveCave(newCave, f"dwelling{len(locations)}_{x}_{y}_{z}_{cost}_patelj24.cave.cave")
    # locations.append((x,y,z))
    # if len(locations) == 4:
    #     with open("locations.pkl", "wb") as f:
    #         pickle.dump(locations, f)
    #     break

# with open("locations.pkl", "rb") as f:
#     locations = pickle.load(f)

import os
filenames = os.listdir()
for filename in filenames:
    if not filename.endswith(".cave") or filename.startswith("input"):
        filenames.remove(filename)
filenames.sort()
def side_change(val):
    cv2.imshow("side view", makePretty(cave[:,val,:].T))
def top_change(val):
    cv2.imshow("top view", makePretty(cave[:,:,val]))
cave = loadCave(filenames[0])
cv2.imshow("side view", makePretty(cave[:,y,:].T))
cv2.imshow("top view", makePretty(cave[:,:,z].T))
cv2.createTrackbar('slider', "side view", y, 511, side_change)
cv2.createTrackbar('slider', "top view", z, 511, top_change)
for i in range(len(filenames)):
    print(filenames[i])
    x, y, z, cost = [int(x) for x in filenames[i].split("_")[1:-1]]
    print(x,y,z)
    cave = loadCave(filenames[i])
    print(f"cost of {i}:", cost)
    print("Change in dirt:", cave.sum() - dirt_before)
    # show(makePretty(cave[:,:,z]))
    cv2.imshow("side view", makePretty(cave[:,y,:].T))
    cv2.imshow("top view", makePretty(cave[:,:,z].T))
    cv2.waitKey(0)

# end=time.time()
# print("Time elapsed:", end-start)


#slider code
# def side_change(val):
#     cv2.imshow("side view", makePretty(cave[:,val,:].T))
# cv2.imshow("side view", makePretty(cave[:,0,:].T))
# cv2.createTrackbar('slider', "side view", 0, 511, side_change)
# def top_change(val):
#     cv2.imshow("top view", makePretty(cave[:,:,val]))
# cv2.imshow("top view", makePretty(cave[:,:,0].T))
# cv2.createTrackbar('slider', "top view", 0, 511, top_change)
# cv2.waitKey(0)






