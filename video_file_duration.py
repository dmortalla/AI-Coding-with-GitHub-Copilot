# The script calculates the duration of video files in a given directory.
# It uses the moviepy library to do this.

import os  # Import the os module for interacting with the operating system, including file and directory operations
import argparse  # Import the argparse module for parsing command-line arguments
from moviepy.editor import VideoFileClip  # Import VideoFileClip from moviepy.editor for handling video files and calculating their durations

def calculate_duration(file_path):
    """Calculate the duration of the given video file.
    
    Args:
        file_path (str): The path to the video file.
    
    Returns:
        float: The duration of the video in seconds. Returns 0 if an error occurs.
    """
    try:
        with VideoFileClip(file_path) as video:
            return video.duration
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return 0

def process_directory(directory):
    """Process the directory to calculate video durations and write to a text file.
    
    Args:
        directory (str): The path to the directory containing video files.
    """
    folder_durations = {}
    video_files_found = False
    grand_total_duration = 0  # Initialize grand total duration
    
    # Walk through the directory and all its subdirectories
    for root, _, files in os.walk(directory):
        folder_name = os.path.basename(root)
        total_duration = 0
        video_files = []
        
        # Iterate over each file in the current directory
        for file in files:
            file_path = os.path.join(root, file)
            file_path = os.path.normpath(file_path)  # Normalize the file path
            if file.lower().endswith(('.mp4', '.avi', '.mov', '.mkv', '.flv')):  # Check if the file is a video file
                video_files_found = True
                duration = calculate_duration(file_path)
                total_duration += duration
                grand_total_duration += duration  # Add to grand total duration
                video_files.append((file, duration))
        
        # If video files are found in the current folder, store their durations
        if video_files:
            folder_durations[folder_name] = (video_files, total_duration)
    
    # If no video files are found in any folder or sub-folder, print a notification
    if not video_files_found:
        print("No video files found in any folder or sub-folder.")
        return
    
    # Define the path for the output file in the main directory
    output_file = os.path.join(directory, "video_durations.txt")
    
    # Write the results to a text file with UTF-8 encoding
    with open(output_file, "w", encoding="utf-8") as f:
        for folder, (videos, total_duration) in folder_durations.items():
            f.write(f"Folder: {folder}\n")
            for video, duration in videos:
                duration_minutes = duration / 60  # Convert duration to minutes
                f.write(f"  {video}: {duration_minutes:.2f} minutes\n")
            total_duration_minutes = total_duration / 60  # Convert total duration to minutes
            f.write(f"Total duration: {total_duration_minutes:.2f} minutes\n\n")
        
        # Calculate and write the grand total duration in minutes
        grand_total_duration_hours = grand_total_duration / 3600
        f.write(f"Grand Total Duration: {grand_total_duration_hours:.2f} hours\n")
    
    print(f"Video durations have been written to {output_file}.")
    os.startfile(output_file)  # Automatically open the output text file

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Calculate video durations in a directory.")
    parser.add_argument("directory", help="Directory containing video files to check.")
    args = parser.parse_args()

    process_directory(args.directory)


# To run the script:
# Use the CLI and run by entering the following command:
# python video_file_duration.py "directory_path"
