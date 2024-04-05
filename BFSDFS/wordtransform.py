words = set([word.strip().upper() for word in open('20k.txt')])

def get_transformations(word, haystack):
    # Remove letters
    for i in range(len(word)):
        yield word[:i] + word[i+1:]
    # Change letters
    for i in range(len(word)):
        for new_letter in haystack:
            if new_letter != word[i]:
                yield word[:i] + new_letter + word[i+1:]
    # Add letters
    for i in range(len(word) + 1):
        for letter in haystack:
            yield word[:i] + letter + word[i:]

letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
letter_set = set(letters)

start = "FOX"
end = "HOUND"

paths = []
found_words = {}

queue = [[start]]

import time
start_time = time.time()
pops = 0
while queue:
    # print(len(paths), len(deque), end='\r')
    path = queue.pop(0)
    pops += 1
    if len(path) >= 6:
        continue
    for transformation in get_transformations(path[-1], letters):
        if transformation in words:
            if transformation in found_words:
                if len(path) > found_words[transformation]:
                    continue
            else:
                found_words[transformation] = len(path)
            
            new_path = path.copy()
            new_path.append(transformation)
            if transformation == end:
                paths.append(new_path)
                continue
            queue.append(new_path)

print("Time elapsed:", time.time() - start_time)
print("Paths:")
print(paths)
print("Pops:", pops)