from src.base import Cache
import threading

class LIFO(Cache):
    """
    Implementation of Last In First Out cache policy
    """
    def __init__(self, capacity: int) -> None:
        super().__init__(capacity)
        self.stack = []
        self.lock = threading.Lock()

    def set(self, key: int, value: str) -> str:
        if self.lock:
            for item in self.stack:
                if item[0] == key:
                    item[1] = value
                    return "Value asscoiated with the key updated"
            if len(self.stack) == self.capacity:
                self.stack.pop(-1)
                self.stack.append([key, value])
                return "Key value pair set"
            self.stack.append([key, value])

    def get(self, key: int) -> str:
        if self.lock:
            for item in self.stack:
                if item[0] == key:
                    return item[1]
            return "Not found"
    
    def delete(self, key: int) -> str:
        if self.lock:
            for item in self.queue:
                if item[0] == key:
                    self.stack.remove(item)
                    return "Item successfully removed"
            return "The given key doesn't exist"
    
    def view(self) -> None:
        if self.lock:
            for index in range(len(self.stack) - 1, -1, -1):
                print(f"Key: {self.stack[index][0]}, Value: {self.stack[index][1]}")