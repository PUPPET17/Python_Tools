import os
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox

def list_files(startpath, exclude_dirs):
    output = []
    for root, dirs, files in os.walk(startpath):
        # Skip excluded directories
        if any(exclude_dir in root.split(os.sep) for exclude_dir in exclude_dirs):
            continue

        level = root.replace(startpath, '').count(os.sep)
        indent = '│   ' * level
        output.append(f"{indent}├── {os.path.basename(root)}/")
        subindent = '│   ' * (level + 1)

        for i, f in enumerate(files):
            if i == len(files) - 1:
                output.append(f"{subindent}└── {f}")
            else:
                output.append(f"{subindent}├── {f}")
    
    return output

def select_directory():
    return filedialog.askdirectory(title="Select Project Directory")

def select_exclude_dirs():
    exclude_dirs = simpledialog.askstring("Exclude Directories", "Enter directories to exclude (comma-separated):")
    return exclude_dirs.split(',') if exclude_dirs else []

def save_directory_structure(directory_path, output, output_file):
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"Directory Structure: {directory_path}\n")
        f.write("=" * 50 + "\n")
        for line in output:
            f.write(line + "\n")

def main():
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    directory_path = select_directory()
    if not directory_path:
        messagebox.showerror("Error", "No directory selected!")
        return

    exclude_dirs = select_exclude_dirs()
    
    result = list_files(directory_path, exclude_dirs)
    
    output_file = filedialog.asksaveasfilename(
        initialdir="./", 
        title="Save Directory Structure",
        defaultextension=".txt",
        filetypes=(("Text files", "*.txt"), ("All files", "*.*"))
    )
    
    if output_file:
        save_directory_structure(directory_path, result, output_file)
        messagebox.showinfo("Success", f"Directory structure saved to {output_file}")
    else:
        messagebox.showwarning("Warning", "File not saved!")

if __name__ == "__main__":
    main()
