import sqlite3
import datetime

class DatabaseManager:
    def __init__(self, db_name="security_log.db"):
        self.db_name = db_name
        self.conn = None
        self.cursor = None

    def connect(self):
        """Establishes a connection to the SQLite database file."""
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()
        except sqlite3.Error as e:
            print(f"Error connecting to database: {e}")

    def close(self):
        """Closes the database connection."""
        if self.conn:
            self.conn.close()

    def create_table(self):
        """Creates the security_log table if it doesn't already exist."""
        sql_create_table = """
        CREATE TABLE IF NOT EXISTS security_log (
            id INTEGER PRIMARY KEY,
            timestamp TEXT NOT NULL,
            event_type TEXT NOT NULL,
            source_ip TEXT,
            details TEXT
        );
        """
        self.cursor.execute(sql_create_table)
        self.conn.commit()

    def insert_event(self, event_type, source_ip, details):
        """Inserts a new event record into the security_log table."""
        timestamp = datetime.datetime.now().isoformat()
        sql_insert = """
        INSERT INTO security_log (timestamp, event_type, source_ip, details)
        VALUES (?, ?, ?, ?);
        """
        # We use the tuple (timestamp, event_type, source_ip, details) to securely pass values
        self.cursor.execute(sql_insert, (timestamp, event_type, source_ip, details))
        self.conn.commit()
        
    def get_all_events(self):
        """Retrieves all records from the security_log table."""
        self.cursor.execute("SELECT * FROM security_log;")
        return self.cursor.fetchall()

    def get_filtered_events(self, type_filter):
        """
        Retrieves records based on a specific event_type using the SQL WHERE clause.
        This is the filtering operation essential for security analysis.
        """
        sql_select_filtered = """
        SELECT * FROM security_log WHERE event_type = ?;
        """
        # The comma (type_filter,) makes it a single-element tuple for the query execution
        self.cursor.execute(sql_select_filtered, (type_filter,))
        return self.cursor.fetchall()


# --- Main Execution Block ---
if __name__ == "__main__":
    
    # Initialize and connect
    db_manager = DatabaseManager()
    db_manager.connect()
    db_manager.create_table()
    
    # Clear existing data for a clean run
    # (Optional, but good for demos)
    db_manager.cursor.execute("DELETE FROM security_log;")
    db_manager.conn.commit()

    # Insert sample data (with mixed types)
    db_manager.insert_event('LOGIN_SUCCESS', '192.168.1.5', 'User Jane logged in.')
    db_manager.insert_event('LOGIN_FAIL', '10.0.0.100', 'Incorrect password attempt from external IP.')
    db_manager.insert_event('SYSTEM_ALERT', '127.0.0.1', 'Disk space is low.')
    db_manager.insert_event('LOGIN_FAIL', '10.0.0.100', 'Second failed attempt. Brute force suspected.')
    db_manager.insert_event('LOGIN_SUCCESS', '192.168.1.15', 'User Joe logged in.')
    
    print("--- 5 Sample Logs Inserted ---")

    # 1. Retrieve ALL events (as before)
    all_events = db_manager.get_all_events()
    print("\n[ALL EVENTS RETRIEVED]:", len(all_events), "records found.")
    # print(all_events) # Uncomment this to see all raw data
    
    # 2. FILTER for only LOGIN_FAIL events
    fail_events = db_manager.get_filtered_events('LOGIN_FAIL')
    
    print("\n--- FILTERING: Results for 'LOGIN_FAIL' ---")
    print(f"[{len(fail_events)}] Failed Login Attempts Found:")
    for event in fail_events:
        # Print only the important columns for analysis
        print(f"  | Time: {event[1][11:19]} | IP: {event[3]} | Details: {event[4]}")


    db_manager.close()
    
    print("\nDatabase closed.")
