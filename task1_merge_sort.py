import time
import random
import os
from concurrent.futures import ThreadPoolExecutor

def merge(left, right):
    #Merge two sorted arrays
    result = []
    i = j = 0
    
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    
    result.extend(left[i:])
    result.extend(right[j:])
    return result

def sequential_merge_sort(arr):
    #Regular merge sort implementation
    if len(arr) <= 1:
        return arr
    
    mid = len(arr) // 2
    left = sequential_merge_sort(arr[:mid])
    right = sequential_merge_sort(arr[mid:])
    
    return merge(left, right)

def threaded_merge_sort(arr, max_workers=4):
    #multithreaded merge sort implementation using ThreadPoolExecutor
    if len(arr) <= 1:
        return arr
    
    #sequential sort
    if len(arr) <= 1000:
        return sequential_merge_sort(arr)
    
    #split the array
    mid = len(arr) // 2
    left_half = arr[:mid]
    right_half = arr[mid:]
    
    #use ThreadPoolExecutor to manage threads
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        #sorting both halves
        left_future = executor.submit(threaded_merge_sort, left_half, max_workers)
        right_future = executor.submit(threaded_merge_sort, right_half, max_workers)
        
        left_sorted = left_future.result()
        right_sorted = right_future.result()
    
    #merge the sorted halves
    return merge(left_sorted, right_sorted)

def read_array_from_file(filename):
    #Read numbers from a file into an array
    with open(filename, 'r') as file:
        return [int(x) for x in file.read().split()]

def main():
    #directproes exist
    os.makedirs('sample_inputs', exist_ok=True)
    os.makedirs('sample_outputs', exist_ok=True)
    
    #input file exists
    input_file = 'sample_inputs/input_merge_sort.txt'
    if os.path.exists(input_file):
        arr = read_array_from_file(input_file)
    else:
        #random array
        size = 20
        arr = [random.randint(1, 100) for _ in range(size)]
        
        #save to input file
        with open(input_file, 'w') as file:
            file.write(' '.join(map(str, arr)))
    
    print(f"Running merge sort on {len(arr)} elements...\n")
    print(f"Original array: ")
    print(" ".join(map(str, arr)))
    print()
    
    #copy the array for both sorting methods
    arr1 = arr.copy()
    arr2 = arr.copy()
    
    #test sequential merge sort
    start_time = time.time()
    sorted_arr1 = sequential_merge_sort(arr1)
    seq_time = time.time() - start_time
    
    print(f"Sorted array (Sequential): ")
    print(" ".join(map(str, sorted_arr1)))
    print()
    print(f"Sequential merge sort time: {seq_time:.4f} seconds")
    print()
    
    #test threaded merge sort with ThreadPoolExecutor
    start_time = time.time()
    sorted_arr2 = threaded_merge_sort(arr2)
    thread_time = time.time() - start_time
    
    print(f"Sorted array (ThreadPoolExecutor): ")
    print(" ".join(map(str, sorted_arr2)))
    print()
    print(f"ThreadPoolExecutor merge sort time: {thread_time:.4f} seconds")
    print()
    
    #verify results
    print(f"Arrays are equal: {sorted_arr1 == sorted_arr2}")
    print(f"Speedup: {seq_time / thread_time:.2f}x")
    
    #write output to file
    output_file = 'sample_outputs/output_merge_sort.txt'
    with open(output_file, 'w') as file:
        file.write(f"Running merge sort on {len(arr)} elements...\n\n")
        file.write(f"Original array:\n")
        file.write(" ".join(map(str, arr)))
        file.write("\n\n")
        
        file.write(f"Sorted array (Sequential):\n")
        file.write(" ".join(map(str, sorted_arr1)))
        file.write("\n\n")
        file.write(f"Sequential merge sort time: {seq_time:.4f} seconds\n\n")
        
        file.write(f"Sorted array (ThreadPoolExecutor):\n")
        file.write(" ".join(map(str, sorted_arr2)))
        file.write("\n\n")
        file.write(f"ThreadPoolExecutor merge sort time: {thread_time:.4f} seconds\n\n")
        
        file.write(f"Arrays are equal: {sorted_arr1 == sorted_arr2}\n")
        file.write(f"Speedup: {seq_time / thread_time:.2f}x\n")

if __name__ == "__main__":
    main()