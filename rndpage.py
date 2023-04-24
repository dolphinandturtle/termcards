from random import randint
import os


# Misc
def clear_buffer():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")

clear_buffer()

# Read profiles
profiles = [path[:-5] for path in os.listdir() if ".prof" == path[-5:]]

# Prompt profiles
is_picking_profiles = True
selected_profile = ""
while is_picking_profiles:

    profile_table = [f"{n}) {p}" for n, p in enumerate(profiles)]
    print("# PROFILES #")
    print(*profile_table, sep="\n")
    separator = ['#'] * (max([len(p) for p in profiles]) + 3) \
        if profiles else ''
    print(*separator, sep="", end="\n\n")

    profile_command = input("Profile: ").split(' ')

    if profile_command[0] == "new" and len(profile_command) == 2:
        with open(f"{profile_command[1]}.prof", 'a') as file:
            pass
        selected_profile = profile_command[1]
        is_picking_profiles = False
        print("New profile!")
    if len(profile_command) == 1 and profile_command[0].isnumeric() and \
       int(profile_command[0]) < len(profiles):
        is_picking_profiles = False
        selected_profile = profiles[int(profile_command[0])]
        print("Reloaded profile!")
    clear_buffer()

# Prompt data file
data_file = f"{selected_profile}.prof"
with open(data_file, "r") as file:
    lines = file.read().split("\n")[:-1]
page_range = ''
while True:
    print("Page Range", end='')
    if not lines:
        print(" (Required)", end='')
    page_range = input(": ")
    if page_range.isnumeric():
        with open(data_file, "w") as file:
            file.write(f"range:{page_range}\n")
        break
    if lines:
        break
    clear_buffer()

# Random sort
with open(data_file, "r") as file:
    lines = file.read().split('\n')[:-1]
    if lines[0][:6] == "range:":
        page_range = int(lines[0][6:])
page = randint(1, int(lines[0][6:]))

# Save
with open(data_file, "r+") as file:
    cached = {int(val) for val in file.read().split('\n')[1:-1]}
    while True:
        # Mark as complete
        if cached == {*range(1, page_range+1)}:
            print("Termine! These cards have been completed!")
            break
        while True:
            page = randint(1, page_range)
            if int(page) not in cached:
                print(f"[{len(cached)}/{page_range}] {page}", end=" ")
                break
        game_input = input("")
        if game_input == "y":
            file.write(str(page) + '\n')
            cached.add(page)
        if game_input == "stop":
            break
    clear_buffer()
