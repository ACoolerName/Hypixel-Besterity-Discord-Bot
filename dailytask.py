import os
import shutil
import sys    

# Add the parent folder to the Python path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "."))
sys.path.append(parent_dir)

# Define the paths to the input and output folders
input_folder = os.path.join(parent_dir, 'userkills')
daily_output_folder = os.path.join(parent_dir, 'dailykills')

def dailyrefresh():   
    # Delete all old files in the directory
    old_files = os.listdir(daily_output_folder)
    for file_name in old_files:
        file_path = os.path.join(daily_output_folder, file_name)
        os.remove(file_path)

    # Copy existing files from userkills to dailyoutput
    existing_files = os.listdir(input_folder)
    for file_name in existing_files:
        source_file_path = os.path.join(input_folder, file_name)
        destination_file_path = os.path.join(daily_output_folder, file_name)
        shutil.copy(source_file_path, destination_file_path)

def extract_kills_from_file(file_path):
    with open(file_path, "r") as f:
        contents = f.read()
    t1_start = contents.index("kills_t1: ") + len("kills_t1: ")
    t1_end = contents.index("\n", t1_start)
    t1_kills = int(contents[t1_start:t1_end])

    t2_start = contents.index("kills_t2: ") + len("kills_t2: ")
    t2_end = contents.index("\n", t2_start)
    t2_kills = int(contents[t2_start:t2_end])

    return t1_kills, t2_kills

def compare_t1_t2_kills():
    global input_folder
    global daily_output_folder
    daily_folder = daily_output_folder
    input_files = [file for file in os.listdir(input_folder) if file.endswith(".txt")]

    t1_diff = {}
    t2_diff = {}
    all_diff = {}

    for file in input_files:
        input_file_path = os.path.join(input_folder, file)
        daily_file_path = os.path.join(daily_folder, file)

        if not os.path.exists(daily_file_path):
            continue

        input_t1_kills, input_t2_kills = extract_kills_from_file(input_file_path)
        daily_t1_kills, daily_t2_kills = extract_kills_from_file(daily_file_path)

        t1_difference = input_t1_kills - daily_t1_kills
        t2_difference = input_t2_kills - daily_t2_kills
        all_difference = t1_difference + t2_difference

        filename = os.path.splitext(file)[0]

        t1_diff[filename] = t1_difference
        t2_diff[filename] = t2_difference
        all_diff[filename] = all_difference

    sorted_t1_diff = sorted(t1_diff.items(), key=lambda x: x[1], reverse=True)
    sorted_t2_diff = sorted(t2_diff.items(), key=lambda x: x[1], reverse=True)
    sorted_all_diff = sorted(all_diff.items(), key=lambda x: x[1], reverse=True)

    top_5_t1_diff = sorted_t1_diff[:5]
    top_5_t2_diff = sorted_t2_diff[:5]
    top_5_all_diff = sorted_all_diff[:5]

    result_t1 = [f"{uuid}: {kill}" for uuid, kill in top_5_t1_diff]
    result_t2 = [f"{uuid}: {kill}" for uuid, kill in top_5_t2_diff]
    result_all = [f"{uuid}: {kill}" for uuid, kill in top_5_all_diff]

    return result_t1, result_t2, result_all

# Example usage:
'result_t1, result_t2, result_all = compare_t1_t2_kills()'