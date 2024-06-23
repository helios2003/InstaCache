# InstaCache

## Introduction
This project aims to implement a thread safe in memory cache with an option to choose the algorithm one wishes to implement for cache insertion and cache eviction policy.

There are few standard algorithms that have been implemented and few that are use case specific.

### Standard Cache Eviction Policies
- FIFO (First In First Out)
- LIFO (Last In First Out)
- LFU (Least Frequently Used)
- LRU (Least Recently Used)

### Custom Cache Eviction Policies
- TTL (Time to Live)
- RR (Random Replacement Strategy)

## Getting started
- Create a fork or clone the repository directly using the command:
```
git clone https://github.com/helios2003/InstaCache.git
```
- Change directory to `InstaCache`.
- To use the program write
```
python main.py <caching-strategy> <capacity>

<caching-strategy>: fifo, lifo, lru, lfu, expiry, random
<capcity>: An integer
```
- After that a menu driven program appears from which the necessary operation can be selected.

## Testing
- Few tests have also been written for each strategy in the `tests/` directory which can be run using:
```
python -m unittest discover -s tests
```

## Requirements:
- Python 3.xx

## Brief Explanation of the Policies Implemented
- **FIFO** : First In First Out. In this policy the first element that is inserted into the cache is the first element that is removed from the cache.
- **LIFO** : Last In First Out. In this policy the last element that is inserted into the cache is the first element that is removed from the cache.
- **LRU** : Least Recently Used. In this policy the element that was used the least recently is the first element that is removed from the cache
- **LFU** : Least Frequently Used. In this policy the element that is used the least number of times is the first element that is removed from the cache. If there is a tie, the value that was least recently used is removed.
- **TTL** : Time to Live. In this policy there is an expiration time for each element in the cache. The element is removed from the cache after the expiration time period.
- **RR** : Random Replacement Strategy. In this policy while removal a random element is removed from the cache.
