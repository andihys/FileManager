
# File Manager

This repository contains the **File Manager** and **Advanced File Manager** projects with a focus on clean design, modern functionality, and user-friendliness.

## Features Overview

### File Manager
A lightweight script with a simple GUI to help users organize files by type.

**Key Features:**
1. Organizes files into categories like Images, Documents, Videos, Music, and Archives.
2. Moves unrecognized files to an "Others" folder.
3. Tkinter-based GUI.

**Usage:**  
Run the `file_manager.py` script to start the application and select a folder to organize.

---

### Advanced File Manager
An enhanced file manager with a modern design and additional features for intelligent file management.

**Key Features:**
1. **Organize Files by Type:** Automatically categorizes files into folders based on their extensions.
2. **Cluster Files:** Groups text files into clusters based on their content using KMeans clustering.
3. **Predict Categories:** Analyzes text files and predicts their categories using a machine learning model.
4. **Extract Text from Images (OCR):** Extracts text from image files using Tesseract OCR.
5. **Unpack Subfolders:** Copies all files from the selected folder and its subfolders into a single "Unpacked" folder.
6. **Modern Design:** A sleek, Apple-inspired GUI with clean aesthetics and enhanced UX.
7. **Detailed Logs:** Tracks actions with color-coded log messages for errors, successes, and actions.

**Usage:**  
Run the `final_advanced_file_manager_modern_design.py` script to start the application. Use the modern GUI to:
- Organize files, cluster them, predict categories, or extract text using OCR.
- Unpack subfolders into a unified folder while preserving the original files.

---

## Installation

### Python Dependencies
Install the required libraries using:
```bash
pip install pandas scikit-learn pillow pytesseract
```

### Tesseract OCR
Install Tesseract OCR for text extraction from images:

1. **Windows:** Download the installer from [Tesseract OCR GitHub](https://github.com/tesseract-ocr/tesseract).
2. **Linux:** Install via:
   ```bash
   sudo apt-get install tesseract-ocr
   ```
3. **macOS:** Install via Homebrew:
   ```bash
   brew install tesseract
   ```

### Verifying Installation
After installation, verify by running:
```bash
tesseract --version
```

---

## Screenshots
Here are the highlights of the modern design:

1. **Clean and Modern Layout**  
   Buttons are styled with rounded edges and hover effects for an Apple-inspired look.

2. **Detailed Logs with Colors**  
   Logs are color-coded for better visibility:
   - Blue: Informational messages.
   - Green: Success messages.
   - Red: Errors.

---

## Contribution
We welcome contributions to enhance the features or improve the design. Submit a pull request with your changes.

## License
This project is licensed under the MIT License.

**Disclaimer:** Always back up your files before using these tools to prevent accidental data loss.

---
