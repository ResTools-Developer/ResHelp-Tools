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
import glob
import sys

def print_purple(text):
    print("\033[95m {}\033[00m" .format(text))

def display_intro():
    print_purple("""
 _______                       __        __                            ________                    __           
|       \                     |  \      |  \                          |        \                  |  \          
| $$$$$$$\  ______    _______ | $$   __  \$$ _______    ______         \$$$$$$$$______    ______  | $$  _______ 
| $$  | $$ /      \  /       \| $$  /  \|  \|       \  /      \          | $$  /      \  /      \ | $$ /       |
| $$  | $$|  $$$$$$\|  $$$$$$$| $$_/  $$| $$| $$$$$$$\|  $$$$$$\         | $$ |  $$$$$$\|  $$$$$$\| $$|  $$$$$$$
| $$  | $$| $$  | $$| $$      | $$   $$ | $$| $$  | $$| $$  | $$         | $$ | $$  | $$| $$  | $$| $$ \$$    \ 
| $$__/ $$| $$__/ $$| $$_____ | $$$$$$\ | $$| $$  | $$| $$__| $$         | $$ | $$__/ $$| $$__/ $$| $$ _\$$$$$$|
| $$    $$ \$$    $$ \$$     \| $$  \$$\| $$| $$  | $$ \$$    $$         | $$  \$$    $$ \$$    $$| $$|       $$
 \$$$$$$$   \$$$$$$   \$$$$$$$ \$$   \$$ \$$ \$$   \$$ _\$$$$$$$          \$$   \$$$$$$   \$$$$$$  \$$ \$$$$$$$ 
                                                      |  \__| $$                                                
                                                       \$$    $$                                                
                                                        \$$$$$$                                                 
    """)
    print("ResHelp Tools")
    print("Version: 1.05")
    print("Developer: Manav Choudhary")
    print("Description: Automated process of docking")
    print("\n")

def check_install_software():
    """Check if OpenBabel and AutoDock Vina are installed, if not, ask user before installing."""
    try:
        subprocess.run(["obabel", "-V"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        response = input("OpenBabel is not installed. Do you want to install it? (Y/N): ").strip().upper()
        if response == 'Y':
            print("Installing OpenBabel...")
            subprocess.run(["sudo", "apt", "install", "openbabel"])
        else:
            print("OpenBabel installation skipped.")

    try:
        subprocess.run(["vina", "--version"], check=True)
        subprocess.run(["vina_split", "--version"], check=True)
    except subprocess.CalledProcessError:
        response = input("AutoDock Vina is not installed1. Do you want to install it? (Y/N): ").strip().upper()
        if response == 'Y':
            print("Installing AutoDock Vina...")
            subprocess.run(["sudo", "apt", "install", "autodock-vina"])
        else:
            print("AutoDock Vina installation skipped.")

def ask_working_directory():
    """Ask user for working directory."""
    while True:
        directory = input("Enter the working directory where files are present: ").strip()
        if os.path.exists(directory):
            return directory
        else:
            print("The entered path does not exist. Please enter a valid path.")

def confirm_files_presence():
    """Ask user for confirmation of required files presence."""
    response = input("Are all required ligand and protein files present? (Y/N): ").strip().upper()
    return response == 'Y'

def energy_minimize(directory):
    os.chdir(directory)
    """Start the docking process."""
    input("Press Enter to start the docking process...")
    subprocess.run(["obminimize -ff MMFF94 -n 1000 *.sdf"], shell=True)

def convert_to_pdbqt(directory):
    os.chdir(directory)
    """Convert ligands to .pdbqt format."""
    response = input("Do you want to convert the energy minimized ligands to .pdbqt format? (Y/N): ").strip().upper()
    if response == 'Y':
        subprocess.run(["obabel -isdf *.sdf -opdbqt -O*.pdbqt"], shell=True)
        subprocess.run(["ls *.pdbqt > ligands.txt"], shell=True)

def start_docking(directory):
    os.chdir(directory)
    """Start the docking process."""
    response = input("Do you want to start the docking process? (Y/N): ").strip().upper()
    if response == 'Y':
        os.chdir(directory)
        subprocess.run(["perl", "vina_modified.pl"])
        os.makedirs("Log", exist_ok=True)
        os.makedirs("Output", exist_ok=True)
        subprocess.run("mv *.log Log", shell=True)

def split_output_files(directory):
    os.chdir(directory)
    """split output pdbqt files into docking poses"""
    response = input("Do you want to split the output files into docking poses? (Y/N): ").strip().upper()
    if response == 'Y':
        output_files = glob.glob("*_out.pdbqt")
        for output_file in output_files:
            subprocess.run(["vina_split", "--input", output_file])
        os.makedirs("01_Docking_Pose", exist_ok=True)
        os.makedirs("Other_Docking_Pose", exist_ok=True)
        os.makedirs("Input", exist_ok=True)
        os.makedirs("PDBQT", exist_ok=True)
        subprocess.run(["mv *_ligand_01.pdbqt 01_Docking_Pose"], shell=True)
        subprocess.run(["mv *_ligand_[0-9][0-9].pdbqt Other_Docking_Pose"], shell=True)
        subprocess.run(["mv *.sdf Input && mv protein.pdbqt Input"], shell=True)
        subprocess.run(["mv 01_Docking_Pose Output"], shell=True)
        subprocess.run(["mv Other_Docking_Pose Output"], shell=True)
        subprocess.run(["mv Log Output"], shell=True)
        subprocess.run(["mv *.pdbqt PDBQT"], shell=True)
        subprocess.run(["mv PDBQT Output"], shell=True)
   
def display_options():
    print("Available Actions:")
    print("1. Software Required")
    print("2. Change working directory")
    print("3. Minimize Energy of Ligand")
    print("4. Convert .sdf ligands to .pdbqt")
    print("5. Start docking process")
    print("6. Split output files")
    print("7. Return to ResHelp Tools")
    print("8. Exit")

    print("\n")

def ask_for_tool_choice():
    while True:
        print()
        choice = input("Enter the serial number of the action you want to perform (or 7 to exit): ")
        if choice.isdigit():
            choice = int(choice)
            if choice == 1:
                check_install_software()
            elif choice == 2:
                wd1 = ask_working_directory()
            elif choice == 3:
                if confirm_files_presence():
                    energy_minimize(wd1)
            elif choice == 4:
                convert_to_pdbqt(wd1)
            elif choice == 5:
                start_docking(wd1)
            elif choice == 6:
                split_output_files(wd1)
            elif choice == 7:
                os.system("python3 ../main.py")
            elif choice == 8:
                print("Exiting...")
                sys.exit()
            else:
                print("Invalid choice. Please enter a valid serial number.")
        else:
            print("Invalid choice. Please enter a valid serial number.")


if __name__ == "__main__":
    display_intro()
    while True:
        display_options()
        ask_for_tool_choice()