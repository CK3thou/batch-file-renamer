# 🔄 Batch File Renamer - Web Interface

A simple yet powerful web-based tool to batch rename files in a directory.

## Features

✨ **Interactive Web Interface** - Beautiful, user-friendly interface  
📁 **Easy Directory Selection** - Simply paste your directory path  
👁️ **Live Preview** - See changes before applying them  
🔧 **Multiple Operations**:
   - Remove specific text from filenames
   - Remove characters from the beginning (left)
   - Remove characters from the end (right)
✅ **Safe Renaming** - Preview changes and confirm before applying  
⚡ **Fast & Responsive** - Real-time feedback

## Requirements

- Python 3.6+
- Flask

## Installation

1. **Install Flask** (if not already installed):
```bash
pip install flask
```

2. **Navigate to the project directory**:
```bash
cd path\to\batch-file-renamer
```

## Running the Application

### Web Interface (Recommended)
```bash
python app.py
```

This will start a web server. Open your browser and go to:
```
http://localhost:5000
```

### Original CLI Version
```bash
# Interactive mode (prompts for folder selection)
python file-renamer.py

# Command-line mode
python file-renamer.py "C:\path\to\folder" --remove-text "old_prefix_"
python file-renamer.py "C:\path\to\folder" --remove-chars 5 --from-left --preview
python file-renamer.py "C:\path\to\folder" --remove-chars 3 --from-right
```

## Usage Examples

### In the Web Interface:

1. **Enter Directory Path**
   - Example: `C:\Users\John\Downloads\Photos`

2. **Select Operation**
   - Remove Text: `_old` → removes "_old" from all filenames
   - Remove from Left: `5` → removes first 5 characters
   - Remove from Right: `3` → removes last 3 characters

3. **Preview Changes**
   - Click "👁️ Preview Changes" to see what will be renamed
   - Review the list of changes

4. **Apply Changes**
   - If satisfied, click "✅ Apply Changes"
   - Confirm the action in the popup dialog
   - Watch as files are renamed

### Examples:

**Scenario 1: Remove prefix from photos**
- Directory: `C:\My Photos`
- Operation: Remove Text
- Text: `IMG_`
- Result: `IMG_20240101.jpg` → `20240101.jpg`

**Scenario 2: Remove unwanted prefix**
- Directory: `C:\Downloads`
- Operation: Remove from Left
- Characters: `4`
- Result: `2024_Report.pdf` → `_Report.pdf`

**Scenario 3: Remove file extension prefix**
- Directory: `C:\Documents`
- Operation: Remove from Right
- Characters: `5`
- Result: `Resume_FINAL_v2.pdf` → `Resume_FINA.pdf`

## Features Explained

### Preview Mode
- Shows exactly what will change
- Displays how many files will be affected
- No files are modified until you confirm

### Smart Handling
- Preserves file extensions
- Prevents overwriting existing files
- Shows errors for problematic renames
- Handles special characters safely

## Troubleshooting

**Issue: "Directory not found"**
- Ensure the path is correct and accessible
- Try using the full absolute path
- Check that you have read/write permissions

**Issue: Files not renaming**
- Make sure files are not open in another program
- Check that you have write permissions to the directory
- Verify the pattern matches what you want to remove

**Issue: Port 5000 already in use**
- Edit `app.py` and change `port=5000` to another port (e.g., `port=5001`)
- Or close the application using port 5000

## License

MIT License - Feel free to use and modify!

## Support

For issues or feature requests, please create an issue in the GitHub repository.
