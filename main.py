#HariOm
import os
import sys

def print_red(text):
    print("\033[91m {}\033[00m" .format(text))

def display_intro():
    print_red("""
    /$$$$$$$                      /$$   /$$           /$$                 /$$$$$$$$                  /$$          
   | $$__  $$                    | $$  | $$          | $$                |__  $$__/                 | $$          
   | $$  \ $$  /$$$$$$   /$$$$$$$| $$  | $$  /$$$$$$ | $$  /$$$$$$          | $$  /$$$$$$   /$$$$$$ | $$  /$$$$$$$
   | $$$$$$$/ /$$__  $$ /$$_____/| $$$$$$$$ /$$__  $$| $$ /$$__  $$         | $$ /$$__  $$ /$$__  $$| $$ /$$_____/
   | $$__  $$| $$$$$$$$|  $$$$$$ | $$__  $$| $$$$$$$$| $$| $$  \ $$         | $$| $$  \ $$| $$  \ $$| $$|  $$$$$$ 
   | $$  \ $$| $$_____/ \____  $$| $$  | $$| $$_____/| $$| $$  | $$         | $$| $$  | $$| $$  | $$| $$ \____  $$
   | $$  | $$|  $$$$$$$ /$$$$$$$/| $$  | $$|  $$$$$$$| $$| $$$$$$$/         | $$|  $$$$$$/|  $$$$$$/| $$ /$$$$$$$/
   |__/  |__/ \_______/|_______/ |__/  |__/ \_______/|__/| $$____/          |__/ \______/  \______/ |__/|_______/ 
                                                          | $$                                                     
                                                          | $$                                                     
                                                          |__/                                                     
    """)
    print("ResHelp Tools")
    print("Version: 1.05")
    print("Developer: Manav Choudhary")
    print("Description: Collection of tools to help researchers in their work")
    print("\n")

def display_options():
    print("Available Tools:")
    print("1. PubChem Database")
    print("2. IMPPAT Databse")
    print("3. Add Hydrogen Tool")
    print("4. Docking Tools")
    print("5. Exit")
    print("\n")

def ask_for_tool_choice():
    while True:
        choice = input("Enter the serial number of the tool you want to use: ")
        if choice.isdigit():
            choice = int(choice)
            if choice == 1:
                os.system("python3 pubchem.py")
                break
            elif choice == 2:
                os.system("python3 IMPPAT.py")
                break
            elif choice == 3:
                os.system("python3 addh.py")
                break
            elif choice == 4:
                os.system("python3 docking.py")
                break
            elif choice == 5:
                print("Exiting...")
                sys.exit()
            else:
                print("Invalid choice. Please enter a valid serial number.")
        else:
            print("Invalid choice. Please enter a valid serial number.")


if __name__ == "__main__":
    display_intro()
    display_options()
    ask_for_tool_choice()
