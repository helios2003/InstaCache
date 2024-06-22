from src.base import Cache
import threading
import logging

class LIFO(Cache):
    """
    Implementation of First In First Out cache policy
    """
    def __init__(self, capacity):
        super().__init__(capacity)
        self.stack = []
        self.lock = threading.Lock()
        logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)

    def set(self, key, value):
        with self.lock:
            for item in self.stack:
                if item[0] == key:
                    item[1] = value
                    print(f"Key {key} is updated")

            if len(self.stack) >= self.capacity:
                self.stack.pop(-1)
                self.stack.append([key, value])
                print(f"Key: {key} with value {value} is set")
            else:
                self.stack.append([key, value])
                print(f"Key: {key} with value {value} is set")
                return
            
    def get(self, key):
        with self.lock:
            for item in self.stack:
                if item[0] == key:
                    print(f"Value associated with key: {key} is {item[1]}")
                    return item[1]
            print(f"Key {key} not found")
            return None
    
    def delete(self, key):
        with self.lock:
            for item in self.stack:
                if item[0] == key:
                    self.stack.remove(item)
                    print(f"{key} is deleted")
                    return "Item successfully removed"
            print("The given key doesn't exist")
            return "The given key doesn't exist"
    
    def view(self):
        if self.lock:
            for index in range(len(self.stack) - 1, -1, -1):
                self.logger.info(f"Key: {self.stack[index][0]}, Value: {self.stack[index][1]}")
