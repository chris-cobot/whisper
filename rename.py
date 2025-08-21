import os

# Loads a bunch of files from a directory in alphanumeric order
# Renames them to a new name
# The new name is the original name with the first 4 characters removed
# The new name is also in alphanumeric order


# Get the directory of the script
# script_dir = os.path.dirname(os.path.abspath(__file__))

# Get the directory of the files
files_dir = "/home/chrislai/testing/whisper/data/sandbox/"

# Get the files in the directory
files = os.listdir(files_dir)
files.sort(key=lambda x: int(x.split(' ')[-1].split('.')[0]))
print(files)

for episode_number, file in enumerate(files):
    # Get the original name
    original_name = file

    # Get the new name
    new_name = f"episode_{episode_number:06d}.{original_name.split('.')[-1]}"

    # Rename the file
    os.rename(os.path.join(files_dir, file), os.path.join(files_dir, new_name))

    