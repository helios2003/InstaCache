import unittest
import threading
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

    def test_ttl_expiry(self):
        self.cache.set("key1", "value1")
        time.sleep(3)  #---> for checking the expiry
        self.assertEqual(self.cache.get("key1"), None)
        self.assertEqual(len(self.cache.cache), 0)

if __name__ == '__main__':
    unittest.main()