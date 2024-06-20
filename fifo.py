from base import Cache

class FIFO(Cache):
    """
    Implementation of First In First Out cache policy
    """
    def __init__(self, capacity: int) -> None:
        super().__init__(capacity)
        self.queue = []

    def set(self, key: int, value: int) -> str:
        for item in self.queue:
            if item[0] == key:
                item[1] = value
                return "Key updated"
        if len(self.queue) == self.capacity:
            self.queue.pop(0)
            self.queue.append([key, value])
            return "Key value pair set"
        self.queue.append([key, value])
        
    
    def get(self, key: int) -> str:
        for item in self.queue:
            if item[0] == key:
                return item[1]
        return "Not found"
    
    def delete(self, key: int) -> str:
        for item in self.queue:
            if item[0] == key:
                self.queue.remove(item)
                return "Item successfully removed"
        return "The given key doesn't exist"
    
    def view(self) -> None:
        for item in self.queue:
            print(f"Key: {item[0]}, Value: {item[1]}")

    

        
