# Multithreading in Python Assignment

This repository contains implementations of three multithreaded Python tasks using `concurrent.futures.ThreadPoolExecutor` 

## Project Structure

multithreading-assignment/
├── task1_merge_sort.py
├── task2_quicksort.py
├── task3_file_downloader.py
├── README.md
├── sample_inputs/
│   ├── input_merge_sort.txt
│   ├── input_quicksort.txt
│   └── urls.txt
└── sample_outputs/
    ├── output_merge_sort.txt
    ├── output_quicksort.txt
    └── output_file_downloader.txt

## Dependencies

The project requires Python 3.x and the following packages:
- `requests` (for the file downloader task)

You can install the dependencies with:
```bash
pip install requests
```

## Implementation Approach

All three tasks leverage Python's `concurrent.futures` module with `ThreadPoolExecutor` for efficient thread management. This approach offers several advantages over manual thread creation and management:

1. **Thread pooling**: Controls the number of active threads to avoid system resource exhaustion
2. **Simplified API**: Reduces complex thread management to a few simple function calls
3. **Clean error handling**: Built-in exception handling for thread operations
4. **Easy result collection**: Simple methods to gather results from parallel operations

## Task 1: Multi-threaded Merge Sort

### Implementation Approach

The merge sort algorithm is implemented in two versions:
1. **Sequential**: Standard recursive implementation
2. **Multithreaded**: Uses `ThreadPoolExecutor` to sort subarrays in parallel

The multithreaded approach divides the array and creates separate tasks for sorting each subarray. It uses a thread pool to manage the resources efficiently.

### How to Run

```bash
python task1_merge_sort.py
```

### Sample Input/Output

**Input**: A space-separated list of integers in `sample_inputs/input_merge_sort.txt`

**Output**: Performance comparison between sequential and multithreaded implementations

## Task 2: Multi-threaded Quicksort

### Implementation Approach

The quicksort algorithm is implemented in two versions:
1. **Sequential**: Standard recursive implementation 
2. **Multithreaded**: Uses `ThreadPoolExecutor` to sort partitions in parallel

The implementation limits thread creation by reverting to sequential sorting for small arrays, preventing excessive thread overhead.

### How to Run

```bash
python task2_quicksort.py
```

### Sample Input/Output

**Input**: A space-separated list of integers in `sample_inputs/input_quicksort.txt`

**Output**: Performance comparison between sequential and multithreaded implementations

## Task 3: Concurrent File Downloader

### Implementation Approach

The file downloader is implemented in two versions:
1. **Sequential**: Downloads files one after another
2. **Multithreaded**: Uses `ThreadPoolExecutor` with `as_completed()` to download files concurrently

The `as_completed()` function allows processing results as they become available, rather than waiting for all tasks to complete.

### How to Run

With default sample URLs:
```bash
python task3_file_downloader.py
```

With a custom URLs file:
```bash
python task3_file_downloader.py path/to/custom_urls.txt
```

### Sample Input/Output

**Input**: A list of URLs in `sample_inputs/urls.txt`

**Output**: Performance comparison between sequential and multithreaded downloads

## Performance Analysis

The performance of multithreaded implementations depends on several factors:

1. **Task type**: 
   - CPU-bound tasks (sorting) benefit from multithreading up to the number of available CPU cores
   - I/O-bound tasks (downloading) show significant improvements regardless of core count

2. **Input size**: 
   - For small inputs, the overhead of thread creation can outweigh the benefits
   - Larger inputs show more pronounced speedups

3. **System resources**:
   - Number of CPU cores
   - Available memory
   - Network bandwidth (for downloads)

## Benefits of ThreadPoolExecutor

1. **Resource management**: Automatically handles thread creation, reuse, and cleanup
2. **Controlled concurrency**: Limits the number of active threads to avoid resource exhaustion
3. **Simplified API**: More intuitive than directly working with thread objects
4. **Future objects**: Provides a clean way to get results from threaded operations
5. **Exception handling**: Better management of exceptions occurring in threads

## Conclusion

The multithreaded implementations using `ThreadPoolExecutor` demonstrate significant performance improvements over sequential versions, particularly for larger inputs or I/O-bound operations. The code is also cleaner and more maintainable compared to manual thread management.# multithreading
