from src.base import Cache
import threading

class LIFO(Cache):
    """
    Implementation of Last In First Out cache policy
    """
    def __init__(self, capacity: int):
        super().__init__(capacity)
        self.stack = []
        self.lock = threading.Lock()

    def set(self, key, value):
        if self.lock:
            for item in self.stack:
                if item[0] == key:
                    item[1] = value
                    print(f"Key {key} is updated")
                    return
            if len(self.stack) == self.capacity:
                self.stack.pop(-1)
                self.stack.append([key, value])
                print(f"Key: {key} with value {value} is set")
                return
            print(f"Key: {key} with value {value} is set")
            return

    def get(self, key):
        if self.lock:
            for item in self.stack:
                if item[0] == key:
                    print(f"Value associated with key: {key} is {item[0]}")
                    return
            print(f"Key {key} not found")
            return
    
    def delete(self, key):
        if self.lock:
            for item in self.queue:
                if item[0] == key:
                    self.stack.remove(item)
                    return "Item successfully removed"
            return "The given key doesn't exist"
    
    def view(self):
        if self.lock:
            for index in range(len(self.stack) - 1, -1, -1):
                print(f"Key: {self.stack[index][0]}, Value: {self.stack[index][1]}")