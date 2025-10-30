import socket
import threading
import time
import sys 

# --- 1. Configuration (Set defaults, these will be overwritten by user input) ---
TARGET_HOST = '127.0.0.1'  
PORT_RANGE_START = 1      
PORT_RANGE_END = 100      
TIMEOUT = 0.5             

# List to store open ports found: now stores (port, service) tuples
open_ports = [] 
print_lock = threading.Lock() 

# Heuristic mapping for common port services
KNOWN_PORTS = {
    21: 'FTP (File Transfer Protocol)',
    22: 'SSH (Secure Shell)',
    23: 'Telnet',
    25: 'SMTP (Simple Mail Transfer Protocol)',
    53: 'DNS (Domain Name System)',
    80: 'HTTP (Web Server)',
    110: 'POP3 (Post Office Protocol)',
    135: 'MS RPC',
    139: 'NetBIOS',
    443: 'HTTPS (Encrypted Web Server)',
    445: 'SMB (File Sharing)',
    3389: 'RDP (Remote Desktop)'
}

# --- 2. The Concurrent Worker Function (I/O Bound Task) ---
def port_scan_worker(port):
    """
    Attempts to connect to a specific port and detect the service running.
    """
    global TARGET_HOST
    
    # Create a socket object
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(TIMEOUT)
    
    # Start with the known service name (will be overwritten if a banner is found)
    service_name = KNOWN_PORTS.get(port, "Unknown")

    try:
        # connect_ex returns 0 if the connection is successful (port is open)
        result = sock.connect_ex((TARGET_HOST, port))
        
        if result == 0:
            
            # --- SERVICE DETECTION LOGIC ---
            if port not in KNOWN_PORTS:
                # For unknown ports, attempt a simple banner grab for identification
                try:
                    # Try to read the initial banner (common for SSH, FTP, etc.)
                    # We use a short timeout and small buffer (1024 bytes)
                    banner = sock.recv(1024).decode(errors='ignore').strip()
                    if banner:
                        # Take the first line of the banner for clean identification
                        first_line = banner.splitlines()[0]
                        service_name = f"Banner: {first_line[:30]}..."
                    else:
                        service_name = "Open (No Banner Detected)"
                except:
                    # Fallback if reading the banner fails
                    service_name = "Open (Silent Service)"
            
            # Use the lock to safely update the shared list
            with print_lock:
                open_ports.append((port, service_name))

            # Use the lock to ensure the print statement doesn't get interrupted
            with print_lock:
                print(f"✅ Port {port:<5} is OPEN ({service_name})")
            
    except socket.error:
        # We silently ignore common connection errors (connection refused, etc.)
        pass
            
    finally:
        # Always close the socket
        sock.close()

# --- 3. Main Execution and Thread Management ---
if __name__ == "__main__":
    
    # --- ARGUMENT HANDLING BLOCK (Unchanged) ---
    if len(sys.argv) != 3:
        print("Usage: python port_scanner.py <target_host_ip> <end_port>")
        print("Example: python port_scanner.py 127.0.0.1 500")
        sys.exit(1)
        
    TARGET_HOST = sys.argv[1] 
    
    try:
        PORT_RANGE_END = int(sys.argv[2]) 
        if PORT_RANGE_END > 65535 or PORT_RANGE_END < 1:
            print("Error: End port must be between 1 and 65535.")
            sys.exit(1)
            
    except ValueError:
        print("Error: Port range end must be a valid number.")
        sys.exit(1)
    # --- END ARGUMENT HANDLING BLOCK ---

    
    print("=" * 40)
    print(f"Starting CONCURRENT Port Scanner")
    print(f"Target: {TARGET_HOST}")
    print(f"Scanning Ports: {PORT_RANGE_START} - {PORT_RANGE_END}")
    print("=" * 40)
    
    start_time = time.time()
    
    threads = []
    
    # Loop through the now-dynamic port range
    for port in range(PORT_RANGE_START, PORT_RANGE_END + 1):
        thread = threading.Thread(target=port_scan_worker, args=(port,))
        threads.append(thread)
        thread.start()
        
    print("\n--- Main program waiting for all threads to finish scanning... ---")
    for thread in threads:
        thread.join()
        
    end_time = time.time()
    
    # --- FINAL SUMMARY UPDATE ---
    
    # Sort the results by port number for clean display
    sorted_ports = sorted(open_ports, key=lambda x: x[0])
    
    print("\n" + "=" * 40)
    print("✅ Scan Complete!")
    print(f"Total time taken: {end_time - start_time:.2f} seconds")
    print("-" * 40)
    
    if sorted_ports:
        print("Open Ports & Detected Services:")
        for port, service in sorted_ports:
            # Print the formatted output using the tuple elements
            print(f"  Port {port:<5}: {service}")
    else:
        print("No open ports found in the scanned range.")
        
    print("=" * 40)
