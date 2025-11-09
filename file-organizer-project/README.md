# 📂 Python File Organizer

A simple, robust command-line script designed to automatically organize files in a specified directory (like your Downloads folder) into organized subfolders based on file type.

This script ensures that no files are overwritten by implementing **duplicate detection and renaming**.

## ✨ Features

* **Automatic Sorting:** Moves files (Images, Documents, Videos, Executables, etc.) into designated category folders.
* **Duplicate Handling:** Safely renames files that have the same name in the destination folder (e.g., `file.pdf` becomes `file(1).pdf`).
* **System Safe:** Skips system files (like `desktop.ini`) and existing directories.
* **Customizable:** Easily extendable to include new file types and categories.

## ⚙️ Prerequisites

* Python 3.x

## 🚀 How to Use

### 1. Setup

Create a file named `organizer.py` and paste the script contents into it.

### 2. Configure the Target Directory

You must update the **`SOURCE_DIR`** variable near the top of `organizer.py` to point to the directory you want to clean.

```python
SOURCE_DIR = # Replace with your actual path!