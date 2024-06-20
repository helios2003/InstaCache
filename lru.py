from base import Cache

class Node:
    def __init__(self, val= 0, prev=None, next=None):
        self.val = val
        self.left: Node = prev
        self.right: Node = next

class LRU(Cache):
    def __init__(self, capacity):
        super().__init__(capacity)



    