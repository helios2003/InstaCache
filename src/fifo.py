from src.base import Cache
import threading

class FIFO(Cache):
    """
    Implementation of First In First Out cache policy
    """
    def __init__(self, capacity):
        super().__init__(capacity)
        self.queue = []
        self.lock = threading.Lock()

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
            self.queue.append([key, value])
            print(f"Key: {key} with value {value} is set")
            return
            
    
    def get(self, key):
        with self.lock:
            for item in self.queue:
                if item[0] == key:
                    print(f"Value associated with key: {key} is {item[0]}")
                    return
            print(f"Key {key} not found")
            return
    
    def delete(self, key):
        with self.lock:
            for item in self.queue:
                if item[0] == key:
                    self.queue.remove(item)
                    print(f"{key} is deleted")
                    return
            print("The given key doesn't exist")
            return
    
    def view(self):
        with self.lock:
            for item in self.queue:
                print(f"Key: {item[0]}, Value: {item[1]}")

    

        
