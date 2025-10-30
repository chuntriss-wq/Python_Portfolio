import multiprocessing 
import time
import hashlib # Crucial library for cryptographic hashing
import os # Used to generate a secure random salt

# --- 1. The CPU-Bound Task Function ---
def hash_password(task_id, password):
    """
    This function simulates a slow, CPU-intensive password hashing operation.
    It repeatedly hashes the password (key stretching) to make it harder to crack,
    which is an ideal scenario for multiprocessing.
    """
    
    start_time = time.time()
    
    # Generate a random salt (a unique random string added to the password before hashing)
    # This prevents attackers from using pre-computed rainbow tables.
    salt = os.urandom(16) 
    
    # 1. Log the start of the task
    print(f"🚦 [START] Task {task_id}: Hashing password '{password}'...")
    
    # 2. Perform the heavy hashing calculation
    
    # We use a loop of 500,000 iterations to simulate a strong password stretching mechanism.
    # This is a CPU-intensive task that benefits massively from multiprocessing.
    hashed_result = password.encode('utf-8')
    for _ in range(500000): # Run 500,000 times
        hashed_result = hashlib.sha256(salt + hashed_result).digest()
        
    duration = time.time() - start_time
    
    # Convert the final hash to a readable format
    final_hash = hashed_result.hex() 
    
    # 3. Log the completion of the task
    print(f"✅ [DONE] Task {task_id} finished in {duration:.2f}s.")
    # In a real app, we would store this final_hash and the salt in the database!
    print(f"   [RESULT] Final Hash (first 20 chars): {final_hash[:20]}...") 

# --- 2. Main Execution Block ---
if __name__ == "__main__":
    
    # Data: A list of passwords to hash concurrently
    tasks = [
        (1, "my-secret-password-123"),
        (2, "hunter2"),
        (3, "AdminPass4567!"),
        (4, "verylongbutweakkey")
    ]
    
    # List to hold the Process objects
    processes = []
    
    print(f"Prepared to hash {len(tasks)} passwords concurrently.")
    
    print("\n--- Starting CONCURRENT Password Hashing (Multiprocessing) ---")
    
    start_time_concurrent = time.time()
    
    # 1. Create the processes
    for task_id, password in tasks:
        # Create a new Process object.
        process = multiprocessing.Process(target=hash_password, args=(task_id, password,))
        processes.append(process)
        process.start() # Start the process (tells it to begin running the function in a new core)
        
    
    # 2. Wait for all processes to finish (The Join Command remains crucial)
    print("\n--- Main program waiting for tasks to complete... ---")
    for process in processes:
        process.join()
        
    end_time_concurrent = time.time()
    
    # Calculate and display the total time
    total_time = end_time_concurrent - start_time_concurrent
    print("\n----------------------------------------------------------------------")
    print(f"✅ All {len(tasks)} passwords hashed in: {total_time:.2f} seconds.")
    print("----------------------------------------------------------------------")
