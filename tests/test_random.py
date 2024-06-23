import unittest
import threading
import sys
sys.path.append('..')
from src.random import RandomReplacement

class RandomReplacementTest(unittest.TestCase):
    def setUp(self):
        self.array = RandomReplacement(capacity=3)

    ############# General Tests #####################
    def test_set_get(self):
        self.array.set("key1", "value1")
        self.assertEqual(self.array.get("key1"), "value1")

    def test_update_key(self):
        self.array.set("key1", "value1")
        self.array.set("key1", "value2")
        self.assertEqual(self.array.get("key1"), "value2")

    def test_delete_existing_key(self):
        self.array.set("key1", "value1")
        self.assertEqual(self.array.delete("key1"), "Item successfully removed")
        self.assertEqual(self.array.get("key1"), None)

    def test_delete_non_existing_key(self):
        self.assertEqual(self.array.delete("key1"), "The given key doesn't exist")

    def test_eviction_when_full(self):
        self.array.set("key1", "value1")
        self.array.set("key2", "value2")
        self.array.set("key3", "value3")
        self.array.set("key4", "value4")  # ---> eviction should happen here
        self.assertEqual(len(self.array.array), 3)

    def test_view(self):
        self.array.set("key1", "value1")
        self.array.set("key2", "value2")
        self.array.set("key3", "value3")
        with self.assertLogs(level='INFO') as log:
            self.array.view()
        self.assertIn("Key: key1, Value: value1", log.output[0])
        self.assertIn("Key: key2, Value: value2", log.output[1])
        self.assertIn("Key: key3, Value: value3", log.output[2])

if __name__ == '__main__':
    unittest.main()
