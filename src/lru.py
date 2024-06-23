from src.base import Cache
import threading
import logging

class Node:
    """
    Implementation of Least Recently Used Cache policy
    """
    def __init__(self, key=0, val=0, prev=None, next=None):
        self.key = key
        self.val = val
        self.prev = prev
        self.next = next

class LRU(Cache):
    def __init__(self, capacity):
        super().__init__(capacity)
        self.dict = {}
        self.start = Node(-1, -1)
        self.end = Node(-1, -1)
        self.start.next = self.end
        self.end.prev = self.start
        self.lock = threading.Lock()
        logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)

    # helper function associated with the linked list class
    def _add(self, node):
        temp = self.start.next
        node.next = temp
        self.start.next = node
        node.prev = self.start
        temp.prev = node

    # helper function associated with the linked list class
    def _remove(self, node):
        prev_node = node.prev
        next_node = node.next
        prev_node.next = next_node
        next_node.prev = prev_node

    def set(self, key, val):
        with self.lock:
            if key in self.dict:
                node = self.dict[key]
                node.val = val
                self._remove(node)
                self._add(node)
            else:
                if len(self.dict) == self.capacity:
                    lru_node = self.end.prev
                    self._remove(lru_node)
                    del self.dict[lru_node.key]
                new_node = Node(key, val)
                self._add(new_node)
                self.dict[key] = new_node

    def get(self, key):
        with self.lock:
            if key in self.dict:
                node = self.dict[key]
                self._remove(node)
                self._add(node)
                return node.val
            return "Not found"

    def delete(self, key):
        with self.lock:
            if key in self.dict:
                node = self.dict[key]
                self._remove(node)
                del self.dict[key]
                return "Item successfully removed"
            return "The given key doesn't exist"

    def view(self):
        with self.lock:
            current = self.start.next
            while current != self.end:
                self.logger.info(f"Key: {current.key}, Value: {current.val}")
                current = current.next