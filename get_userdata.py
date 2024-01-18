import hypixel
import os
import sys
import json
import logging

# Add the parent folder to the Python path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "."))
sys.path.append(parent_dir)

# Define the paths to the input and output folders
input_folder = os.path.join(parent_dir, 'userdata')
output_folder = os.path.join(parent_dir, 'userkills')
daily_output_folder = os.path.join(parent_dir, 'dailykills')

# Get guild id
with open(os.path.join(parent_dir, "guild_id.txt")) as readguild:
    hypixel_guild = readguild.readline()

# Create a logger instance
logger = logging.getLogger(__name__)
# Set the logging level to ERROR
logger.setLevel(logging.ERROR)
# Create a console handler
console_handler = logging.StreamHandler()
# Create a formatter
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
# Set the formatter for the console handler
console_handler.setFormatter(formatter)
# Add the console handler to the logger
logger.addHandler(console_handler)

def savedata():
    # Get the list of existing files in the "userdata" directory
    existing_files = os.listdir(os.path.join(parent_dir,"userdata"))
    
    # Get all users in guild
    guild = hypixel.Guild(hypixel_guild)
    guildlist = guild.getMembers()
    members = [member for sublist in guildlist.values() for member in sublist]

    # Get individual stats for all users in guild
    for member in members:
        user = hypixel.SkyblockPlayer(member)
        raw = user.JSON
        raw_json = json.dumps(raw)
    
        # Write the contents of "raw_json" to the user's file
        file_path = os.path.join("userdata", f"{member}.txt")
        with open(file_path, "w") as file:
            file.write(raw_json)
    
        # Check if a text file exists for a member who is no longer a member
        if f"{member}.txt" in existing_files:
            existing_files.remove(f"{member}.txt")  # Remove the file from the existing files list

    # Delete text files for members who are no longer members
    for file_name in existing_files:
        file_path = os.path.join(parent_dir, "userdata", file_name)
        os.remove(file_path)

    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Get the list of files in the input folder
    file_list = os.listdir(input_folder)

    # Iterate over each file in the input folder
    for file_name in file_list:
        # Construct the full path to the input file
        input_file_path = os.path.join(input_folder, file_name)

        try:
            # Load the JSON data from the input file
            with open(input_file_path) as f:
                data = json.load(f)
    
        except FileNotFoundError:
            error_message = f"File not found: {input_file_path}"
            logger.error(error_message)
            continue  # Skip to the next input file
        except json.JSONDecodeError as e:
            error_message = f"Error decoding JSON in {input_file_path}: {str(e)}"
            logger.error(error_message)
            continue  # Skip to the next input file

        # Check if 'profiles' key is present and has a value of 'null'
        if 'profiles' not in data or data['profiles'] is None or data['profiles'] == 'null':
            file_name_without_ext = file_name[:-4]
            error_message = f'Error: Player "{file_name_without_ext}" has no Skyblock profile'
            continue

        # Iterate over profiles to find the selected profile
        selected_profile = None
        for profile in data.get('profiles', []):
            if profile.get('selected', False):
                selected_profile = profile
                break

        # Extract the file name without the extension
        file_name_without_ext = file_name[:-4]

        # Find the matching member based on the file name
        matching_member = None
        for member_key, member_value in selected_profile.get('members', {}).items():
            if member_key == file_name_without_ext:
                matching_member = member_value
                break

        # Access the "bestiary" field from the matching member
        bestiary_value = matching_member.get('bestiary', {}).get('kills', {})

        if bestiary_value is None:
            error_message = f"Error: 'bestiary' field is missing in {file_name}"
            logger.error(error_message)
            continue  # Skip to the next input file

        # Retrieve "kills_arachne_300" and "kills_arachne_500" values, setting to 0 if they don't exist
        kills_t1 = bestiary_value.get('arachne_300', 0)
        kills_t2 = bestiary_value.get('arachne_500', 0)
        #kills_t3 = bestiary_value.get('arachne_xxx', 0) # Preparing for when T3 update comes sometime in the future

        # Construct the full path to the output file
        output_file_path = os.path.join(output_folder, file_name)

        # Save the output variables kills_t1 and kills_t2 to the output file
        with open(output_file_path, 'w') as f:
            f.write(f'kills_t1: {kills_t1}\n')
            f.write(f'kills_t2: {kills_t2}\n')
            #f.write(f'kills_t3: {kills_t3}\n') # Preparing for when T3 update comes sometime in the future
