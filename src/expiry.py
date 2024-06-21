from src.base import Cache
import threading
import heapq
import time

class Expiry(Cache):
    """
    Implementation of the caching policy where the key: value pair expires after a specified time period
    """
    def __init__(self, capacity, ttl):
        super().__init__(capacity)
        self.ttl = ttl
        self.heap = []     # [expiry_time, key]  --> maxheap
        self.cache = {}    # {key: [value, expiry_time]}
        self.lock = threading.Lock()

   # helper function for removal of the item from the heap
    def _remove_from_heap(self, key):
        for index in range(len(self.heap)):
            if self.heap[index][1] == key:
                self.heap[index] = self.heap[-1]
                self.heap.pop()
                heapq.heapify(self.heap)
                break

    # helper function for evicting the item from the cache after the expiry
    def _evict(self):
        while self.heap:
            curr_time = time.time()
            if self.heap[0][0] <= curr_time:
                _, key = heapq.heappop(self.heap)
                if key in self.cache and self.cache[key][1] <= curr_time:
                    del self.cache[key]

    def set(self, key, value):
        with self.lock:
            self._evict()
            if key in self.cache.keys():
                self._remove_from_heap(key)

            elif len(self.cache) >= self.capacity:
                self._evict()
                if len(self.cache) >= self.capacity:
                    _, oldest_key = heapq.heappop(self.heap)
                    if oldest_key in self.cache.keys():
                        del self.cache[oldest_key]
            expiry_time = time.time() + self.ttl
            self.cache[key] = [value, expiry_time]
            self.heap.append([expiry_time, value])
            heapq.heapify(self.heap)
            print(f"Key: {key} with value {value} is set")
            return

    def get(self, key):
        with self.lock:
            self._evict()
            if key in self.cache:
                return self.cache[key][0]
            print("The {key} doesn't exist in the cache")
            return
        
    def delete(self, key):
        with self.lock:
            self._evict()
            if key in self.cache:
                del self.cache[key]
                self._remove_from_heap(key)
                print(f"{key} is deleted")
                return
        print(f"{key} does not exist in the cache")
        return
        
    def view(self):
        with self.lock:
            self._evict()
            for key, (value, expiry_time) in self.cache.items():
                print(f"Key: {key}, Value: {value}, Expires at: {time.ctime(expiry_time)}")
        

    

