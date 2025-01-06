import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

class SymlinkConverterApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Symlink Converter")
        self.master.geometry("600x400")

        self.button_frame = tk.Frame(master)
        self.button_frame.pack(pady=10)

        self.select_files_button = tk.Button(self.button_frame, text="Select Symlink Files", command=self.select_symlink_files)
        self.select_files_button.pack(side=tk.LEFT, padx=5)

        self.convert_button = tk.Button(self.button_frame, text="Convert to Normal Files", command=self.convert_symlinks, state=tk.DISABLED)
        self.convert_button.pack(side=tk.LEFT, padx=5)

        self.tree = ttk.Treeview(master, columns=("Path", "Target"), show="headings")
        self.tree.heading("Path", text="File Path")
        self.tree.heading("Target", text="Symlink Target")
        self.tree.column("Path", width=300)
        self.tree.column("Target", width=300)
        self.tree.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        self.scrollbar = ttk.Scrollbar(master, orient=tk.VERTICAL, command=self.tree.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=self.scrollbar.set)

        self.symlink_files = []
        self.target_directory = ""

    def select_symlink_files(self):
        file_paths = filedialog.askopenfilenames(title="Select Symlink Files")
        if file_paths:
            self.symlink_files = list(file_paths)
            self.convert_button.config(state=tk.NORMAL)
            
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            for path in self.symlink_files:
                target = os.readlink(path) if os.path.islink(path) else "Not a symlink"
                self.tree.insert("", tk.END, values=(path, target))

    def convert_symlinks(self):
        self.target_directory = filedialog.askdirectory(title="Select Target Directory")
        if not self.target_directory:
            messagebox.showwarning("No Directory Selected", "Please select a target directory.")
            return

        errors = []
        success_count = 0  # Track successful conversions
        
        for symlink_path in self.symlink_files:
            if os.path.islink(symlink_path):
                try:
                    real_file = os.readlink(symlink_path)
                    real_file_path = os.path.join(os.path.dirname(symlink_path), real_file)
                    if not os.path.exists(real_file_path):
                        errors.append(f"Real file does not exist: {real_file_path}")
                        continue
                    target_file_path = os.path.join(self.target_directory, os.path.basename(symlink_path))
                    shutil.copy2(real_file_path, target_file_path)
                    success_count += 1
                except Exception as e:
                    errors.append(f"Error processing {symlink_path}: {str(e)}")
            else:
                # Just log non-symlinks as warnings rather than errors
                errors.append(f"Skipped (not a symlink): {symlink_path}")
                continue

        # Show summary message
        message = f"Processed {success_count} files successfully."
        if errors:
            message += "\n\nWarnings/Errors:\n" + "\n".join(errors)
            messagebox.showwarning("Conversion Complete", message)
        else:
            messagebox.showinfo("Success", message)

        self.symlink_files = []
        self.convert_button.config(state=tk.DISABLED)
        
        # Clear the treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

def main():
    root = tk.Tk()
    app = SymlinkConverterApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()