import os


def get_top_tier1_kills(subfolder_path):
    # Get a list of all .txt files in the subfolder
    files = [file for file in os.listdir(subfolder_path) if file.endswith(".txt")]

    # Dictionary to store the kill numbers for each UUID for tier 1
    kill_numbers_tier1 = {}

    # Iterate over each file
    for file in files:
        # Extract the UUID from the filename
        uuid = file.replace(".txt", "")

        # Read the contents of the file
        with open(os.path.join(subfolder_path, file), "r") as f:
            contents = f.read()

        # Extract the kill number for tier 1
        tier1_start = contents.index("kills_t1: ") + len("kills_t1: ")
        tier1_end = contents.index("\n", tier1_start)
        tier1_kills = int(contents[tier1_start:tier1_end])

        # Store the kill number for tier 1 in the dictionary
        kill_numbers_tier1[uuid] = tier1_kills

    # Sort the kill numbers for tier 1 in descending order
    sorted_kills_tier1 = sorted(kill_numbers_tier1.items(), key=lambda x: x[1], reverse=True)

    # Get the top 5 kills for tier 1
    top_5_kills_tier1 = sorted_kills_tier1[:5]

    # Store the top 5 kills for tier 1 in the desired format
    result_tier1 = [f"{uuid}: {kill}" for uuid, kill in top_5_kills_tier1]

    return result_tier1


def get_top_tier2_kills(subfolder_path):
    # Get a list of all .txt files in the subfolder
    files = [file for file in os.listdir(subfolder_path) if file.endswith(".txt")]

    # Dictionary to store the kill numbers for each UUID for tier 2
    kill_numbers_tier2 = {}

    # Iterate over each file
    for file in files:
        # Extract the UUID from the filename
        uuid = file.replace(".txt", "")

        # Read the contents of the file
        with open(os.path.join(subfolder_path, file), "r") as f:
            contents = f.read()

        # Extract the kill number for tier 2
        tier2_start = contents.index("kills_t2: ") + len("kills_t2: ")
        tier2_end = contents.index("\n", tier2_start)
        tier2_kills = int(contents[tier2_start:tier2_end])

        # Store the kill number for tier 2 in the dictionary
        kill_numbers_tier2[uuid] = tier2_kills

    # Sort the kill numbers for tier 2 in descending order
    sorted_kills_tier2 = sorted(kill_numbers_tier2.items(), key=lambda x: x[1], reverse=True)

    # Get the top 5 kills for tier 2
    top_5_kills_tier2 = sorted_kills_tier2[:5]

    # Store the top 5 kills for tier 2 in the desired format
    result_tier2 = [f"{uuid}: {kill}" for uuid, kill in top_5_kills_tier2]

    return result_tier2


def get_top_total_kills(subfolder_path):
    # Get a list of all .txt files in the subfolder
    files = [file for file in os.listdir(subfolder_path) if file.endswith(".txt")]

    # Dictionary to store the kill numbers for each UUID for tier 1 and tier 2
    kill_numbers_tier1 = {}
    kill_numbers_tier2 = {}

    # Iterate over each file
    for file in files:
        # Extract the UUID from the filename
        uuid = file.replace(".txt", "")

        # Read the contents of the file
        with open(os.path.join(subfolder_path, file), "r") as f:
            contents = f.read()

        # Extract the kill numbers for tier 1 and tier 2
        tier1_start = contents.index("kills_t1: ") + len("kills_t1: ")
        tier1_end = contents.index("\n", tier1_start)
        tier1_kills = int(contents[tier1_start:tier1_end])

        tier2_start = contents.index("kills_t2: ") + len("kills_t2: ")
        tier2_end = contents.index("\n", tier2_start)
        tier2_kills = int(contents[tier2_start:tier2_end])

        # Store the kill numbers for tier 1 and tier 2 in the respective dictionaries
        kill_numbers_tier1[uuid] = tier1_kills
        kill_numbers_tier2[uuid] = tier2_kills

    # Calculate the total kills for tier 1 and tier 2
    total_kills = {uuid: kill_numbers_tier1.get(uuid, 0) + kill_numbers_tier2.get(uuid, 0) for uuid in
                   set(kill_numbers_tier1) | set(kill_numbers_tier2)}

    # Sort the total kills in descending order
    sorted_total_kills = sorted(total_kills.items(), key=lambda x: x[1], reverse=True)

    # Get the top 5 total kills
    top_5_total_kills = sorted_total_kills[:5]

    # Store the top 5 total kills in the desired format
    result_total = [f"{uuid}: {kill}" for uuid, kill in top_5_total_kills]

    return result_total
