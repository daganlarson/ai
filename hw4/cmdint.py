from binheap import BinHeap
import random
def main():
    comment = ""
    choice = ""
    key = 0
    H = BinHeap()  # This actually constructs the heap
    n = 0
    interact = True
    print_extract = True
    try:
        while True:
            if interact:
                print("Commands:")
                print(" (i)nsert, (m)inimum, (e)xtract min,")
                print(" (d)ecrease key, (p)rint heap, print as (t)ree, (s)earch,")
                print(" (S)orting test")
                print("+/- turns extract print on/off, or # (to comment)")
                print(" > ", end="")

            inputs = input().split()
            if len(inputs) == 0:
                continue
            choice = inputs[0]

            if choice == 'i':
                if interact:
                    print("Enter key value to insert: ", end="")
                key = int(inputs[1])
                H.insert(key)
            elif choice == 'm':
                key = H.minimum()
                print(f"Minimum = {key}")
            elif choice == 'e':
                if H.is_empty():
                    print("Heap empty, can't extract minimum.\n")
                else:
                    key = H.extract_min()
                    if print_extract:
                        print(f"Minimum extracted = {key}")
            elif choice == 'd':
                if interact:
                    print("Enter index & new key to decrease: ", end="")
                print(inputs[1:3])
                i, key = map(int, inputs[1:3])
                H.decrease_key(i, key)
            elif choice == 't':
                print("Heap as a logical tree (rotated 90 degrees to left):\n")
                H.show_heap(1, 0)
                print("\n")
            elif choice == 'p':
                H.print_heap()
            elif choice == '+':
                print_extract = True
            elif choice == '-':
                print_extract = False
            elif choice == '#':
                print(' '.join(inputs), end="\n\n")
            elif choice == 's':
                if interact:
                    print("Enter key value to search for: ", end="")
                key = int(inputs[1])
                i = H.search(key)
                print(f"key, {key}, found at index {i}")
            elif choice == 'S':
                if interact:
                    print("Enter length for sorting test: ", end="")
                n = int(inputs[1])
                if n > H.length or n < 0:
                    print("Warning: bad length, using entire array")
                    n = H.length
                print("Original array:")
                for i in range(1, n + 1):
                    H.A[i] = random.randint(0, n - 1)
                    print(H.A[i], end=" ")
                print()
                H.min_heap_sort(n)
                print("Sorted array:")
                for i in range(1, n + 1):
                    print(H.A[i], end=" ")
                print()
                H.heap_size = 0  # destroys heap
            else:
                print(f"Illegal choice: {choice}")
    except EOFError:
        print("\nReached end of input. Exiting...")
if __name__ == "__main__":
    main()
