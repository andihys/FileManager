
import os
import shutil
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkinter.font import Font
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pandas as pd
from PIL import Image
import pytesseract


class FileManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced File Manager")
        self.root.geometry("750x700")
        self.root.resizable(False, False)

        # Minimal Theme and Fonts
        self.theme_color = "#f5f5f5"
        self.button_color = "#ffffff"
        self.text_color = "#333333"
        self.border_color = "#dddddd"
        self.font_primary = Font(family="Arial", size=11)
        self.font_heading = Font(family="Helvetica Neue", size=14, weight="bold")

        self.root.configure(bg=self.theme_color)
        self.folder_path = tk.StringVar()

        # Header
        header_frame = tk.Frame(self.root, bg=self.theme_color)
        header_frame.pack(pady=10)
        tk.Label(header_frame, text="Advanced File Manager", font=self.font_heading, bg=self.theme_color, fg=self.text_color).pack()

        # Input Frame
        input_frame = tk.Frame(self.root, bg=self.theme_color)
        input_frame.pack(pady=10, padx=10)

        tk.Label(input_frame, text="Folder Path:", font=self.font_primary, bg=self.theme_color, fg=self.text_color).grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.folder_entry = tk.Entry(input_frame, textvariable=self.folder_path, width=50, font=self.font_primary, relief="flat", bg=self.button_color, fg=self.text_color)
        self.folder_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        tk.Button(input_frame, text="Browse", command=self.browse_folder, font=self.font_primary, bg=self.button_color, fg=self.text_color, relief="flat", borderwidth=1, highlightbackground=self.border_color).grid(row=0, column=2, padx=5, pady=5)

        # Buttons Frame
        button_frame = tk.Frame(self.root, bg=self.theme_color)
        button_frame.pack(pady=20)

        buttons = [
            ("Organize by Type", self.organize_files),
            ("Cluster Files", self.preview_cluster_files),
            ("Predict Categories", self.preview_predict_categories),
            ("Extract Text (OCR)", self.perform_ocr),
            ("Unpack Subfolders", self.unpack_subfolders),
        ]

        for i, (text, command) in enumerate(buttons):
            tk.Button(
                button_frame,
                text=text,
                command=command,
                font=self.font_primary,
                bg=self.button_color,
                fg=self.text_color,
                relief="flat",
                borderwidth=1,
                highlightbackground=self.border_color,
                width=25,
            ).grid(row=i, column=0, padx=10, pady=5, sticky="w")

        # Log Area with Scrollbar
        log_frame = tk.Frame(self.root, bg=self.theme_color)
        log_frame.pack(pady=20, fill="both", expand=True)

        tk.Label(log_frame, text="Log Area:", font=self.font_heading, bg=self.theme_color, fg=self.text_color).pack(anchor="w")
        self.log_text = tk.Text(log_frame, wrap="word", height=15, font=("Courier New", 10), bg=self.button_color, fg=self.text_color, relief="flat", borderwidth=1)
        self.log_text.pack(side="left", fill="both", expand=True, padx=5, pady=5)

        log_scrollbar = ttk.Scrollbar(log_frame, orient="vertical", command=self.log_text.yview)
        log_scrollbar.pack(side="right", fill="y")
        self.log_text.configure(yscrollcommand=log_scrollbar.set)

    def browse_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.folder_path.set(folder)

    def log(self, message, color="black"):
        self.log_text.config(state="normal")
        self.log_text.insert("end", f"{message}\n", (color,))
        self.log_text.tag_config(color, foreground=color)
        self.log_text.config(state="disabled")
        self.log_text.see("end")

    def unpack_subfolders(self):
        folder = self.folder_path.get()
        if not folder:
            messagebox.showerror("Error", "Please select a folder!")
            return

        try:
            unpacked_folder = os.path.join(folder, "Unpacked")
            os.makedirs(unpacked_folder, exist_ok=True)

            for root, dirs, files in os.walk(folder):
                for file in files:
                    file_path = os.path.join(root, file)
                    if os.path.isfile(file_path):
                        shutil.copy(file_path, os.path.join(unpacked_folder, file))
                        self.log(f"Copied {file} from {root} to {unpacked_folder}", color="blue")

            messagebox.showinfo("Success", "Files copied to Unpacked folder successfully!")
            self.log("Files copied to Unpacked folder successfully!", color="green")
        except Exception as e:
            self.log(f"Error during unpacking subfolders: {e}", color="red")
            messagebox.showerror("Error", f"An error occurred: {e}")

    def organize_files(self):
        folder = self.folder_path.get()
        if not folder:
            messagebox.showerror("Error", "Please select a folder!")
            return

        try:
            file_types = {
                "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff"],
                "Documents": [".md", ".pdf", ".docx", ".txt", ".xlsx", ".pptx"],
                "Videos": [".mp4", ".mkv", ".avi", ".mov"],
                "Music": [".mp3", ".wav", ".aac", ".flac"],
                "Code": [".py", ".c", ".cpp"]
            }

            for file_name in os.listdir(folder):
                file_path = os.path.join(folder, file_name)
                if not os.path.isfile(file_path):
                    continue

                file_moved = False
                for category, extensions in file_types.items():
                    if file_name.lower().endswith(tuple(extensions)):
                        self._move_file(file_path, folder, category)
                        file_moved = True
                        break

                if not file_moved:
                    self._move_file(file_path, folder, "Others")

            messagebox.showinfo("Success", "Files organized successfully by type!")
            self.log("Files organized successfully by type!", color="green")
        except Exception as e:
            self.log(f"Error during file organization: {e}", color="red")
            messagebox.showerror("Error", f"An error occurred: {e}")

    def perform_ocr(self):
        image_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.jpeg *.png *.bmp *.tiff")])
        if not image_path:
            return

        try:
            text = pytesseract.image_to_string(Image.open(image_path))
            self.log("Extracted Text from Image:", color="blue")
            self.log(text, color="green")
            messagebox.showinfo("OCR Result", text)
        except Exception as e:
            self.log(f"Error during OCR: {e}", color="red")
            messagebox.showerror("Error", f"An error occurred during OCR: {e}")

    def preview_cluster_files(self):
        folder = self.folder_path.get()
        if not folder:
            messagebox.showerror("Error", "Please select a folder!")
            return

        try:
            texts = []
            file_names = []

            for file_name in os.listdir(folder):
                if file_name.endswith(".txt"):
                    file_path = os.path.join(folder, file_name)
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        texts.append(f.read())
                        file_names.append(file_name)

            if not texts:
                self.log("No text files found for clustering.", color="blue")
                messagebox.showinfo("Info", "No text files found to cluster.")
                return

            vectorizer = TfidfVectorizer(stop_words='english')
            X = vectorizer.fit_transform(texts)

            kmeans = KMeans(n_clusters=3, random_state=42)
            labels = kmeans.fit_predict(X)

            actions_preview = ""
            for label, file_name in zip(labels, file_names):
                actions_preview += f"Move {file_name} to Cluster_{label}\n"

            self.preview_action(
                "Preview Clustering",
                "The following actions will be executed if you accept:",
                actions_preview,
                lambda: self.execute_cluster_files(labels, file_names, folder)
            )
        except Exception as e:
            self.log(f"Error during file clustering preview: {e}", color="red")
            messagebox.showerror("Error", f"An error occurred: {e}")

    def execute_cluster_files(self, labels, file_names, folder):
        try:
            for label, file_name in zip(labels, file_names):
                cluster_folder = os.path.join(folder, f"Cluster_{label}")
                os.makedirs(cluster_folder, exist_ok=True)
                shutil.move(os.path.join(folder, file_name), os.path.join(cluster_folder, file_name))

            messagebox.showinfo("Success", "Files clustered successfully!")
            self.log("Files clustered successfully!", color="green")
        except Exception as e:
            self.log(f"Error during file clustering execution: {e}", color="red")
            messagebox.showerror("Error", f"An error occurred: {e}")

    def preview_predict_categories(self):
        folder = self.folder_path.get()
        if not folder:
            messagebox.showerror("Error", "Please select a folder!")
            return

        try:
            data = pd.DataFrame({
                "text": ["budget report", "holiday photo", "project plan", "beach video"],
                "category": ["Documents", "Images", "Documents", "Videos"]
            })

            X_train, X_test, y_train, y_test = train_test_split(
                data["text"], data["category"], test_size=0.25, random_state=42
            )

            vectorizer = TfidfVectorizer(stop_words='english')
            X_train_tfidf = vectorizer.fit_transform(X_train)
            X_test_tfidf = vectorizer.transform(X_test)

            model = RandomForestClassifier(random_state=42)
            model.fit(X_train_tfidf, y_train)

            y_pred = model.predict(X_test_tfidf)
            accuracy = accuracy_score(y_test, y_pred)
            self.log(f"Category prediction model accuracy: {accuracy * 100:.2f}%", color="blue")

            actions_preview = ""
            for file_name in os.listdir(folder):
                if file_name.endswith(".txt"):
                    file_path = os.path.join(folder, file_name)
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        predicted_category = model.predict(vectorizer.transform([content]))[0]
                        actions_preview += f"Move {file_name} to {predicted_category}\n"

            self.preview_action(
                "Preview Predictions",
                "The following actions will be executed if you accept:",
                actions_preview,
                lambda: self.execute_predict_categories(folder, model, vectorizer)
            )
        except Exception as e:
            self.log(f"Error during category prediction preview: {e}", color="red")
            messagebox.showerror("Error", f"An error occurred: {e}")

    def execute_predict_categories(self, folder, model, vectorizer):
        try:
            for file_name in os.listdir(folder):
                if file_name.endswith(".txt"):
                    file_path = os.path.join(folder, file_name)
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        predicted_category = model.predict(vectorizer.transform([content]))[0]
                        category_folder = os.path.join(folder, predicted_category)
                        os.makedirs(category_folder, exist_ok=True)
                        shutil.move(file_path, os.path.join(category_folder, file_name))

            messagebox.showinfo("Success", "Categories predicted and files organized!")
            self.log("Categories predicted and files organized!", color="green")
        except Exception as e:
            self.log(f"Error during category prediction execution: {e}", color="red")
            messagebox.showerror("Error", f"An error occurred: {e}")

    def _move_file(self, file_path, folder, category):
        category_folder = os.path.join(folder, category)
        os.makedirs(category_folder, exist_ok=True)
        shutil.move(file_path, os.path.join(category_folder, os.path.basename(file_path)))
        self.log(f"Moved {file_path} to {category_folder}", color="blue")


    def preview_action(self, title, message, preview_details, action):
        def proceed():
            confirmation_window.destroy()
            action()

        def cancel():
            confirmation_window.destroy()

        confirmation_window = tk.Toplevel(self.root)
        confirmation_window.title(title)
        confirmation_window.geometry("600x400")
        confirmation_window.resizable(False, False)

        tk.Label(confirmation_window, text=message, font=self.font_primary, wraplength=580, justify="center", bg=self.theme_color).pack(pady=10)
        preview_text = tk.Text(confirmation_window, wrap="word", height=15, font=("Courier New", 10), bg="#ffffff", fg="#333333")
        preview_text.pack(padx=10, pady=5, fill="both", expand=True)
        preview_text.insert("1.0", preview_details)
        preview_text.config(state="disabled")

        tk.Button(confirmation_window, text="Accept", command=proceed, bg="#007aff", fg="white", font=self.font_primary, width=15).pack(side="left", padx=50, pady=10)
        tk.Button(confirmation_window, text="Decline", command=cancel, bg="#d9534f", fg="white", font=self.font_primary, width=15).pack(side="right", padx=50, pady=10)


if __name__ == "__main__":
    root = tk.Tk()
    app = FileManagerApp(root)
    root.mainloop()
