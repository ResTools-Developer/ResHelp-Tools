#HariOm
"""
Copyright 2024 Manav Amit Choudhary

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import os
import subprocess

def print_green(text):
    print("\033[92m {}\033[00m" .format(text))

def display_intro():
    print_green("""           
  ______         __        __        __    __                  __                                                   
 /      \       |  \      |  \      |  \  |  \                |  \                                                  
|  $$$$$$\  ____| $$  ____| $$      | $$  | $$ __    __   ____| $$  ______    ______    ______    ______   _______  
| $$__| $$ /      $$ /      $$      | $$__| $$|  \  |  \ /      $$ /      \  /      \  /      \  /      \ |       \ 
| $$    $$|  $$$$$$$|  $$$$$$$      | $$    $$| $$  | $$|  $$$$$$$|  $$$$$$\|  $$$$$$\|  $$$$$$\|  $$$$$$\| $$$$$$$\
| $$$$$$$$| $$  | $$| $$  | $$      | $$$$$$$$| $$  | $$| $$  | $$| $$   \$$| $$  | $$| $$  | $$| $$    $$| $$  | $$
| $$  | $$| $$__| $$| $$__| $$      | $$  | $$| $$__/ $$| $$__| $$| $$      | $$__/ $$| $$__| $$| $$$$$$$$| $$  | $$
| $$  | $$ \$$    $$ \$$    $$      | $$  | $$ \$$    $$ \$$    $$| $$       \$$    $$ \$$    $$ \$$     \| $$  | $$
 \$$   \$$  \$$$$$$$  \$$$$$$$       \$$   \$$ _\$$$$$$$  \$$$$$$$ \$$        \$$$$$$  _\$$$$$$$  \$$$$$$$ \$$   \$$
                                              |  \__| $$                              |  \__| $$                    
                                               \$$    $$                               \$$    $$                    
                                                \$$$$$$                                 \$$$$$$                                                                                  
""")
    print("Add Hydrogen Tool")
    print("Version: 1.05")
    print("Developer: Manav Choudhary")
    print("Description: Adds hydrogen atoms to SDF files and converts them to PDB format.")
    print("\n")

def add_hydrogen_to_sdf(sdf_folder):
    added_hydrogen_folder = os.path.join(sdf_folder, "Added Hydrogen SDF")
    os.makedirs(added_hydrogen_folder, exist_ok=True)

    sdf_files = [file for file in os.listdir(sdf_folder) if file.endswith(".sdf")]

    for sdf_file in sdf_files:
        sdf_path = os.path.join(sdf_folder, sdf_file)
        sdf_path_save = os.path.join(added_hydrogen_folder)

        # Launch PyMOL and add hydrogen atoms
        command = [r"C:\ProgramData\pymol\PyMOLWin.exe", "-cq", "-d", f"load {sdf_path}, molecule; h_add; save {sdf_path_save}, molecule"]
        subprocess.run(command)

if __name__ == "__main__":
    display_intro()
    sdf_folder = input("Enter the path to the folder where SDF files are saved: ")
    confirm = input("Are you sure you want to add hydrogen to all molecules? (Y/N): ").strip().lower()
    if confirm == "y":
        add_hydrogen_to_sdf(sdf_folder)
