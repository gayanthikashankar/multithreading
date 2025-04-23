import time
import requests
import os
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed

def download_file(url, index):
    #downlaod a file from URL with an index for naming
    filename = f"file_{index+1}.download"
    
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()  #raiseexception for HTTP errors
        
        with open(filename, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)
        
        print(f"Downloaded {url} to {filename}")
        return True, url, filename
    except Exception as e:
        print(f"Error downloading {url}: {e}")
        return False, url, filename

def sequential_download(urls):
    #Download files sequentially
    start_time = time.time()
    results = []
    
    for i, url in enumerate(urls):
        success, url, filename = download_file(url, i)
        results.append((success, url, filename))
    
    success_count = sum(1 for success, _, _ in results if success)
    elapsed_time = time.time() - start_time
    
    print(f"\nSequential download completed: {success_count}/{len(urls)} files")
    print(f"Total time: {elapsed_time:.2f} seconds")
    
    return elapsed_time, success_count, results

def threaded_download_with_pool(urls, max_workers=4):
    #Download files using ThreadPoolExecutor
    start_time = time.time()
    results = []
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        #create a mapping of futures to their respective URLs and indices
        future_to_url = {
            executor.submit(download_file, url, i): (url, i)
            for i, url in enumerate(urls)
        }
        
        #process results as they complete
        for future in as_completed(future_to_url):
            results.append(future.result())
    
    success_count = sum(1 for success, _, _ in results if success)
    elapsed_time = time.time() - start_time
    
    print(f"\nThreadPoolExecutor download completed: {success_count}/{len(urls)} files")
    print(f"Total time: {elapsed_time:.2f} seconds")
    
    return elapsed_time, success_count, results

def read_urls_from_file(filename):
    #read URLs from a text file, one URL per line
    with open(filename, 'r') as file:
        return [line.strip() for line in file if line.strip()]

def main():
    #directories exist
    os.makedirs('sample_inputs', exist_ok=True)
    os.makedirs('sample_outputs', exist_ok=True)
    
    urls_file = 'sample_inputs/urls.txt'
    if not os.path.exists(urls_file):
        #else:  create default URLs file
        default_urls = [
            "https://www.gutenberg.org/files/1661/1661-0.txt",
            "https://www.adobe.com/support/products/enterprise/knowledgecenter/media/c4611_sample_explain.pdf",
            "https://upload.wikimedia.org/wikipedia/commons/e/ec/Mona_Lisa%2C_by_Leonardo_da_Vinci%2C_from_C2RMF_retouched.jpg",
            "https://www.irs.gov/pub/irs-pdf/p17.pdf"
        ]
        
        with open(urls_file, 'w') as file:
            file.write('\n'.join(default_urls))
        print(f"Created default URLs file: {urls_file}")

    #get URLs from file or command line argument
    if len(sys.argv) > 1:
        urls = read_urls_from_file(sys.argv[1])
    else:
        urls = read_urls_from_file(urls_file)
    
    if not urls:
        print("No URLs found, check the URLs file.")
        return
    
    print(f"Found {len(urls)} URLs to download from {urls_file}\n")
    
    #create/open output file
    output_file = 'sample_outputs/output_file_downloader.txt'
    with open(output_file, 'w') as file:
        file.write(f"Found {len(urls)} URLs to download from {urls_file}\n\n")
    
    #sequential download
    print("Sequential Download:")
    seq_time, seq_success, seq_results = sequential_download(urls)
    
    #append to output file
    with open(output_file, 'a') as file:
        file.write("Sequential Download:\n")
        for success, url, filename in seq_results:
            status = "Downloaded" if success else "Failed to download"
            file.write(f"{status} {url} to {filename}\n")
        file.write(f"\nSequential download completed: {seq_success}/{len(urls)} files\n")
        file.write(f"Total time: {seq_time:.2f} seconds\n\n")
    
    #clean up sequential download files to avoid confusion
    for _, _, filename in seq_results:
        if os.path.exists(filename):
            os.remove(filename)
    
    #ThreadPoolExecutor download
    print("\nThreadPoolExecutor Download: ")
    thread_time, thread_success, thread_results = threaded_download_with_pool(urls)
    
    #appendd to output file
    with open(output_file, 'a') as file:
        file.write("ThreadPoolExecutor Download:\n")
        for success, url, filename in thread_results:
            status = "Downloaded" if success else "Failed to download"
            file.write(f"{status} {url} to {filename}\n")
        file.write(f"\nThreadPoolExecutor download completed: {thread_success}/{len(urls)} files\n")
        file.write(f"Total time: {thread_time:.2f} seconds\n\n")
    
    #print and write speedup
    if seq_time > 0:
        speedup = seq_time / thread_time
        print(f"\nThreadPoolExecutor speedup: {speedup:.2f}x")
        
        with open(output_file, 'a') as file:
            file.write(f"ThreadPoolExecutor speedup: {speedup:.2f}x\n")
            file.write("\nBenefits of using ThreadPoolExecutor:\n")
            file.write("1. Simpler code - no need to manually create and manage threads\n")
            file.write("2. Built-in thread pooling to limit resource usage\n")
            file.write("3. Easy handling of results with as_completed() or map()\n")
            file.write("4. Automatic cleanup of thread resources\n")

if __name__ == "__main__":
    main()