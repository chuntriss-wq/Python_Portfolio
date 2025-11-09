import os
import shutil # <--- Added for robust file moving

# ⚠️ IMPORTANT: Changed to a RAW STRING (r"...") for Windows paths
SOURCE_DIR =   # Replace with your actual path!  

# Dictionary mapping extensions to folder names
FILE_CATEGORIES = {
    # Images
    ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg'): 'Images',
    # Videos
    ('.mp4', '.mov', '.avi', '.mkv', '.wmv'): 'Videos',
    # Documents
    ('.pdf', '.docx', '.doc', '.txt', '.pptx', '.xlsx'): 'Documents',
    # Archives
    ('.zip', '.rar', '.7z'): 'Archives',
    # Code/Scripts
    ('.py', '.js', '.html', '.css', '.c', '.cpp'): 'Code',
    # Executables
    ('.exe', '.msi'): 'Executables',
    # Others
    # Default category for anything not listed
}
def organize_files(source_dir):
    print(f"--- Starting organization in: {source_dir} ---")
    
    if not os.path.exists(source_dir):
        print(f"Error: Source directory not found at {source_dir}")
        return

    for item in os.listdir(source_dir):
        item_path = os.path.join(source_dir, item)
        
        if os.path.isdir(item_path):
            continue
        
        # 1. Determine category folder and get original name/extension
        original_name, ext = os.path.splitext(item)
        ext = ext.lower()
        
        category_folder = 'Others'
        for extensions, folder_name in FILE_CATEGORIES.items():
            if ext in extensions:
                category_folder = folder_name
                break
        
        category_path = os.path.join(source_dir, category_folder)
        os.makedirs(category_path, exist_ok=True)
        
        # 2. --- DUPLICATE HANDLING LOGIC STARTS HERE ---
        
        # Start with the intended path
        new_path = os.path.join(category_path, item)
        counter = 1
        
        # Loop until a unique file name is found
        while os.path.exists(new_path):
            # Create a new file name: original_name(counter).ext
            new_item_name = f"{original_name}({counter}){ext}"
            new_path = os.path.join(category_path, new_item_name)
            counter += 1
        
        # --- DUPLICATE HANDLING LOGIC ENDS HERE ---
        
        # 3. Move the file
        try:
            shutil.move(item_path, new_path)
            # Check if we renamed the file for a more informative message
            if counter > 1:
                print(f'Conflict: Renamed and moved **{item}** to **{new_path}**')
            else:
                print(f'Moved: **{item}** to **{category_folder}/**')
        except Exception as e:
            print(f'Error moving {item}: {e}')

    print(f"--- Organization complete! ---")



def main():
    # It's good practice to print the target directory before running
    print(f"Attempting to organize: {SOURCE_DIR}")
    organize_files(SOURCE_DIR)

if __name__ == "__main__":
    main()