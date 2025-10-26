import datetime
import os
import re # Import regex for advanced log parsing

# --- Constants ---
# Define the default log file name
LOG_FILE = 'application.log'
# Regex to match the log entry format: [YYYY-MM-DD HH:MM:SS] Message
# This pattern captures the timestamp (Group 1) and the message (Group 2)
LOG_PATTERN = re.compile(r"^\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\] (.*)$")

# --- LogEntry Class (Parent Data Model) ---
class LogEntry:
    """
    Represents a single, parsed log entry with structured attributes.
    This is the Parent class.
    """
    # *** NEW: CLASS ATTRIBUTE ***
    # This attribute is shared across ALL instances of LogEntry and its children.
    total_log_entries = 0 
    
    def __init__(self, timestamp_str: str, message: str):
        """Constructor (Initializer) for the LogEntry object."""
        
        # INSTANCE ATTRIBUTES (Unique to this object)
        self.timestamp_str = timestamp_str
        self.message = message
        # Single underscore suggests internal/protected use
        self.level = self._determine_level() 
        
        # 1. Update the SHARED Class Attribute
        LogEntry.total_log_entries += 1
        
        # 2. Use the Class Attribute value to set a unique Instance ID
        # Double underscore triggers Python's name mangling for pseudo-privacy
        self.__secret_id = f"ID-{LogEntry.total_log_entries:03d}"
        
    def _determine_level(self) -> str:
        """
        Helper method (protected) to determine the log level based on message 
        content. Intended for internal use by the class or its children.
        """
        if "ERROR" in self.message.upper():
            return "🚨 ERROR"
        return "INFO"

    def format_for_display(self) -> str:
        """Formats the entry for the summary printout."""
        # This method defines the default output format for all standard logs.
        return f"  {self.level:<10} | {self.timestamp_str} | {self.message}"
        
    def __repr__(self) -> str:
        """Special method for string representation (debugging)."""
        # We access the name-mangled attribute here, which works internally
        mangled_id = self.__secret_id
        return f"LogEntry(id='{mangled_id}', level='{self.level}', timestamp='{self.timestamp_str}', message='{self.message}')"

# --- CriticalLogEntry Class (Child Class) ---
class CriticalLogEntry(LogEntry):
    """
    A specialized log entry that inherits from LogEntry.
    It overrides methods to handle CRITICAL level logs distinctly.
    """
    def _determine_level(self) -> str:
        """
        Overrides the parent method. Since this class is only instantiated 
        for critical messages, we hardcode the level here.
        """
        return "🔥 CRITICAL"

    def format_for_display(self) -> str:
        """
        Overrides the parent method to give critical logs a distinct look 
        by adding extra borders/emphasis.
        """
        # Call the parent's implementation using super() and strip whitespace
        parent_format = super().format_for_display().strip()
        # Add the custom formatting around the parent's output
        return f"[!!! ALERT !!!] {parent_format} [!!! ALERT !!!]"


# --- NEW: DebugLogEntry Class (Child Class for Polymorphism) ---
class DebugLogEntry(LogEntry):
    """
    A specialized log entry that is only displayed if DEBUG_MODE is active.
    Demonstrates polymorphism: responds to format_for_display(), but conditionally.
    """
    def _determine_level(self) -> str:
        """Hardcode level to DEBUG."""
        return "🔬 DEBUG"

    def format_for_display(self) -> str:
        """
        Only formats the entry if the global LogAnalyzer.DEBUG_MODE is True.
        Otherwise, it returns an empty string, effectively hiding the log.
        This is the core of the polymorphic behavior.
        """
        # Accessing the class attribute of LogAnalyzer to determine visibility
        if LogAnalyzer.DEBUG_MODE:
            # Call the parent's implementation using super()
            return super().format_for_display()
        return "" # Hides the log entry if not in DEBUG_MODE


# --- LogAnalyzer Class (Encapsulating Functionality) ---
class LogAnalyzer:
    """
    Encapsulates the functionality required to read, parse, and summarize
    the contents of a specific log file.
    """
    # Class Attribute - shared by all instances, controls debug visibility
    DEBUG_MODE = False 

    def __init__(self, filename: str):
        """Initializes the analyzer object."""
        self.filename = filename
        self.entries = []  
        self.parsing_failures = 0

    def load_logs(self):
        """
        Reads the log file, line by line, and uses logic to instantiate 
        LogEntry, CriticalLogEntry, or DebugLogEntry objects.
        """
        if not os.path.exists(self.filename):
            print(f"File {self.filename} does not exist.")
            return

        print(f"Attempting to load logs from {self.filename}...")
        
        try:
            with open(self.filename, 'r') as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue

                    match = LOG_PATTERN.match(line)
                    
                    if match:
                        timestamp_str, message = match.groups()
                        
                        # *** POLYMORPHISM / INHERITANCE LOGIC ***
                        # Decide which class to instantiate based on keywords
                        if "CRITICAL" in message.upper() or "FATAL" in message.upper():
                            entry = CriticalLogEntry(timestamp_str, message) 
                        elif "DEBUG" in message.upper():
                            # NEW: Instantiate the specialized Debug class
                            entry = DebugLogEntry(timestamp_str, message)
                        else:
                            entry = LogEntry(timestamp_str, message)
                            
                        self.entries.append(entry)
                    else:
                        self.parsing_failures += 1
                        print(f"  [PARSING FAILURE] | {line}")

        except IOError as e:
            print(f"❌ Error reading log file {self.filename}: {e}")
        except Exception as e:
            print(f"❌ An unexpected error occurred during analysis: {e}")

    def generate_summary(self):
        """
        Prints the structured report based on the loaded log entries.
        Polymorphism ensures each entry prints itself correctly (or not at all).
        """
        print(f"\n--- Analysis Summary of {self.filename} (DEBUG_MODE={self.DEBUG_MODE}) ---")
        
        if not self.entries:
            print("No log entries loaded or file was empty.")
            return

        error_count = 0
        
        for entry in self.entries:
            # Polymorphism: Calls the object's specific format_for_display()
            formatted_line = entry.format_for_display()
            
            if formatted_line: 
                print(formatted_line) 
                
                # We check the entry's level attribute (which is set in __init__) 
                if "CRITICAL" in entry.level or "ERROR" in entry.level:
                    error_count += 1

        print(f"\nTotal entries processed: {len(self.entries)}. Total errors found: {error_count}.")
        if self.parsing_failures > 0:
            print(f"Warning: {self.parsing_failures} lines could not be parsed.")


# --- Standalone Function for Writing Logs ---

def log_message(message: str, filename: str = LOG_FILE) -> None:
    """
    Appends a timestamped message to a specified log file. (Unchanged)
    """
    try:
        # 1. Get the current timestamp in a standard format
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # 2. Format the complete log entry
        log_entry = f"[{timestamp}] {message}\n"

        # 3. Use 'with open' to ensure the file is properly closed.
        with open(filename, 'a') as f:
            f.write(log_entry)

        print(f"✅ Successfully logged: '{message.strip()}' to {filename}")

    except IOError as e:
        print(f"❌ Error writing to log file {filename}: {e}")
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")


# --- Example Usage (Generating logs) ---

print("--- Starting Log Manager Test (Including CRITICAL and DEBUG Log) ---")

# (Ensure we have fresh logs to analyze)
log_message("System initialized successfully.")
log_message("User 'Chris' completed Workbook 2 successfully!")
log_message("DEBUG: Function 'calculate_metrics' started.") # NEW DEBUG LOG
log_message("Data export started.", filename="data_events.log")
log_message("ERROR: Database connection timed out. Retrying in 5s.")
log_message("CRITICAL: All core services have failed. Shutting down immediately.")
log_message("Data export completed successfully.", filename="data_events.log")
log_message("DEBUG: Metrics calculated and validated successfully.") # NEW DEBUG LOG


# --- Verification (Running the new Analysis - DEBUG_MODE OFF) ---

print("\n--- Running Encapsulated Log Analysis (DEBUG_MODE=False) ---")

# 1. Create an Analyzer object for the main log file
app_analyzer = LogAnalyzer(LOG_FILE)
app_analyzer.load_logs()
app_analyzer.generate_summary() # Debug logs will be hidden here

# --- Verification (Running the new Analysis - DEBUG_MODE ON) ---
print("\n--- Toggling LogAnalyzer.DEBUG_MODE to True ---")
# Accessing the CLASS attribute directly to change behavior globally
LogAnalyzer.DEBUG_MODE = True 

print("\n--- Running Encapsulated Log Analysis (DEBUG_MODE=True) ---")
# The analyzer object is the same, but the summary call now shows the debug entries
app_analyzer.generate_summary() 

# Reset the debug mode for other examples
LogAnalyzer.DEBUG_MODE = False

# 2. Create a separate Analyzer object for the data events log (Still works!)
data_analyzer = LogAnalyzer("data_events.log")
data_analyzer.load_logs()
data_analyzer.generate_summary()


# --- Demonstration of Visibility ---
print("\n--- Demonstration of Python Visibility ---")

# We grab the first entry from the analysis (if it exists)
if app_analyzer.entries:
    first_entry = app_analyzer.entries[0]

    print(f"\n1. Public Access (Recommended):")
    # Accessing 'message' is public and straightforward
    print(f"   Message: {first_entry.message}")

    print(f"\n2. Protected Access (Convention Only - Use with Caution):")
    # Accessing '_determine_level' method is discouraged but possible
    # We call the method directly, but developers know not to do this generally.
    print(f"   Level (via internal method): {first_entry._determine_level()}")

    print(f"\n3. Pseudo-Private Access (Name Mangled):")
    try:
        # This will fail because Python has changed the name internally
        print(f"   Attempting direct __secret_id access: {first_entry.__secret_id}")
    except AttributeError:
        print("   Direct access to __secret_id failed (AttributeError).")
        # Python changes the name to _ClassName__attributeName, which is required for external access
        print(f"   Accessing mangled name: {first_entry._LogEntry__secret_id}")

else:
    print("No entries to demonstrate visibility.")

# --- Final OOP Concept: Class vs. Instance Attributes ---
print("\n--- Class vs. Instance Attribute Demonstration ---")
# Accessing the shared counter directly via the class name
print(f"Total LogEntry objects ever created (Class Attribute): {LogEntry.total_log_entries}")
if app_analyzer.entries:
    # We grab the last entry written to the log
    last_entry = app_analyzer.entries[-1]
    # Accessing the unique, sequential ID assigned during object creation
    print(f"ID of the last entry (Instance Attribute): {last_entry._LogEntry__secret_id}")
