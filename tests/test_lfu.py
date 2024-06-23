import unittest
import threading
import sys
sys.path.append('..') 
from src.lfu import LFU

class LFUTest(unittest.TestCase):
    def setUp(self):
        self.cache = LFU(capacity=3)

    ############# General Tests #####################
    def test_set_get(self):
        self.cache.set("key1", "value1")
        self.assertEqual(self.cache.get("key1"), "value1")

    def test_update_key(self):
        self.cache.set("key1", "value1")
        self.cache.set("key1", "value2")
        self.assertEqual(self.cache.get("key1"), "value2")

    def test_delete_existing_key(self):
        self.cache.set("key1", "value1")
        self.assertEqual(self.cache.delete("key1"), "Item successfully removed")
        self.assertEqual(self.cache.get("key1"), "The key not found")

    def test_delete_non_existing_key(self):
        self.assertEqual(self.cache.delete("key1"), "The given key doesn't exist")

    def test_view(self):
        self.cache.set("key1", "value1")
        self.cache.set("key2", "value2")
        self.cache.set("key3", "value3")
        self.cache.get("key2")
        with self.assertLogs(level='INFO') as log:
            self.cache.view()
        messages = [
            "Key: key3, Value: value3, Frequency: 1",
            "Key: key1, Value: value1, Frequency: 1",
            "Key: key2, Value: value2, Frequency: 2",
        ]
        for i, message in enumerate(messages):
            self.assertIn(message, log.output[i])

    # ############# LFU Specific Tests #####################
    def test_eviction_least_frequent(self):
        self.cache.set("key1", "value1")
        self.cache.set("key2", "value2")
        self.cache.set("key3", "value3")
        self.cache.get("key2")
        self.cache.set("key4", "value4")  #--> eviction should happen here
        self.assertEqual(self.cache.get("key1"), "The key not found")
        self.assertEqual(self.cache.get("key2"), "value2")
        self.assertEqual(self.cache.get("key3"), "value3")
        self.assertEqual(self.cache.get("key4"), "value4")

    def test_eviction_within_frequency(self):
        self.cache.set("key1", "value1")
        self.cache.set("key2", "value2")
        self.cache.set("key3", "value3")
        self.cache.get("key2")
        self.cache.set("key4", "value4")
        self.assertEqual(self.cache.get("key1"), "The key not found")
        self.assertEqual(self.cache.get("key2"), "value2")
        self.assertEqual(self.cache.get("key3"), "value3")
        self.assertEqual(self.cache.get("key4"), "value4")

    def test_eviction_tie_in_frequency(self):
        self.cache.set("key1", "value1")
        self.cache.set("key2", "value2")
        self.cache.set("key3", "value3")
        self.cache.get("key2")
        self.cache.get("key3")
        self.cache.set("key4", "value4")  
        self.assertEqual(self.cache.get("key1"), "The key not found")
        self.assertEqual(self.cache.get("key2"), "value2")
        self.assertEqual(self.cache.get("key3"), "value3")
        self.assertEqual(self.cache.get("key4"), "value4")

if __name__ == '__main__':
    unittest.main()