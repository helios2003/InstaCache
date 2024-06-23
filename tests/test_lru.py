import unittest
from threading import Thread
import random
import logging
import sys
sys.path.append('..')
from src.lru import LRU

class LRUTest(unittest.TestCase):
    def setUp(self):
        self.dict = LRU(capacity=3)

    ############# General Tests #####################
    def test_set_get(self):
        self.dict.set("key1", "value1")
        self.assertEqual(self.dict.get("key1"), "value1")

    def test_update_key(self):
        self.dict.set("key1", "value1")
        self.dict.set("key1", "value2")
        self.assertEqual(self.dict.get("key1"), "value2")

    def test_delete_existing_key(self):
        self.dict.set("key1", "value1")
        self.assertEqual(self.dict.delete("key1"), "Item successfully removed")
        self.assertEqual(self.dict.get("key1"), None)

    def test_delete_non_existing_key(self):
        self.assertEqual(self.dict.delete("key1"), None)

    def test_eviction_when_full(self):
        self.dict.set("key1", "value1")
        self.dict.set("key2", "value2")
        self.dict.set("key3", "value3")
        self.dict.set("key4", "value4")  # ---> eviction should happen here
        self.assertEqual(len(self.dict.dict), 3)

    def test_view(self):
        self.dict.set("key1", "value1")
        self.dict.set("key2", "value2")
        self.dict.set("key3", "value3")
        with self.assertLogs(level='INFO') as log:
            self.dict.view()
        self.assertIn("Key: key3, Value: value3", log.output[0])
        self.assertIn("Key: key2, Value: value2", log.output[1])
        self.assertIn("Key: key1, Value: value1", log.output[2])

    ########### Concurrency Test ####################

    def test_concurrency(self):
        num_threads = 10
        ops_per_thread = 100
        
        def worker(self):
            for _ in range(ops_per_thread):
                operation = random.choice(['set', 'get', 'delete'])
                key = f"key{random.randint(1, 20)}"
                value = f"value{random.randint(1, 100)}"

                if operation == 'set':
                    self.dict.set(key, value)
                    retrieved_value = self.dict.get(key)
                    self.assertEqual(retrieved_value, value)
                elif operation == 'get':
                    try:
                        retrieved_value = self.dict.get(key)
                        self.assertIsNotNone(retrieved_value)
                    except Exception as e:
                        logging.error(f"Error getting key {key}: {e}")
                else: 
                    self.dict.delete(key)
                    retrieved_value = self.dict.get(key)
                    self.assertIsNone(retrieved_value)

        threads = []
        for _ in range(num_threads):
            t = Thread(target=worker, args=(self,))
            threads.append(t)
            t.start()
            
        for t in threads:
            t.join()
        self.assertLessEqual(len(self.dict.dict), self.dict.capacity)


if __name__ == '__main__':
    unittest.main()
