import unittest
from threading import Thread
import random
import logging
import sys
sys.path.append('..')
from src.expiry import Expiry
import time

class ExpiryTest(unittest.TestCase):
    def setUp(self):
        self.cache = Expiry(capacity=3, ttl=1)

    ############# General Tests #####################
    def test_set_get(self):
        self.cache.set("key1", ["value1", time.time() + 1])
        val, _ = self.cache.get("key1")
        self.assertEqual("value1", val)

    def test_update_key(self):
        self.cache.set("key1", ["value1", time.time() + 1])
        self.cache.set("key1", ["value2", time.time() + 1])
        val, _ = self.cache.get("key1")
        self.assertEqual(val, 'value2')

    def test_delete_existing_key(self):
        self.cache.set("key1",["value1", time.time() + 1])
        self.assertEqual(self.cache.delete("key1"), "Item successfully removed")
        self.assertEqual(self.cache.get("key1"), None)

    def test_delete_non_existing_key(self):
        self.assertEqual(self.cache.delete("key1"), "The given key doesn't exist")

    def test_eviction_when_full(self):
        self.cache.set("key1", ["value1", time.time() + 1])
        self.cache.set("key2", ["value2", time.time() + 1])
        self.cache.set("key3", ["value3", time.time() + 1])
        self.cache.set("key4", ["value4", time.time() + 1])  # ---> eviction should happen here
        self.assertEqual(len(self.cache.cache), 3)

    def test_view(self):
        self.cache.set("key1", ["value1", time.time() + 1])
        self.cache.set("key2", ["value2", time.time() + 1])
        self.cache.set("key3", ["value3", time.time() + 1])
        with self.assertLogs(level='INFO') as log:
            self.cache.view()
        index = 0
        for key, (value, t) in self.cache.cache.items():
            self.assertIn(f"Key: {key}, Value: {value}, Expires at: {time.ctime(t)}", log.output[index])
            index += 1

    ###### TTL Test #####################

    def test_ttl_expiry(self):
        self.cache.set("key1", "value1")
        time.sleep(1)  #---> for checking the expiry
        self.assertEqual(self.cache.get("key1"), None)
        self.assertEqual(len(self.cache.cache), 0)


    ############# Concurrency Tests #####################

    def test_concurrency(self):
        num_threads = 10
        ops_per_thread = 100
        
        def worker(self):
            for _ in range(ops_per_thread):
                operation = random.choice(['set', 'get', 'delete'])
                key = f"key{random.randint(1, 20)}"
                value = f"value{random.randint(1, 100)}"

                if operation == 'set':
                    self.cache.set(key, [value, time.time() + 1])
                    retrieved_value = self.cache.get(key)
                    self.assertEqual(retrieved_value[0], value)
                elif operation == 'get':
                    try:
                        retrieved_value = self.cache.get(key)
                        self.assertIsNotNone(retrieved_value)
                    except Exception as e:
                        logging.error(f"Error getting key {key}: {e}")
                else: 
                    self.cache.delete(key)
                    retrieved_value = self.cache.get(key)
                    self.assertIsNone(retrieved_value)

        threads = []
        for _ in range(num_threads):
            t = Thread(target=worker, args=(self,))
            threads.append(t)
            t.start()
            
        for t in threads:
            t.join()
        self.assertLessEqual(len(self.cache.cache), self.cache.capacity)

if __name__ == '__main__':
    unittest.main()