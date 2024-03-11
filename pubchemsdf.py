import os
import requests

def print_green(text):
    print("\033[92m {}\033[00m" .format(text))

def display_intro():
    print_green("""
              
  _____       _      _____ _                      ____  _____     _____ _____  ______   _____                      _                 _           
 |  __ \     | |    / ____| |                    |___ \|  __ \   / ____|  __ \|  ____| |  __ \                    | |               | |          
 | |__) |   _| |__ | |    | |__   ___ _ __ ___     __) | |  | | | (___ | |  | | |__    | |  | | _____      ___ __ | | ___   __ _  __| | ___ _ __ 
 |  ___/ | | | '_ \| |    | '_ \ / _ \ '_ ` _ \   |__ <| |  | |  \___ \| |  | |  __|   | |  | |/ _ \ \ /\ / / '_ \| |/ _ \ / _` |/ _` |/ _ \ '__|
 | |   | |_| | |_) | |____| | | |  __/ | | | | |  ___) | |__| |  ____) | |__| | |      | |__| | (_) \ V  V /| | | | | (_) | (_| | (_| |  __/ |   
 |_|    \__,_|_.__/ \_____|_| |_|\___|_| |_| |_| |____/|_____/  |_____/|_____/|_|      |_____/ \___/ \_/\_/ |_| |_|_|\___/ \__,_|\__,_|\___|_|   
                                                                                                                                                 
                                                                                                                                                 
""")
    print("PubChem 3D Conformer SDF File Downloader")
    print("Version: 1.00.001")
    print("Developer: Manav Choudhary")
    print("Description: Downloads SDF files of molecules with provided names from a text file to a particular location to be set by the user.")
    print("\n")

def download_sdf(pubchem_id, save_folder):
    url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/CID/{pubchem_id}/record/SDF/?record_type=3d"
    response = requests.get(url)
    if response.status_code == 200:
        with open(os.path.join(save_folder, f"{pubchem_id}.sdf"), 'wb') as f:
            f.write(response.content)
        print(f"Downloaded SDF file for CID {pubchem_id} successfully.")
    else:
        print(f"Failed to download SDF file for CID {pubchem_id}.")

def search_and_download(names_file, save_folder):
    with open(names_file, 'r') as file:
        chemical_names = file.readlines()
    
    for name in chemical_names:
        name = name.strip()  # Remove leading/trailing whitespace and newline characters
        url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{name}/cids/JSON?name_type=word"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if 'IdentifierList' in data:
                cid = data['IdentifierList']['CID'][0]
                download_sdf(cid, save_folder)
            else:
                print(f"No CID found for chemical {name}.")
        else:
            print(f"Failed to search for chemical {name}.")

if __name__ == "__main__":
    display_intro()
    names_file = input("Enter the path to the text file containing chemical names: ")
    save_folder = input("Enter the path to the folder where you want to save SDF files: ")
    search_and_download(names_file, save_folder)


    
