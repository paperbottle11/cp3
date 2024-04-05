words = [word.strip().upper() for word in open('20k.txt')]
partials = set(word[:i+1] for word in words for i in range(len(word)))
partials.add("")

def get_neighbors(x,y):
    for i in range(-1,2):
        for j in range(-1,2):
            if (i,j) == (0,0):
                continue
            if 0 <= x+i < 10 and 0 <= y+j < 10:
               yield (x+i,y+j)

found_words = set()
stack = [[(x,y)] for y in range(10) for x in range(10)]

# seed=6923313
board = [['I', 'C', 'A', 'N', 'T', 'P', 'O', 'A', 'L', 'E'],
         ['N', 'W', 'Y', 'T', 'M', 'L', 'I', 'I', 'S', 'I'],
         ['H', 'R', 'D', 'I', 'I', 'S', 'I', 'T', 'S', 'U'],
         ['R', 'T', 'G', 'T', 'O', 'A', 'A', 'E', 'G', 'I'],
         ['S', 'R', 'G', 'I', 'I', 'E', 'I', 'R', 'A', 'C'],
         ['E', 'N', 'Y', 'S', 'E', 'S', 'P', 'E', 'E', 'X'],
         ['N', 'I', 'T', 'Y', 'N', 'S', 'E', 'N', 'R', 'R'],
         ['B', 'E', 'T', 'G', 'T', 'B', 'R', 'U', 'O', 'E'],
         ['N', 'E', 'S', 'N', 'U', 'I', 'N', 'C', 'E', 'U'],
         ['O', 'D', 'S', 'A', 'O', 'L', 'U', 'O', 'I', 'S']]

import time
start_time = time.time()

while stack:
    path = stack.pop()
    word = ""
    for x,y in path:
        word += board[y][x]
    
    if word in words:
        found_words.add(word)

    end = path[-1]
    for neighbor in get_neighbors(*end):
        if neighbor in path:
            continue
        new_path = path.copy()
        new_path.append(neighbor)
        new_word = ""
        for x,y in path:
            new_word += board[y][x]
        if new_word in partials:
            stack.append(new_path)

print("Time elapsed:", time.time() - start_time)
print("Found words:", len(found_words))

lengths = [len(word) for word in found_words]
max_length = max(lengths)
print("Max length:", max_length)
print("Words of max length:")
for word in found_words:
    if len(word) == max_length:
        print(word)