class BinHeap:
    def __init__(self, array_length=1000):
        self.heap_size = 0
        self.length = array_length
        self.A = [0] * (array_length + 1)

    def parent(self, i):
        return i // 2

    def left(self, i):
        return 2 * i

    def right(self, i):
        return 2 * i + 1

    def is_empty(self):
        return self.heap_size == 0

    def min_heapify(self, i):
        l = self.left(i)
        r = self.right(i)
        # You write the rest of this - remember this is a _min_ heap
        if l <= self.heap_size and self.A[l] < self.A[i]:
            smallest = l
        else:
            smallest = i 
        if r <= self.heap_size and self.A[r] < self.A[smallest]:
            smallest = r 
        if i != smallest:
            self.swap(smallest, i)
            self.min_heapify(smallest) 

    def build_min_heap(self, n):
        #You implement this (needed for HeapSort)
        self.heap_size = n
        for i in range(n/2, 0, -1):
            self.min_heapify(i)

    def insert(self, key):
        self.heap_size += 1
        self.A[self.heap_size] = key
        self.decrease_key(self.heap_size, key)

    def minimum(self):
        return self.A[1] #Assuems heap is not Empty!

    def extract_min(self):
        if self.heap_size < 1:
            print("\nHeap underflow in extractMin()\n\n")
            return 0
        min_val = self.A[1]
        #You write the rest of this - remember this is a _min_ heap
        self.A[1] = self.A[self.heap_size]
        self.heap_size -= 1
        self.min_heapify(1)
        return min_val

    def decrease_key(self, i, key):
        if key > self.A[i]:
            print("\nKey larger than A[i] in decreaseKey()\n\n")
            return
        # You write the rest of this - remember this is a _min_ heap
        self.A[i] = key 
        while i > 0 and self.A[i] < self.A[self.parent(i)]:
            self.swap(i, self.parent(i))
            i = self.parent(i)
    # Auxiliary operations

    def swap(self, i, j):
        temp = self.A[i]
        self.A[i] = self.A[j]
        self.A[j] = temp

    def show_heap(self, i, depth):
        if i <= self.heap_size:
            self.show_heap(self.right(i), depth + 1)
            print(" " * (depth * 6 + 4), self.A[i])
            self.show_heap(self.left(i), depth + 1)

    def print_heap(self):
        print("Heap elements in the array:")
        for i in range(1, self.heap_size + 1):
            print(self.A[i], end=" ")
        print()

    def search(self, key):
        for i in range(1, self.heap_size + 1):
            if self.A[i] == key:
                return i
        return 0

    def min_heap_sort(self, n):
        # You implement this
        self.build_min_heap(n)
        for i in range(n, 2, -1):
            self.swap(self.A[1], self.A[i])
            self.heap_size -= 1
            self.min_heapify(1)
        
        for j in range(0, n/2):
            self.swap(j, n-j)
