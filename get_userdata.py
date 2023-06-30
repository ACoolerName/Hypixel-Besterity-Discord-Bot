import hypixel
import os
import sys
import json
import shutil

# Add the parent folder to the Python path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "."))
sys.path.append(parent_dir)

# Define the paths to the input and output folders
input_folder = parent_dir+'\\userdata'
output_folder = parent_dir+'\\userkills'
old_output_folder = parent_dir+'\\userkills_old'

# Get API key
with open(parent_dir+"\\api_key.txt") as readapikey:
    API_KEY = [readapikey.readline()]
hypixel.setKeys(API_KEY)

# Get guild id
with open(parent_dir+"\\guild_id.txt") as readguild:
    hypixel_guild = readguild.readline()

def savedata():
    # Get the list of existing files in the "userdata" directory
    existing_files = os.listdir(os.path.join(parent_dir,"userdata"))
    print(existing_files)
    
    # Get all users in guild
    guild = hypixel.Guild(hypixel_guild)
    guildlist = guild.getMembers()
    members = [member for sublist in guildlist.values() for member in sublist]

    # Get individual stats for all users in guild
    for member in members:
        print(member)
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

    print("REFRESHING DATA")
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Create the old output folder if it doesn't exist
    if not os.path.exists(old_output_folder):
        os.makedirs(old_output_folder)
    else:
        # Delete all old files in the userkills_old directory
        old_files = os.listdir(old_output_folder)
        for file_name in old_files:
            file_path = os.path.join(old_output_folder, file_name)
            os.remove(file_path)

    # Move existing files from userkills to userkills_old
    existing_files = os.listdir(output_folder)
    for file_name in existing_files:
        source_file_path = os.path.join(output_folder, file_name)
        destination_file_path = os.path.join(old_output_folder, file_name)
        shutil.move(source_file_path, destination_file_path)

    # Get the list of files in the input folder
    file_list = os.listdir(input_folder)

    # Iterate over each file in the input folder
    for file_name in file_list:
        # Construct the full path to the input file
        input_file_path = os.path.join(input_folder, file_name)

        # Load the JSON data from the input file
        with open(input_file_path) as f:
            data = json.load(f)

        # Iterate over profiles to find the selected profile
        selected_profile = None
        for profile in data['profiles']:
            if profile.get('selected', False):
                selected_profile = profile
                break

        # Extract the file name without the extension
        file_name_without_ext = file_name[:-4]

        # Find the matching member based on the file name
        matching_member = None
        for member_key, member_value in selected_profile['members'].items():
            if member_key == file_name_without_ext:
                matching_member = member_value
                break

        # Access the "bestiary" field from the matching member
        bestiary_value = matching_member.get('bestiary', {})

        # Retrieve "kills_arachne_300" and "kills_arachne_500" values, setting to 0 if they don't exist
        kills_t1 = bestiary_value.get('kills_arachne_300', 0)
        kills_t2 = bestiary_value.get('kills_arachne_500', 0)

        # Construct the full path to the output file
        output_file_path = os.path.join(output_folder, file_name)

        # Save the output variables kills_t1 and kills_t2 to the output file
        with open(output_file_path, 'w') as f:
            f.write(f'kills_t1: {kills_t1}\n')
            f.write(f'kills_t2: {kills_t2}\n')
