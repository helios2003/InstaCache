import argparse

def main():
    parser = argparse.ArgumentParser(description='Add the caching strategy')
    parser.add_argument('strategy', metavar='type', type=str, choices=['fifo', 'lifo', 'lru', 'lfu'], help='Select the cache type')
    parser.add_argument('capacity', metavar='c', type=int, help='Add the cache capacity')
    args = parser.parse_args()
    
    if args.strategy == 'fifo':
        from fifo import FIFO
        cache = FIFO(args.capacity)

    elif args.strategy == 'lifo':
        from lifo import LIFO
        cache = LIFO(args.capacity)

    elif args.strategy == 'lru':
        from lru import LRU
        cache = LRU(args.capacity)

    elif args.strategy == 'lfu':
        from lfu import LFU
        cache = LFU(args.capacity)

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

main()
