import os
import subprocess

def print_green(text):
    print("\033[92m {}\033[00m" .format(text))

def display_intro():
    print_green("""           

              _     _   _    _           _                            
     /\      | |   | | | |  | |         | |                           
    /  \   __| | __| | | |__| |_   _  __| |_ __ ___   __ _  ___ _ __  
   / /\ \ / _` |/ _` | |  __  | | | |/ _` | '__/ _ \ / _` |/ _ \ '_ \ 
  / ____ \ (_| | (_| | | |  | | |_| | (_| | | | (_) | (_| |  __/ | | |
 /_/    \_\__,_|\__,_| |_|  |_|\__, |\__,_|_|  \___/ \__, |\___|_| |_|
                                __/ |                 __/ |           
                               |___/                 |___/                                                                                                  
                                                                                       
""")
    print("Add Hydrogen Tool")
    print("Version: 1.00.001")
    print("Developer: Manav Choudhary")
    print("Description: Adds hydrogen atoms to SDF files and converts them to PDB format.")
    print("\n")

def add_hydrogen_to_sdf(sdf_folder):
    added_hydrogen_folder = os.path.join(sdf_folder, "Added Hydrogen SDF")
    os.makedirs(added_hydrogen_folder, exist_ok=True)

    sdf_files = [file for file in os.listdir(sdf_folder) if file.endswith(".sdf")]

    for sdf_file in sdf_files:
        sdf_path = os.path.join(sdf_folder, sdf_file)
        pdb_file = sdf_file.replace(".sdf", ".pdb")
        pdb_path = os.path.join(added_hydrogen_folder, pdb_file)

        # Launch PyMOL and add hydrogen atoms
        command = [r"C:\ProgramData\pymol\PyMOLWin.exe", "-cq", "-d", f"load {sdf_path}, molecule; h_add; save {pdb_path}, molecule"]
        subprocess.run(command)

if __name__ == "__main__":
    display_intro()
    sdf_folder = input("Enter the path to the folder where SDF files are saved: ")
    confirm = input("Are you sure you want to add hydrogen to all molecules? (Y/N): ").strip().lower()
    if confirm == "y":
        add_hydrogen_to_sdf(sdf_folder)
