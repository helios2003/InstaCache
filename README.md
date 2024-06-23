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

