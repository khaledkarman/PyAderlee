import threading
from datetime import datetime, timedelta
import queue
import time

# Configuration
number_of_threads = 20
# start_date = datetime(2025, 1, 1)
start_date = "2025-01-01 03"
# end_date = datetime(2025, 1, 10)
end_date = "2025-01-10 12"

# Convert start and end dates to datetime objects
start_date = datetime.strptime(start_date, "%Y-%m-%d %H")
end_date = datetime.strptime(end_date, "%Y-%m-%d %H")
hours = [str(i).zfill(2) for i in range(24)]

# Create a thread-safe queue of dates (as strings)
date_queue = queue.Queue()
current_date = start_date
while current_date <= end_date:
    date_queue.put(current_date.strftime("%Y-%m-%d %H"))
    current_date += timedelta(hours=1)

# Shared dictionary to track thread progress
progress = {}
progress_lock = threading.Lock()  # Ensure thread-safe updates

def worker(thread_id):
    thread_name = f"Thread-{thread_id}"
    while True:
        try:
            # Attempt to fetch a date without blocking
            date_to_process = date_queue.get(block=False)
        except queue.Empty:
            # No more dates to process
            print(f"{thread_name} found no further tasks and is exiting.")
            break
        
        # Mark the date as being processed by this thread
        with progress_lock:
            progress[thread_name] = f"Processing date: {date_to_process}"
        print(f"{thread_name} processing {date_to_process}")
        
        # Simulate processing the date (e.g., performing work)
        time.sleep(1)
        
        # Update progress after processing
        with progress_lock:
            progress[thread_name] = f"Finished processing {date_to_process}"
        
        # Mark the task as done
        date_queue.task_done()

# Create and start threads
threads = []
for i in range(1, number_of_threads + 1):
    t = threading.Thread(target=worker, args=(i,))
    threads.append(t)
    t.start()

# Wait for all threads to finish
for t in threads:
    t.join()

# Print final progress status from all threads
print("\nFinal progress status:")
with progress_lock:
    for thread, status in progress.items():
        print(f"{thread}: {status}")
