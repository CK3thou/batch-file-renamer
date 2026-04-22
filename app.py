#!/usr/bin/env python3
"""
Batch File Renamer - Flask Web Application
"""
import os
import sys
from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max

def get_file_changes(directory, remove_text=None, num_chars=0, from_left=False, from_right=False):
    """
    Calculate what files would be renamed (without actually renaming them).
    Returns a list of (old_name, new_name) tuples.
    """
    if not os.path.isdir(directory):
        return {"error": f"'{directory}' is not a valid directory"}
    
    try:
        files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    except PermissionError:
        return {"error": f"Permission denied accessing '{directory}'"}
    
    if not files:
        return {"files": [], "count": 0}
    
    changes = []
    
    for filename in files:
        new_name = filename
        
        # Get file name and extension separately
        name_parts = os.path.splitext(filename)
        base_name = name_parts[0]
        extension = name_parts[1] if len(name_parts) > 1 else ""
        
        if remove_text:
            # Remove specific text from the base name
            new_base_name = base_name.replace(remove_text, "")
            new_name = new_base_name + extension
        elif num_chars > 0:
            if from_left:
                # Remove characters from the beginning
                new_base_name = base_name[num_chars:]
                new_name = new_base_name + extension
            elif from_right:
                # Remove characters from the end
                new_base_name = base_name[:-num_chars] if num_chars < len(base_name) else ""
                new_name = new_base_name + extension
        
        if new_name != filename:
            changes.append({
                "old_name": filename,
                "new_name": new_name,
                "changed": True
            })
        else:
            changes.append({
                "old_name": filename,
                "new_name": new_name,
                "changed": False
            })
    
    return {
        "directory": directory,
        "files": changes,
        "count": len(changes),
        "changes_count": sum(1 for c in changes if c["changed"])
    }

def apply_renaming(directory, remove_text=None, num_chars=0, from_left=False, from_right=False):
    """
    Actually rename the files in the directory.
    """
    if not os.path.isdir(directory):
        return {"error": f"'{directory}' is not a valid directory"}
    
    try:
        files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    except PermissionError:
        return {"error": f"Permission denied accessing '{directory}'"}
    
    if not files:
        return {"error": "No files found in directory"}
    
    results = []
    errors = []
    
    for filename in files:
        new_name = filename
        
        # Get file name and extension separately
        name_parts = os.path.splitext(filename)
        base_name = name_parts[0]
        extension = name_parts[1] if len(name_parts) > 1 else ""
        
        if remove_text:
            new_base_name = base_name.replace(remove_text, "")
            new_name = new_base_name + extension
        elif num_chars > 0:
            if from_left:
                new_base_name = base_name[num_chars:]
                new_name = new_base_name + extension
            elif from_right:
                new_base_name = base_name[:-num_chars] if num_chars < len(base_name) else ""
                new_name = new_base_name + extension
        
        if new_name != filename:
            old_path = os.path.join(directory, filename)
            new_path = os.path.join(directory, new_name)
            
            # Check for duplicates
            if os.path.exists(new_path):
                errors.append({
                    "old_name": filename,
                    "new_name": new_name,
                    "error": "Destination already exists"
                })
                continue
            
            try:
                os.rename(old_path, new_path)
                results.append({
                    "old_name": filename,
                    "new_name": new_name,
                    "success": True
                })
            except Exception as e:
                errors.append({
                    "old_name": filename,
                    "new_name": new_name,
                    "error": str(e)
                })
    
    return {
        "directory": directory,
        "renamed": results,
        "errors": errors,
        "renamed_count": len(results),
        "error_count": len(errors)
    }

@app.route('/')
def index():
    """Serve the main page."""
    return render_template('index.html')

@app.route('/api/preview', methods=['POST'])
def preview():
    """Preview file changes without applying them."""
    data = request.get_json()
    directory = data.get('directory', '').strip()
    operation = data.get('operation', '')
    
    if not directory:
        return jsonify({"error": "Directory is required"}), 400
    
    remove_text = None
    num_chars = 0
    from_left = False
    from_right = False
    
    if operation == 'remove_text':
        remove_text = data.get('remove_text', '').strip()
        if not remove_text:
            return jsonify({"error": "Text to remove is required"}), 400
    elif operation == 'remove_left':
        try:
            num_chars = int(data.get('num_chars', 0))
            from_left = True
        except (ValueError, TypeError):
            return jsonify({"error": "Invalid number of characters"}), 400
    elif operation == 'remove_right':
        try:
            num_chars = int(data.get('num_chars', 0))
            from_right = True
        except (ValueError, TypeError):
            return jsonify({"error": "Invalid number of characters"}), 400
    else:
        return jsonify({"error": "Invalid operation"}), 400
    
    result = get_file_changes(directory, remove_text, num_chars, from_left, from_right)
    return jsonify(result)

@app.route('/api/apply', methods=['POST'])
def apply():
    """Apply the renaming changes."""
    data = request.get_json()
    directory = data.get('directory', '').strip()
    operation = data.get('operation', '')
    
    if not directory:
        return jsonify({"error": "Directory is required"}), 400
    
    remove_text = None
    num_chars = 0
    from_left = False
    from_right = False
    
    if operation == 'remove_text':
        remove_text = data.get('remove_text', '').strip()
        if not remove_text:
            return jsonify({"error": "Text to remove is required"}), 400
    elif operation == 'remove_left':
        try:
            num_chars = int(data.get('num_chars', 0))
            from_left = True
        except (ValueError, TypeError):
            return jsonify({"error": "Invalid number of characters"}), 400
    elif operation == 'remove_right':
        try:
            num_chars = int(data.get('num_chars', 0))
            from_right = True
        except (ValueError, TypeError):
            return jsonify({"error": "Invalid number of characters"}), 400
    else:
        return jsonify({"error": "Invalid operation"}), 400
    
    result = apply_renaming(directory, remove_text, num_chars, from_left, from_right)
    return jsonify(result)

if __name__ == '__main__':
    print("=" * 60)
    print("Batch File Renamer - Web Interface")
    print("=" * 60)
    print("\nStarting web server...")
    print("Open your browser and go to: http://localhost:5000")
    print("\nPress Ctrl+C to stop the server.")
    print("=" * 60)
    
    app.run(debug=False, host='127.0.0.1', port=5000)
