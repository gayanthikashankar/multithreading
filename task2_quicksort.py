import time
import random
import os
from concurrent.futures import ThreadPoolExecutor

def sequential_quicksort(arr):
    #Regular quicksort implementation
    if len(arr) <= 1:
        return arr
    
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    
    return sequential_quicksort(left) + middle + sequential_quicksort(right)

def threaded_quicksort(arr, max_workers=4):
    #Multithreaded quicksort implementation using ThreadPoolExecutor
    if len(arr) <= 1:
        return arr
    
    if len(arr) <= 1000:
        return sequential_quicksort(arr)
    
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    
    #use ThreadPoolExecutor to manage threads
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        left_future = executor.submit(threaded_quicksort, left, max_workers)
        right_future = executor.submit(threaded_quicksort, right, max_workers)
        
        left_sorted = left_future.result()
        right_sorted = right_future.result()
    
    return left_sorted + middle + right_sorted

def read_array_from_file(filename):
    #read numbers from a file into an array
    with open(filename, 'r') as file:
        return [int(x) for x in file.read().split()]

def main():
    os.makedirs('sample_inputs', exist_ok=True)
    os.makedirs('sample_outputs', exist_ok=True)
    
    input_file = 'sample_inputs/input_quicksort.txt'
    if os.path.exists(input_file):
        arr = read_array_from_file(input_file)
    else:
        size = 20
        arr = [random.randint(1, 100) for _ in range(size)]
        
        with open(input_file, 'w') as file:
            file.write(' '.join(map(str, arr)))
    
    print(f"Running quicksort on {len(arr)} elements...\n")
    print(f"Original array: ")
    print(" ".join(map(str, arr)))
    print()
    
    arr1 = arr.copy()
    arr2 = arr.copy()
    
    #test sequential quicksort
    start_time = time.time()
    sorted_arr1 = sequential_quicksort(arr1)
    seq_time = time.time() - start_time
    
    print(f"Sorted array (Sequential): ")
    print(" ".join(map(str, sorted_arr1)))
    print()
    print(f"Sequential quicksort time: {seq_time:.4f} seconds")
    print()
    
    #test threaded quicksort with ThreadPoolExecutor
    start_time = time.time()
    sorted_arr2 = threaded_quicksort(arr2)
    thread_time = time.time() - start_time
    
    print(f"Sorted array (ThreadPoolExecutor): ")
    print(" ".join(map(str, sorted_arr2)))
    print()
    print(f"ThreadPoolExecutor quicksort time: {thread_time:.4f} seconds")
    print()
    
    print(f"Arrays are equal: {sorted_arr1 == sorted_arr2}")
    print(f"Speedup: {seq_time / thread_time:.2f}x")
    
    output_file = 'sample_outputs/output_quicksort.txt'
    with open(output_file, 'w') as file:
        file.write(f"Running quicksort on {len(arr)} elements...\n\n")
        file.write(f"Original array:\n")
        file.write(" ".join(map(str, arr)))
        file.write("\n\n")
        
        file.write(f"Sorted array (Sequential):\n")
        file.write(" ".join(map(str, sorted_arr1)))
        file.write("\n\n")
        file.write(f"Sequential quicksort time: {seq_time:.4f} seconds\n\n")
        
        file.write(f"Sorted array (ThreadPoolExecutor):\n")
        file.write(" ".join(map(str, sorted_arr2)))
        file.write("\n\n")
        file.write(f"ThreadPoolExecutor quicksort time: {thread_time:.4f} seconds\n\n")
        
        file.write(f"Arrays are equal: {sorted_arr1 == sorted_arr2}\n")
        file.write(f"Speedup: {seq_time / thread_time:.2f}x\n")

if __name__ == "__main__":
    main()