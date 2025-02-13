import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import sys
from datetime import datetime

class SymlinkConverterApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Symlink Converter")
        self.master.geometry("700x500")

        # Configure dark theme colors
        self.style = ttk.Style()
        self.style.theme_use('default')
        
        # Configure colors
        bg_color = "#2b2b2b"
        fg_color = "#ffffff"
        button_bg = "#3c3f41"
        button_fg = "#ffffff"
        tree_bg = "#313335"
        tree_fg = "#ffffff"
        tree_selected = "#4b6eaf"
        
        # Configure ttk styles
        self.style.configure(
            "Treeview",
            background=tree_bg,
            foreground=tree_fg,
            fieldbackground=tree_bg
        )
        self.style.configure(
            "Treeview.Heading",
            background=button_bg,
            foreground=button_fg
        )
        self.style.map(
            "Treeview",
            background=[('selected', tree_selected)],
            foreground=[('selected', 'white')]
        )
        self.style.configure(
            "TProgressbar",
            troughcolor=bg_color,
            background=tree_selected
        )
        
        # Configure main window
        self.master.configure(bg=bg_color)
        
        # Configure frames with background
        self.button_frame = tk.Frame(master, bg=bg_color)
        self.button_frame.pack(pady=10)
        
        self.progress_frame = tk.Frame(master, bg=bg_color)
        self.progress_frame.pack(pady=5, fill=tk.X, padx=10)

        # Configure buttons with new style
        button_style = {
            'bg': button_bg,
            'fg': button_fg,
            'relief': tk.FLAT,
            'padx': 20,
            'pady': 5,
            'cursor': 'hand2'
        }
        
        self.select_source_button = tk.Button(
            self.button_frame,
            text="Select Source Folder",
            command=self.select_source_folder,
            **button_style
        )
        self.select_source_button.pack(side=tk.LEFT, padx=5)

        self.select_destination_button = tk.Button(
            self.button_frame,
            text="Select Destination Folder",
            command=self.select_destination_folder,
            state=tk.DISABLED,
            **button_style
        )
        self.select_destination_button.pack(side=tk.LEFT, padx=5)

        self.convert_button = tk.Button(
            self.button_frame,
            text="Start Conversion",
            command=self.convert_symlinks,
            state=tk.DISABLED,
            **button_style
        )
        self.convert_button.pack(side=tk.LEFT, padx=5)

        # Configure progress label
        self.progress_label = tk.Label(
            self.progress_frame,
            text="Ready...",
            bg=bg_color,
            fg=fg_color
        )
        self.progress_label.pack(side=tk.LEFT, padx=5)

        # Create a frame to hold the Treeview and scrollbar
        self.tree_frame = tk.Frame(master, bg=bg_color)
        self.tree_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        # Treeview to log symlinks as we convert them
        self.tree = ttk.Treeview(self.tree_frame, columns=("Path", "Target"), show="headings")
        self.tree.heading("Path", text="Symlink Path")
        self.tree.heading("Target", text="Symlink Target")
        self.tree.column("Path", width=330)
        self.tree.column("Target", width=330)
        
        # Add scrollbar
        self.scrollbar = ttk.Scrollbar(self.tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scrollbar.set)
        
        # Pack scrollbar and tree in the correct order
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Add progress bar
        self.progress_bar = ttk.Progressbar(
            self.progress_frame,
            orient=tk.HORIZONTAL,
            length=300,
            mode='determinate'
        )
        self.progress_bar.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Add hover effects in init
        self._configure_button_hover(self.select_source_button)

    def _on_enter(self, event):
        """Handle mouse enter event for buttons"""
        event.widget.configure(bg="#4b6eaf")

    def _on_leave(self, event):
        """Handle mouse leave event for buttons"""
        event.widget.configure(bg="#3c3f41")

    # Add hover effects to buttons
    def _configure_button_hover(self, button):
        button.bind("<Enter>", self._on_enter)
        button.bind("<Leave>", self._on_leave)

    def select_source_folder(self):
        folder_selected = filedialog.askdirectory(title="Select Source Folder")
        if folder_selected:
            self.source_folder = folder_selected
            self.select_destination_button.config(state=tk.NORMAL)
            self._configure_button_hover(self.select_destination_button)

    def select_destination_folder(self):
        folder_selected = filedialog.askdirectory(title="Select Destination Folder")
        if folder_selected:
            self.destination_folder = folder_selected
            self.convert_button.config(state=tk.NORMAL)
            self._configure_button_hover(self.convert_button)

    def convert_symlinks(self):
        if not self.source_folder:
            messagebox.showwarning("No Source Folder", "Please select a source folder.")
            return
        if not self.destination_folder:
            messagebox.showwarning("No Destination Folder", "Please select a destination folder.")
            return

        # Clear any previous logs
        for item in self.tree.get_children():
            self.tree.delete(item)

        errors = []
        success_count = 0

        # Count total files for progress bar
        total_files = sum([len(files) for _, _, files in os.walk(self.source_folder)])
        self.progress_bar["maximum"] = total_files
        processed_files = 0
        
        print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Starting conversion process...")
        print(f"Source: {self.source_folder}")
        print(f"Destination: {self.destination_folder}")
        print(f"Total files to process: {total_files}\n")

        # Walk through the source folder recursively
        for root, dirs, files in os.walk(self.source_folder):
            for file_name in files:
                file_path = os.path.join(root, file_name)
                processed_files += 1
                
                # Update progress bar and label
                self.progress_bar["value"] = processed_files
                progress_percent = (processed_files / total_files) * 100
                self.progress_label.config(
                    text=f"Processing: {processed_files}/{total_files} ({progress_percent:.1f}%)"
                )
                self.master.update_idletasks()
                
                # Log to terminal
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Processing: {file_path}")

                # Build the relative path so we can recreate folder structure in the destination
                relative_path = os.path.relpath(file_path, self.source_folder)
                dest_path = os.path.join(self.destination_folder, relative_path)
                os.makedirs(os.path.dirname(dest_path), exist_ok=True)

                # If the file is a symlink, copy the real file instead
                if os.path.islink(file_path):
                    try:
                        real_file = os.readlink(file_path)  # Path the symlink points to
                        real_file_path = os.path.join(os.path.dirname(file_path), real_file)

                        if not os.path.exists(real_file_path):
                            errors.append(f"Real file does not exist: {real_file_path}")
                            continue

                        shutil.copy2(real_file_path, dest_path)
                        success_count += 1
                        # Log symlink conversion in the Treeview
                        self.tree.insert("", tk.END, values=(file_path, real_file_path))
                        print(f"    └─ Converted symlink -> {dest_path}")
                    except Exception as e:
                        print(f"    └─ Error: {str(e)}")
                        errors.append(f"Error processing {file_path}: {str(e)}")
                else:
                    # Just copy normal files as is
                    try:
                        shutil.copy2(file_path, dest_path)
                        print(f"    └─ Copied file -> {dest_path}")
                    except Exception as e:
                        print(f"    └─ Error: {str(e)}")
                        errors.append(f"Error copying {file_path}: {str(e)}")

        # Reset progress bar and label
        self.progress_label.config(text="Conversion complete!")
        print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Conversion complete!")
        print(f"Successfully processed symlinks: {success_count}")
        if errors:
            print("\nErrors encountered:")
            for error in errors:
                print(f"- {error}")

        self.convert_button.config(state=tk.DISABLED)

def main():
    root = tk.Tk()
    app = SymlinkConverterApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()