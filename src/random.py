from src.base import Cache
import threading
import random

class RandomReplacement(Cache):
    """
    Implements random replacement caching strategy
    """
    def __init__(self, capacity: int) -> None:
        super().__init__(capacity)
        self.array = []
        self.lock = threading.Lock()

    def set(self, key, value):
        if self.lock:
            for item in self.array:
                if item[0] == key:
                    item[1] = value
                    print(f"Key {key} is updated")
                    return
            if len(self.array) == self.capacity:
                index = random.randint(0, self.capacity - 1)
                self.array.pop(index)
                self.array.append([key, value])
                print(f"Key: {key} with value {value} is set")
                return
            self.array.append([key, value])
            print(f"Key: {key} with value {value} is set")
            return

    def get(self, key):
        with self.lock:
            for item in self.array:
                if item[0] == key:
                    print(f"Value associated with key: {key} is {item[0]}")
                    return
            print(f"Key {key} not found")
            return
        
    def delete(self, key):
        if self.lock:
            for item in self.array:
                if item[0] == key:
                    self.array.remove(item)
                    return "Item successfully removed"
            return "The given key doesn't exist"

    def view(self):
        with self.lock:
            for item in self.array:
                print(f"Key: {item[0]}, Value: {item[1]}")
