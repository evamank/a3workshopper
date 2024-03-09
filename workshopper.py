import os
from bs4 import BeautifulSoup
import requests
from datetime import datetime
import subprocess
directory_path = 'linuxgsm/serverfiles'  # Replace with the actual path to your directory
addons_to_update = []
# Get a list of all files in the directory
all_files = os.listdir(directory_path)

# Loop through each file
for file_name in all_files:
    # Check if the file starts with the character '@'
    if file_name.startswith('@'):
        # Create the full path to the meta.cpp file
        meta_file_path = os.path.join(directory_path, file_name, 'meta.cpp')

        # Check if the meta.cpp file exists
        if os.path.exists(meta_file_path):
            # Read the contents of the meta.cpp file
            with open(meta_file_path, 'r') as meta_file:
                meta_content = meta_file.readlines()

            # Extract the published ID (assuming it is on the second line)
            if len(meta_content) >= 2:
                published_id_line = meta_content[1].strip()
                key, published_id = published_id_line.split('=')
                published_id = published_id.strip(';').strip()

                # published id yea
                # Putting id at the end of workshop url, loop should start here
                ur = "https://steamcommunity.com/sharedfiles/filedetails/?id="
                url = ur + published_id
                r = requests.get(url).text
                soup = BeautifulSoup(r, "lxml")

                # Fetching update date
                date = soup.find_all('div', {'class': 'detailsStatRight'})
                date_str = [element.get_text() for element in date[1:3]]
                update_date = date_str[1]

                # Input string
               #datey = str(update_date)
                date_string = update_date

                if len(update_date) > 16:
                    input_date_str = update_date
                    formatted_date = datetime.strptime(date_string, '%d %b, %Y @ %I:%M%p').strftime('%d:%m:%Y')
                    stored_date = formatted_date
                    # file creation time
                    creation_time = os.path.getctime(meta_file_path)

                    # Convert creation time to a datetime object
                    creation_date = datetime.utcfromtimestamp(creation_time)

                    # Format the datetime object as dd:mm:yyyy
                    formatted_creation_date = creation_date.strftime('%d:%m:%Y')

                    # Compare stored date with file creation date
                    stored_date_object = datetime.strptime(stored_date, '%d:%m:%Y')
                    file_date_object = datetime.strptime(formatted_creation_date, '%d:%m:%Y')
                else:
                    current_year = datetime.now().year
                    full_date_string = f"{date_string} {current_year}"
                    # formatted date / stored date is the workshop updatedate
                    date_object = datetime.strptime(full_date_string, "%d %b @ %I:%M%p %Y")
                    formatted_date = date_object.strftime("%d:%m:%Y")
                    stored_date = formatted_date

                    # file creation time
                    creation_time = os.path.getctime(meta_file_path)

                    # Convert creation time to a datetime object
                    creation_date = datetime.utcfromtimestamp(creation_time)

                    # Format the datetime object as dd:mm:yyyy
                    formatted_creation_date = creation_date.strftime('%d:%m:%Y')

                    # Compare stored date with file creation date
                    stored_date_object = datetime.strptime(stored_date, '%d:%m:%Y')
                    file_date_object = datetime.strptime(formatted_creation_date, '%d:%m:%Y')
                if file_date_object > stored_date_object:
                    print(f"Addon {file_name} is up to date")
                elif file_date_object < stored_date_object:
                    print(f"Addon {file_name} Requires Update.") # Add addon to the list
                    addons_to_update.append(file_name)
if addons_to_update:
    print(f"please update {addons_to_update}")
else:
    print("Running server")
    # Run the shell script
    shell_script_path = "./tmuxhost.sh"
    try:
        subprocess.run(["bash", shell_script_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running the shell script: {e}")



