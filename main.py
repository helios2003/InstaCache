import argparse

def main():
    parser = argparse.ArgumentParser(description='Add the caching strategy')
    parser.add_argument('strategy', metavar='type', type=str, choices=['fifo', 'lifo', 'lru', 'lfu', 'expiry', 'random'], help='Select the cache type')
    parser.add_argument('capacity', metavar='cap', type=int, help='Add the cache capacity')
    args = parser.parse_args()
    
    if args.strategy == 'fifo':
        from src.fifo import FIFO
        cache = FIFO(args.capacity)

    elif args.strategy == 'lifo':
        from src.lifo import LIFO
        cache = LIFO(args.capacity)

    elif args.strategy == 'lru':
        from src.lru import LRU
        cache = LRU(args.capacity)

    elif args.strategy == 'lfu':
        from src.lfu import LFU
        cache = LFU(args.capacity)

    elif args.strategy == 'expiry':
        from src.expiry import Expiry
        ttl = int(input("Please enter the time to live for the the cache: "))
        cache = Expiry(args.capacity, ttl)

    elif args.strategy == 'random':
        from src.random import RandomReplacement
        cache = RandomReplacement(args.capacity)

    else:
        print("Please provide a valid input")
        exit(1)

    while True:
        print("\n1. Set key-value\n2. Get value by key\n3. Delete key\n4. View cache\n5. Exit")
        choice = int(input("Enter your choice: "))
        if choice == 1:
            key = input("Enter key: ")
            value = input("Enter value: ")
            cache.set(key, value)
        elif choice == 2:
            key = input("Enter key: ")
            cache.get(key)
        elif choice == 3:
            key = input("Enter key: ")
            cache.delete(key)
        elif choice == 4:
            cache.view()
        elif choice == 5:
            print("Exiting.....")
            break
        else:
            print("Please provide a valid option")

if __name__ == '__main__':
    main()