from src.base import Cache
import threading
import logging

class Node:
    """
    Implementation of a doubly linked list node for LFU Cache
    """
    def __init__(self, key=0, val=0, freq=1, prev=None, next=None):
        self.key = key
        self.val = val
        self.freq = freq
        self.prev = prev
        self.next = next

class DoublyLinkedList:
    """
    Doubly linked list to manage nodes for LFU cache
    """
    def __init__(self):
        self.head = Node()
        self.tail = Node()
        self.head.next = self.tail
        self.tail.prev = self.head

    def add_node(self, node):
        temp = self.head.next
        node.next = temp
        node.prev = self.head
        self.head.next = node
        temp.prev = node

    def remove_node(self, node):
        prev_node = node.prev
        next_node = node.next
        prev_node.next = next_node
        next_node.prev = prev_node

    def pop_tail(self):
        if self.tail.prev == self.head:
            return None
        node = self.tail.prev
        self.remove_node(node)
        return node

class LFU(Cache):
    """
    Implementation of Least Frequently Used cache policy
    """
    def __init__(self, capacity):
        super().__init__(capacity)
        self.capacity = capacity
        self.size = 0
        self.min_freq = 0
        self.dict = {}  # key to node
        self.freq_dict = {}  # freq to doubly linked list
        self.lock = threading.Lock()
        logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)

    def _update_node_freq(self, node):
        freq = node.freq
        self.freq_dict[freq].remove_node(node)
        
        if not self.freq_dict[freq].head.next.next:
            del self.freq_dict[freq]
            if self.min_freq == freq:
                self.min_freq += 1
        
        node.freq += 1
        freq = node.freq
        if freq not in self.freq_dict:
            self.freq_dict[freq] = DoublyLinkedList()
        self.freq_dict[freq].add_node(node)

    def set(self, key, val):
        with self.lock:
            if self.capacity == 0:
                return
            
            if key in self.dict:
                node = self.dict[key]
                node.val = val
                self._update_node_freq(node)
            else:
                if self.size == self.capacity:
                    min_freq_list = self.freq_dict[self.min_freq]
                    lfu_node = min_freq_list.pop_tail()
                    if lfu_node:
                        del self.dict[lfu_node.key]
                        self.size -= 1
                
                new_node = Node(key, val)
                self.dict[key] = new_node
                if 1 not in self.freq_dict:
                    self.freq_dict[1] = DoublyLinkedList()
                self.freq_dict[1].add_node(new_node)
                self.min_freq = 1
                self.size += 1

    def get(self, key):
        with self.lock:
            if key in self.dict:
                node = self.dict[key]
                self._update_node_freq(node)
                return node.val
            return "The key not found"

    def delete(self, key):
        with self.lock:
            if key in self.dict:
                node = self.dict[key]
                self.freq_dict[node.freq].remove_node(node)
                if not self.freq_dict[node.freq].head.next.next:
                    del self.freq_dict[node.freq]
                del self.dict[key]
                self.size -= 1
                return "Item successfully removed"
            return "The given key doesn't exist"

    def view(self):
        with self.lock:
            for freq in sorted(self.freq_dict.keys()):
                current = self.freq_dict[freq].head.next
                while current != self.freq_dict[freq].tail:
                    self.logger.info(f"Key: {current.key}, Value: {current.val}, Frequency: {current.freq}")
                    current = current.next
