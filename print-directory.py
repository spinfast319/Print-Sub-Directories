# Print Sub Directories
# author: hypermodified
# This python script loops through a directory and finds all the sub directories and prints them to a file


# Import dependencies
import os  # Imports functionality that let's you interact with your operating system
import re  # Imports functionality to use regular expressions

#  Set your directory here
directory_to_check = "M:\Music" # Which directory do you want to start with?
list_directory = "M:\Python Test Environment\Logs"  # Which directory do you want the log in?

# Set whether you are using nested folders or have all albums in one directory here
# If you have all your ablums in one music directory Music/Album_name then set this value to 1
# If you have all your albums nest in a Music/Artist/Album style of pattern set this value to 2
# The default is 1
album_depth = 2

# Establishes the counters for completed albums and missing origin files
total_count = 0
folder_count = 0

# identifies album directory level
path_segments = directory_to_check.split(os.sep)
segments = len(path_segments)
album_location = segments + album_depth

# creates the list of folders that need to be printed 
folder_set = set()

# A function to check whether the directory is a an album or a sub-directory
def level_check(directory):
    global total_count
    global album_location

    print("")
    print(directory)
    print("Folder Depth:")
    print(f"--The albums are stored {album_location} folders deep.")

    path_segments = directory.split(os.sep)
    directory_location = len(path_segments)

    print(f"--This folder is {directory_location} folders deep.")

    # Checks to see if a folder is an album or subdirectory by looking at how many segments are in a path
    if album_location == directory_location:
        print("--This is an album.")
        total_count += 1  # variable will increment every loop iteration
        return True
    elif album_location < directory_location:
        print("--This is a sub-directory")
        return False
    elif album_location > directory_location and album_depth == 2:
        print("--This is an artist folder.")
        return False

def collect_directory(directory):
    global folder_count
    global folder_set
    
    skip_list = ["Artwork", "Info"]
    
    subfolders = [ f.name for f in os.scandir(directory) if f.is_dir() ]
    if subfolders:
        for i in subfolders:
            if i in skip_list:
                print(f"----{i} is the correct folder name.")
                print("Don't log this.")
                pass
            elif re.match(r"\bCD(\d+)\b", i):
                print(f"----{i} is the correct folder name.")
                print("Don't log this.")
                pass
            elif re.match(r"^CD(\d+) \- ", i):
                print(f"----{i} is the correct folder name.")
                print("Don't log this.")
                pass
            else:
                print(f"----{i} is a unique folder name.")  
                folder_set.add(i)
                print("Logged it.")
    folder_count += 1  # variable will increment every loop iteration
    
    
def write_list(folder_set):
    global list_directory
    
    list_name = "unique_subfolders.txt"
    list_path = os.path.join(list_directory, list_name)

    with open(list_path, "a", encoding="utf-8") as list_name:
        list_name.write(" \n")
        list_name.write("Unique Subfolders \n")
        list_name.write("----------------- \n")
        list_name.write('\n'.join(folder_set)) 
        list_name.write(" ")
        list_name.write(" \n")
        list_name.close()        
    
# The main function that controls the flow of the script
def main():
    global folder_set
    global album_location
    global album_depth

    # Get all the subdirectories of directory_to_check recursively and store them in a list:
    directories = [os.path.abspath(x[0]) for x in os.walk(directory_to_check)]
    directories.remove(os.path.abspath(directory_to_check)) # If you don't want your main directory included

    #  Run a loop that goes into each directory identified in the list and runs the function that prints the directories
    for i in directories:
        os.chdir(i)         # Change working Directory
        # establish directory level
        is_album = level_check(i)
        print(is_album)
          
        # make a filter for itunes and musicbee folders
        path_segments = i.split(os.sep)
        if album_depth == 1:
            parent_folder = path_segments[-1]
        elif album_depth == 2:
            parent_folder = path_segments[-2]     
        
        if parent_folder == "iTunes":
            print("Excluding iTunes Folder")
            pass
        elif parent_folder == "MusicBee":
            print("Excluding MusicBee Folder")
            pass
        else:  
            if is_album:
                collect_directory(i)      # Run your function
          

    # Print the list of unique subfolders.
    print("")
    print("Unique Subfolders")
    folder_set = sorted(folder_set)
    print ('\n'.join(folder_set))
    print("")
    print(f"This script looked in {folder_count} folders for subfolders.")       

    # Write the subfolder names to a text file
    write_list(folder_set)


if __name__ == "__main__":
    main()
