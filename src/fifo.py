from src.base import Cache
import threading
import logging

class FIFO(Cache):
    """
    Implementation of First In First Out cache policy
    """
    def __init__(self, capacity):
        super().__init__(capacity)
        self.queue = []
        self.lock = threading.Lock()
        logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)

    def set(self, key, value):
        with self.lock:
            for item in self.queue:
                if item[0] == key:
                    item[1] = value
                    print(f"Key {key} is updated")

            if len(self.queue) >= self.capacity:
                self.queue.pop(0)
                self.queue.append([key, value])
                print(f"Key: {key} with value {value} is set")
            else:
                self.queue.append([key, value])
                print(f"Key: {key} with value {value} is set")
                return
            
    def get(self, key):
        with self.lock:
            for item in self.queue:
                if item[0] == key:
                    print(f"Value associated with key: {key} is {item[1]}")
                    return item[1]
            print(f"Key {key} not found")
            return None
    
    def delete(self, key):
        with self.lock:
            for item in self.queue:
                if item[0] == key:
                    self.queue.remove(item)
                    print(f"{key} is deleted")
                    return "Item successfully removed"
            print("The given key doesn't exist")
            return "The given key doesn't exist"
    
    def view(self):
        with self.lock:
            for item in self.queue:
                self.logger.info(f"Key: {item[0]}, Value: {item[1]}")

        
