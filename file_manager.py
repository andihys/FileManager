import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox


class FileManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Manager")
        self.root.geometry("450x250")

        self.folder_path = tk.StringVar()

        tk.Label(self.root, text="Select a folder to organize:").pack(pady=10)
        tk.Entry(self.root, textvariable=self.folder_path, width=50).pack(pady=5)
        tk.Button(self.root, text="Browse", command=self.browse_folder).pack(pady=5)
        tk.Button(self.root, text="Organize Files", command=self.organize_files).pack(pady=20)

    def browse_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.folder_path.set(folder)

    def organize_files(self):
        folder = self.folder_path.get()
        if not folder:
            messagebox.showerror("Error", "Please select a folder!")
            return

        try:
            file_types = {
                "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff"],
                "Documents": [".pdf", ".docx", ".txt", ".xlsx", ".pptx", ".md"],
                "Videos": [".mp4", ".mkv", ".avi", ".mov"],
                "Music": [".mp3", ".wav", ".aac", ".flac"],
                "Archives": [".zip", ".rar", ".7z", ".tar"],
                "Code": [".py", ".c", ".cpp", ".java"],
                "Executables": [".exe"]
            }

            for category, extensions in file_types.items():
                category_folder = os.path.join(folder, category)
                os.makedirs(category_folder, exist_ok=True)

                for file_name in os.listdir(folder):
                    file_path = os.path.join(folder, file_name)
                    if os.path.isfile(file_path) and file_name.lower().endswith(tuple(extensions)):
                        shutil.move(file_path, os.path.join(category_folder, file_name))

            messagebox.showinfo("Success", "Files have been organized successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = FileManagerApp(root)
    root.mainloop()
