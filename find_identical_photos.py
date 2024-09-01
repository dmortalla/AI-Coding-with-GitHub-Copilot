# Find by hash and size then delete the older photos
import os  # Import the os module for interacting with the operating system, including file and directory operations
import hashlib  # Import the hashlib module for creating hash values
import argparse  # Import the argparse module for parsing command-line arguments

def calculate_hash(file_path):
    """Calculate the MD5 hash and get the size of the given file.
    
    Args:
        file_path (str): The path to the file.
    
    Returns:
        tuple: A tuple containing the MD5 hash, file size, and file name.
    """
    hasher = hashlib.md5()  # Create an MD5 hash object
    with open(file_path, 'rb') as f:  # Open the file in binary read mode
        buf = f.read()  # Read the entire file into a buffer
        hasher.update(buf)  # Update the hash object with the buffer content
    file_size = os.path.getsize(file_path)  # Get the size of the file
    file_name = os.path.basename(file_path)  # Get the base name of the file
    return hasher.hexdigest(), file_size, file_name  # Return the hash, size, and name

def find_identical_photos(directory):
    """Find and return a list of identical photos in the given directory.
    
    Args:
        directory (str): The path to the directory containing photos.
    
    Returns:
        list: A list of lists, where each inner list contains paths to identical photos.
    """
    hashes = {}  # Dictionary to store file hashes and their corresponding file paths
    for root, _, files in os.walk(directory):  # Walk through the directory and its subdirectories
        for file in files:  # Iterate over each file in the current directory
            file_path = os.path.join(root, file)  # Get the full path of the file
            file_hash, file_size, file_name = calculate_hash(file_path)  # Calculate the hash, size, and name of the file
            hash_key = (file_hash, file_size, file_name)  # Create a unique key based on hash, size, and name
            if hash_key in hashes:  # If the key already exists in the dictionary
                hashes[hash_key].append(file_path)  # Append the file path to the existing list
            else:
                hashes[hash_key] = [file_path]  # Create a new list with the file path
    identical_photos = [paths for paths in hashes.values() if len(paths) > 1]  # Filter out unique photos
    return identical_photos  # Return the list of identical photos

def delete_old_photos(identical_photos):
    """Delete all but the newest photo in each group of identical photos.
    
    Args:
        identical_photos (list): A list of lists, where each inner list contains paths to identical photos.
    """
    for group in identical_photos:  # Iterate over each group of identical photos
        # Sort the group by modification date, newest first
        group.sort(key=lambda x: os.path.getmtime(x), reverse=True)
        # Print the filenames of the identical photos
        print("Identical photos:")
        for photo in group:
            print(f"  {os.path.basename(photo)}")
        # Keep the newest photo and delete the rest
        for photo in group[1:]:  # Skip the first photo (newest) and delete the rest
            os.remove(photo)  # Delete the photo
            print(f"Deleted: {os.path.basename(photo)}")  # Print the name of the deleted photo

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Find and delete identical photos in a directory.")  # Create an argument parser
    parser.add_argument("directory", help="Directory containing photos to check.")  # Add a positional argument for the directory
    args = parser.parse_args()  # Parse the command-line arguments

    identical_photos = find_identical_photos(args.directory)  # Find identical photos in the specified directory
    if identical_photos:  # If identical photos are found
        print("Identical photos found and deleted:")
        delete_old_photos(identical_photos)  # Delete the older photos
    else:
        print("No identical photos found.")  # Print a message if no identical photos are found

# Use the CLI and run by entering the following command:
# python find_identical_photos.py "directory_path"

