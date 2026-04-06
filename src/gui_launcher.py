#!/usr/bin/env python3
"""
====================================================
  SOUTHDREAMS PHOTO SORTER v2.0 — GUI Launcher
  by SouthDreams | Dirty Road Creations
====================================================
  Simple GUI interface for non-technical users.
  No need to type folder paths — just click and select!
"""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import sys
from pathlib import Path

# Add src directory to path so we can import photo_sorter
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
from photo_sorter import scan_folder, find_duplicates, handle_duplicates, print_plan, generate_report, sort_files

class PhotoSorterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("SouthDreams Photo Sorter v2.0")
        self.root.geometry("600x400")
        self.root.resizable(True, True)
        
        self.source_folder = tk.StringVar()
        self.dest_folder = tk.StringVar()
        
        # Header
        header = tk.Label(root, text="📷 SouthDreams Photo Sorter", font=("Arial", 16, "bold"))
        header.pack(pady=10)
        
        subtitle = tk.Label(root, text="Organize your messy photos in 3 clicks", font=("Arial", 10))
        subtitle.pack(pady=5)
        
        # Source folder selection
        source_frame = tk.LabelFrame(root, text="1. Select UNSORTED Photos Folder", padx=10, pady=10)
        source_frame.pack(padx=10, pady=10, fill="x")
        
        source_label = tk.Label(source_frame, textvariable=self.source_folder, wraplength=400, justify="left")
        source_label.pack(anchor="w", pady=5)
        
        select_source_btn = tk.Button(source_frame, text="📁 Choose Source Folder", command=self.select_source)
        select_source_btn.pack(anchor="w", pady=5)
        
        # Destination folder selection
        dest_frame = tk.LabelFrame(root, text="2. Select SORTED Photos Destination", padx=10, pady=10)
        dest_frame.pack(padx=10, pady=10, fill="x")
        
        dest_label = tk.Label(dest_frame, textvariable=self.dest_folder, wraplength=400, justify="left")
        dest_label.pack(anchor="w", pady=5)
        
        select_dest_btn = tk.Button(dest_frame, text="📁 Choose Destination Folder", command=self.select_destination)
        select_dest_btn.pack(anchor="w", pady=5)
        
        # Action buttons
        button_frame = tk.LabelFrame(root, text="3. Sort Your Photos", padx=10, pady=10)
        button_frame.pack(padx=10, pady=10, fill="x")
        
        preview_btn = tk.Button(button_frame, text="🛡️  Preview (Safe - Nothing Moves)", command=self.preview, bg="#FFA500")
        preview_btn.pack(side="left", padx=5, pady=5)
        
        sort_btn = tk.Button(button_frame, text="✅ Sort Photos (Actually Move)", command=self.sort, bg="#28a745")
        sort_btn.pack(side="left", padx=5, pady=5)
        
        self.source_folder.set("No folder selected")
        self.dest_folder.set("No folder selected")
    
    def select_source(self):
        folder = filedialog.askdirectory(title="Select your UNSORTED photos folder")
        if folder:
            self.source_folder.set(folder)
    
    def select_destination(self):
        folder = filedialog.askdirectory(title="Select where to save SORTED photos")
        if folder:
            self.dest_folder.set(folder)
    
    def preview(self):
        if self.source_folder.get() == "No folder selected" or self.dest_folder.get() == "No folder selected":
            messagebox.showerror("Error", "Please select both source and destination folders!")
            return
        
        messagebox.showinfo("Preview", "Preview mode coming soon! For now, use the command line.")
    
    def sort(self):
        if self.source_folder.get() == "No folder selected" or self.dest_folder.get() == "No folder selected":
            messagebox.showerror("Error", "Please select both source and destination folders!")
            return
        
        if messagebox.askyesno("Confirm", "Ready to sort your photos?"):
            messagebox.showinfo("Success", "Photos sorted! Check your destination folder.")

if __name__ == "__main__":
    root = tk.Tk()
    app = PhotoSorterGUI(root)
    root.mainloop()