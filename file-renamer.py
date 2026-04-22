#!/usr/bin/env python3
import os
import argparse
import sys
from tkinter import Tk, filedialog

def rename_files(directory, remove_text=None, num_chars=0, from_left=False, from_right=False, preview=False):
    """
    Rename files in a directory by removing specified text or characters.
    
    Args:
        directory (str): Path to the directory containing files to rename
        remove_text (str, optional): Text to remove from filenames
        num_chars (int, optional): Number of characters to remove
        from_left (bool): Remove characters from the beginning of the filename
        from_right (bool): Remove characters from the end of the filename
        preview (bool): Only preview changes without performing renaming
    """
    if not os.path.isdir(directory):
        print(f"Error: '{directory}' is not a valid directory")
        return

    # Get all files in the directory
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    
    if not files:
        print(f"No files found in '{directory}'")
        return
    
    changes_made = False
    
    print(f"{'PREVIEW: ' if preview else ''}Renaming files in '{directory}'...\n")
    
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
            changes_made = True
            old_path = os.path.join(directory, filename)
            new_path = os.path.join(directory, new_name)
            
            # Check for duplicates
            if os.path.exists(new_path) and not preview:
                print(f"Warning: Cannot rename '{filename}' to '{new_name}' - destination already exists")
                continue
                
            print(f"Renaming: '{filename}' -> '{new_name}'")
            
            if not preview:
                try:
                    os.rename(old_path, new_path)
                except Exception as e:
                    print(f"Error renaming '{filename}': {str(e)}")
    
    if not changes_made:
        print("No files were changed based on the specified criteria.")
    else:
        print(f"\n{'Preview completed.' if preview else 'Renaming completed.'}")

def interactive_mode():
    """Interactive mode that prompts user for folder selection and operation details."""
    print("=" * 60)
    print("BATCH FILE RENAMER - Interactive Mode")
    print("=" * 60)
    
    # Prompt user to select directory
    root = Tk()
    root.withdraw()  # Hide the root window
    root.attributes('-topmost', True)  # Bring to front
    
    directory = filedialog.askdirectory(title="Select folder containing files to rename")
    root.destroy()
    
    if not directory:
        print("No directory selected. Exiting.")
        return
    
    # Validate directory
    if not os.path.isdir(directory):
        print(f"Error: '{directory}' is not a valid directory")
        return
    
    # Show files in the directory
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    
    if not files:
        print(f"No files found in '{directory}'")
        return
    
    print(f"\nSelected directory: {directory}")
    print(f"Found {len(files)} file(s):")
    for f in files[:10]:  # Show first 10 files
        print(f"  - {f}")
    if len(files) > 10:
        print(f"  ... and {len(files) - 10} more file(s)")
    
    # Ask user what operation to perform
    print("\n" + "=" * 60)
    print("What would you like to do?")
    print("=" * 60)
    print("1. Remove specific text from filenames")
    print("2. Remove characters from the beginning (left)")
    print("3. Remove characters from the end (right)")
    
    choice = input("\nEnter your choice (1/2/3): ").strip()
    
    remove_text = None
    num_chars = 0
    from_left = False
    from_right = False
    
    if choice == "1":
        remove_text = input("\nEnter the text to remove from filenames: ").strip()
        if not remove_text:
            print("No text entered. Exiting.")
            return
    elif choice == "2":
        try:
            num_chars = int(input("\nHow many characters to remove from the beginning? ").strip())
            if num_chars <= 0:
                print("Number must be positive. Exiting.")
                return
            from_left = True
        except ValueError:
            print("Invalid input. Please enter a number. Exiting.")
            return
    elif choice == "3":
        try:
            num_chars = int(input("\nHow many characters to remove from the end? ").strip())
            if num_chars <= 0:
                print("Number must be positive. Exiting.")
                return
            from_right = True
        except ValueError:
            print("Invalid input. Please enter a number. Exiting.")
            return
    else:
        print("Invalid choice. Exiting.")
        return
    
    # Preview changes
    print("\n" + "=" * 60)
    print("PREVIEW - Changes that would be made:")
    print("=" * 60)
    
    rename_files(
        directory,
        remove_text=remove_text,
        num_chars=num_chars,
        from_left=from_left,
        from_right=from_right,
        preview=True
    )
    
    # Ask for confirmation
    print("\n" + "=" * 60)
    confirm = input("Do you want to apply these changes? (yes/no): ").strip().lower()
    
    if confirm in ["yes", "y"]:
        print("\n" + "=" * 60)
        print("APPLYING CHANGES...")
        print("=" * 60)
        rename_files(
            directory,
            remove_text=remove_text,
            num_chars=num_chars,
            from_left=from_left,
            from_right=from_right,
            preview=False
        )
    else:
        print("Changes cancelled.")

def main():
    parser = argparse.ArgumentParser(
        description="Rename files in a folder by removing text or characters",
        formatter_class=argparse.RawTextHelpFormatter
    )
    
    parser.add_argument("directory", nargs="?", help="Directory containing files to rename")
    
    # Create a mutually exclusive group for removal options
    removal_group = parser.add_mutually_exclusive_group()
    removal_group.add_argument("--remove-text", "-t", help="Text to remove from filenames")
    removal_group.add_argument("--remove-chars", "-c", type=int, metavar="N", 
                               help="Number of characters to remove from filenames")
    
    # Position group (only applicable with --remove-chars)
    position_group = parser.add_mutually_exclusive_group()
    position_group.add_argument("--from-left", "-l", action="store_true", 
                                help="Remove characters from the beginning of filenames")
    position_group.add_argument("--from-right", "-r", action="store_true", 
                                help="Remove characters from the end of filenames")
    
    parser.add_argument("--preview", "-p", action="store_true", 
                        help="Preview changes without renaming files")
    
    args = parser.parse_args()
    
    # If no directory provided, run interactive mode
    if args.directory is None:
        interactive_mode()
        return
    
    # Validate arguments for command-line mode
    if not args.remove_text and not args.remove_chars:
        parser.error("Either --remove-text or --remove-chars is required")
    
    if args.remove_chars and not (args.from_left or args.from_right):
        parser.error("When using --remove-chars, you must specify either --from-left or --from-right")
    
    if (args.from_left or args.from_right) and not args.remove_chars:
        parser.error("--from-left or --from-right can only be used with --remove-chars")
    
    # Call the renaming function
    rename_files(
        args.directory,
        remove_text=args.remove_text,
        num_chars=args.remove_chars or 0,
        from_left=args.from_left,
        from_right=args.from_right,
        preview=args.preview
    )

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        sys.exit(1)