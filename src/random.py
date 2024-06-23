from src.base import Cache
import threading
import random
import logging

class RandomReplacement(Cache):
    """
    Implements random replacement caching strategy
    """
    def __init__(self, capacity: int) -> None:
        super().__init__(capacity)
        self.array = []
        self.lock = threading.Lock()
        logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)

    def set(self, key, value):
        if self.lock:
            for item in self.array:
                if item[0] == key:
                    item[1] = value
                    self.logger.info(f"Key {key} is updated")
                    return
            if len(self.array) == self.capacity:
                index = random.randint(0, self.capacity - 1)
                self.array.pop(index)
                self.array.append([key, value])
                self.logger.info(f"Key: {key} with value {value} is set")
                return
            self.array.append([key, value])
            self.logger.info(f"Key: {key} with value {value} is set")
            return 

    def get(self, key):
        with self.lock:
            for item in self.array:
                if item[0] == key:
                    self.logger.info(f"Value associated with key: {key} is {item[1]}")
                    return item[1]
            self.logger.info(f"Key {key} not found")
            return None
        
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
                self.logger.info(f"Key: {item[0]}, Value: {item[1]}")
