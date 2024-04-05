
# The Self-Balancing Binary Search Tree (TSBBST)
# - balanced add
# - balanced delete
# - find

# Add benchmark
# - n vs time
# - n vs depth, plot perfect tree n as a line (1, 3, 7, 15, 31)

# Delete Balance benchmark
# - Add a mbillion-ish nodes
# - Delete all of them one by one at random
# - Plot remaining size vs depth

# https://en.wikipedia.org/wiki/Tree_rotation

class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.height = 1
    def rotate_right(self):
        if self.left:
            x = self.left.value
            y = self.value
            A = self.left.left
            B = self.left.right
            C = self.right

            self.value = x
            self.right = Node(y)
            self.left = A
            self.right.left = B
            self.right.right = C
            self.right.update_height()
            self.update_height()
        else: raise Exception("invalid rotation")
    def rotate_left(self):
        if self.right:
            x = self.right.value
            y = self.value
            A = self.right.right
            B = self.right.left
            C = self.left
            
            self.value = x
            self.left = Node(y)
            self.right = A
            self.left.right = B
            self.left.left = C
            self.left.update_height()
            self.update_height()
        else: raise Exception("invalid rotation")
    def update_height(self):
        self.height = 0
        left_height = self.left.height if self.left else 0
        right_height = self.right.height if self.right else 0
        self.height = 1 + max(left_height, right_height)
    def balance_factor(self):
        return (self.left.height if self.left else 0) - (self.right.height if self.right else 0)
    def balance_tree(self):
        if self.balance_factor() > 1:
            if self.left.balance_factor() < 0:
                self.left.rotate_left()
            self.rotate_right()
        elif self.balance_factor() < -1:
            if self.right.balance_factor() > 0:
                self.right.rotate_right()
            self.rotate_left()
    def add(self, value):
        if value < self.value:
            if self.left: self.left.add(value)
            else: self.left = Node(value)
            if 1+self.left.height > self.height:
                self.height = 1+self.left.height
        elif value > self.value:
            if self.right: self.right.add(value)
            else: self.right = Node(value)
            if 1+self.right.height > self.height:
                self.height = 1+self.right.height
        self.balance_tree()
    def minValueNode(self, node):
        current = node
        while current.left is not None:
            current = current.left
        return current
    def delete(self, next, key):
        if next is None:
            return next

        if key < next.value:
            next.left = self.delete(next.left, key)
        elif key > next.value:
            next.right = self.delete(next.right, key)
        else:
            if next.left is None:
                temp = next.right
                next = None
                return temp
            elif next.right is None:
                temp = next.left
                next = None
                return temp

            temp = self.minValueNode(next.right)
            next.value = temp.value
            next.right = self.delete(next.right, temp.value)
        next.balance_tree()
        return next
    def inorder(self):
         return f"{self.left.inorder() if self.left is not None else ''}{self.value},{self.right.inorder() if self.right is not None else ''}"
    def contains(self, value):
        if self.value == value: return True
        if value < self.value and self.left: return self.left.contains(value)
        if value > self.value and self.right: return self.right.contains(value)
        return False
    def print_tree(self, current_node, nameattr='value', left_child='left', right_child='right', indent='', last='updown'):
        tree_str = ''
        
        if hasattr(current_node, nameattr):
            name = lambda node: getattr(node, nameattr)
        else:
            name = lambda node: str(node)

        up = getattr(current_node, left_child)
        down = getattr(current_node, right_child)

        if up is not None:
            next_last = 'up'
            next_indent = '{0}{1}{2}'.format(indent, ' ' if 'up' in last else '|', ' ' * len(str(name(current_node))))
            tree_str += self.print_tree(up, nameattr, left_child, right_child, next_indent, next_last)

        if last == 'up': start_shape = '┌'
        elif last == 'down': start_shape = '└'
        elif last == 'updown': start_shape = ' '
        else: start_shape = '├'

        if up is not None and down is not None: end_shape = '┤'
        elif up: end_shape = '┘'
        elif down: end_shape = '┐'
        else: end_shape = ''

        tree_str += '{0}{1}{2}{3}\n'.format(indent, start_shape, name(current_node), end_shape)

        if down is not None:
            next_last = 'down'
            next_indent = '{0}{1}{2}'.format(indent, ' ' if 'down' in last else '|', ' ' * len(str(name(current_node))))
            tree_str += self.print_tree(down, nameattr, left_child, right_child, next_indent, next_last)
        
        return tree_str
    def __str__(self):
        return self.print_tree(self)

class BST:
    def __init__(self):
        self.root = None
        self.count = 0
        self.min = 0
        self.max = 0
    def add(self, value):
        if self.root:
            self.root.add(value)
        else:
            self.root = Node(value)
            self.count += 1
            self.min = value
            self.max = value
    def delete(self, key):
        self.root = self.root.delete(self.root, key)
    def contains(self, value):
        if self.root:
            return self.root.contains(value)
    def height(self):
        return self.root.height
    def __str__(self):
        return str(self.root)
    def inorder(self):
        return f"[{self.root.inorder()[:-1]}]"
    
tree = BST()
for i in range(1,33):
    tree.add(i)
print(tree)
tree.delete(24)
print(tree)
# tree.add(50)
# tree.add(17)
# tree.add(76)
# tree.add(97)
# tree.add(107)
# tree.add(66)
# tree.add(67)
# tree.add(108)
# tree.add(96)
# tree.add(98)
# print(tree)

# tree.delete(107)
# print(tree)