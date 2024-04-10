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
from bs4 import BeautifulSoup
import requests
import time
import pandas as pd
from tqdm import tqdm

def print_green(text):
    print("\033[92m {}\033[00m" .format(text))

def display_intro():
    print_green("""   
 ______  __       __  _______   _______    ______  ________        _______              __                __                                     
|      \|  \     /  \|       \ |       \  /      \|        \      |       \            |  \              |  \                                    
 \$$$$$$| $$\   /  $$| $$$$$$$\| $$$$$$$\|  $$$$$$\\$$$$$$$$      | $$$$$$$\  ______  _| $$_     ______  | $$____    ______    _______   ______  
  | $$  | $$$\ /  $$$| $$__/ $$| $$__/ $$| $$__| $$  | $$         | $$  | $$ |      \|   $$ \   |      \ | $$    \  |      \  /       \ /      \ 
  | $$  | $$$$\  $$$$| $$    $$| $$    $$| $$    $$  | $$         | $$  | $$  \$$$$$$\\$$$$$$    \$$$$$$\| $$$$$$$\  \$$$$$$\|  $$$$$$$|  $$$$$$|
  | $$  | $$\$$ $$ $$| $$$$$$$ | $$$$$$$ | $$$$$$$$  | $$         | $$  | $$ /      $$ | $$ __  /      $$| $$  | $$ /      $$ \$$    \ | $$    $$
 _| $$_ | $$ \$$$| $$| $$      | $$      | $$  | $$  | $$         | $$__/ $$|  $$$$$$$ | $$|  \|  $$$$$$$| $$__/ $$|  $$$$$$$ _\$$$$$$\| $$$$$$$$
|   $$ \| $$  \$ | $$| $$      | $$      | $$  | $$  | $$         | $$    $$ \$$    $$  \$$  $$ \$$    $$| $$    $$ \$$    $$|       $$ \$$     |
 \$$$$$$ \$$      \$$ \$$       \$$       \$$   \$$   \$$          \$$$$$$$   \$$$$$$$   \$$$$   \$$$$$$$ \$$$$$$$   \$$$$$$$ \$$$$$$$   \$$$$$$$
                                                                                                                                                                                    
    """)
    print("ResHelp Tools")
    print("Version: 1.05")
    print("Developer: Manav Choudhary")
    print("Description: Collection of tools to help researchers in their work")
    print("\n")

def fetch_data(url, retry_limit=3):
    retry_count = 0
    while retry_count < retry_limit:
        try:
            # Fetch HTML content from the URL
            response = requests.get(url)
            if response.status_code == 200:
                return response.content
            else:
                print("Failed to fetch data from URL:", url)
                return None
        except requests.ConnectionError:
            print("Connection error occurred. Retrying...")
            retry_count += 1
            time.sleep(5)  # Wait for a few seconds before retrying

    print(f"Failed to fetch data from URL after {retry_limit} retries:", url)
    return None

def parse_table(html_content):
    # Parse HTML content and extract tabular data
    soup = BeautifulSoup(html_content, 'html.parser')
    tables = soup.find_all('table')  # Find all tables in the HTML content
    if tables:
        for table in tables:
            rows = table.find_all('tr')
            if rows:
                data = []
                for row in rows[1:]:
                    cols = row.find_all('td')
                    data.append([col.get_text(strip=True) for col in cols])
                return data
        print("No table with tabular data found in the HTML content.")
        return None
    else:
        print("No tables found in the HTML content.")
        return None

def save_to_file(data, filename, headings, output_format='text'):
    if output_format == 'text':
        # Calculate column widths
        col_widths = [max(len(str(item)) for item in col) for col in zip(*data)]

        # Save data to a text file
        with open(filename, 'w') as f:
            # Write table headings
            f.write(' | '.join(headings) + '\n')

            # Write separator line
            f.write('-' * (sum(col_widths) + len(col_widths) * 3 - 1) + '\n')

            # Write table rows
            for row in data[1:]:
                f.write(' | '.join(str(item).ljust(width) for item, width in zip(row, col_widths)) + '\n')

        print("Data saved to", filename)
    elif output_format == 'excel':
        # Create DataFrame from the table data
        df = pd.DataFrame(data[1:], columns=headings)

        # Create ExcelWriter instance
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            # Write DataFrame to Excel
            df.to_excel(writer, index=False, sheet_name='Sheet1')
            # Create a new sheet
            writer.book.create_sheet('Sheet2')
            # Save the Excel file
            writer.book.save(filename)  # Corrected line

        print("Data saved to", filename)
    else:
        print("Invalid output format. Please choose either 'text' or 'excel'.")

def get_output_path():
    while True:
        output_path = input("Enter the path where the output file should be saved (e.g., /path/to/save): ")
        if os.path.isdir(output_path):
            return output_path
        else:
            print("Invalid path. Please enter a valid directory path.")

def get_output_format():
    while True:
        output_format = input("Enter the output format (text/excel): ").lower()
        if output_format in ['text', 'excel']:
            return output_format
        else:
            print("Invalid output format. Please enter either 'text' or 'excel'.")

def get_output_extension(output_format):
    if output_format == 'text':
        return 'txt'
    elif output_format == 'excel':
        return 'xlsx'
    else:
        return None

def parse_table_phytochem(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    table = soup.find('table', {'class': 'phytochem'})
    if table:
        table_data = []
        rows = table.find_all('tr')
        for row in rows[1:]:  # Skip header row
            cols = row.find_all('td')
            phytochemical_name = cols[3].text.strip()  # Extract phytochemical name
            table_data.append(phytochemical_name)
        return table_data
    else:
        print("No table found in the HTML content.")
        return None

def pull_plant_phytochemicals():
    input_path = input("Enter the path of the text file containing plant names: ")
    if not os.path.exists(input_path):
        print("File not found.")
        return

    try:
        # Read the text file containing plant names
        with open(input_path, 'r') as f:
            plant_names = f.read().splitlines()

        # Fetch and parse data for each plant
        all_phytochemicals = set()
        progress_bar = tqdm(total=len(plant_names), desc="Progress", unit="plant")

        for plant_name in plant_names:
            url = f"https://cb.imsc.res.in/imppat/phytochemical/{plant_name.replace(' ', '%20')}"
            html_content = fetch_data(url)

            if html_content:
                table_data = parse_table_phytochem(html_content)
                if table_data:
                    all_phytochemicals.update(table_data)  # Add phytochemical names to set

            progress_bar.update(1)  # Update progress bar

        progress_bar.close()

        # Save the list of phytochemicals into a text file
        output_path = input("Enter the path where the output file should be saved (e.g., /path/to/save): ")
        output_filename = input("Enter the name of the output file: ") + ".txt"

        with open(os.path.join(output_path, output_filename), 'w') as f:
            for phytochemical in all_phytochemicals:
                f.write(f"{phytochemical}\n")

        print("Data saved to", os.path.join(output_path, output_filename))

    except Exception as e:
        print("Error:", e)

def go_back():
    return input("Press Enter to go back...")

def main():
    display_intro()
    url = None
    
    while True:
        print("Browse")
        print("1. Phytochemical Associations")
        print("2. Therapeutic Use")
        print("3. Pull Plant Phytochemicals")
        print("4. Return to ResHelp Tools")
        print("5. Exit")
        browse_option = input("Enter your choice: ")

        if browse_option == '1':
            print("Enter:")
            print("1. Indian Medicinal Plant")
            print("2. Phytochemical")
            print("3. Chemical Superclass")
            print("4. Go back")
            enter_option = input("Enter your choice: ")

            if enter_option == '1':
                headings = ["Indian medicinal plant", "Plant part", "IMPPAT Phytochemical identifier", "Phytochemical name", "References"]
                plant_name = input("Enter the name of the Indian Medicinal Plant: ")
                url = f"https://cb.imsc.res.in/imppat/phytochemical/{plant_name.replace(' ', '%20')}"
                filename = f"{plant_name}_phytochemical_associations.txt"
            elif enter_option == '2':
                headings = ["Indian medicinal plant", "Plant part", "IMPPAT Phytochemical identifier", "Phytochemical name", "References"]
                phytochemical_name = input("Enter the name of the Phytochemical: ")
                url = f"https://cb.imsc.res.in/imppat/phytochemicalplants/{phytochemical_name.replace(' ', '%20')}"
                filename = f"{phytochemical_name}_phytochemical_associations.txt"
            elif enter_option == '3':
                headings = ["Indian medicinal plant", "Plant part", "IMPPAT Phytochemical identifier", "Phytochemical name", "References"]
                chemical_superclass = input("Enter the name of the Chemical Superclass: ")
                url = f"https://cb.imsc.res.in/imppat/phytochemical-searchsupclass/{chemical_superclass.replace(' ', '%20')}"
                filename = f"{chemical_superclass}_phytochemical_associations.txt"
            elif enter_option == '4':
                go_back()
                continue
            else:
                print("Invalid option selected.")
                continue

        elif browse_option == '2':
            print("Enter:")
            print("1. Indian Medicinal Plant")
            print("2. Condition")
            print("3. Go back")
            enter_option = input("Enter your choice: ")

            if enter_option == '1':
                headings = ["Indian medicinal plant", "Plant part", "Therapeutic use", "Therapeutic use identifiers", "References"]
                plant_name = input("Enter the name of the Indian Medicinal Plant: ")
                url = f"https://cb.imsc.res.in/imppat/therapeutics/{plant_name.replace(' ', '%20')}"
                filename = f"{plant_name}_therapeutic_use.txt"
            elif enter_option == '2':
                headings = ["Indian medicinal plant", "Plant part", "Therapeutic use", "Therapeutic use identifiers", "References"]
                condition_name = input("Enter the name of the Condition: ")
                url = f"https://cb.imsc.res.in/imppat/therapeuticsplants/{condition_name.replace(' ', '%20')}"
                filename = f"{condition_name}_therapeutic_use.txt"
            elif enter_option == '3':
                go_back()
                continue
            else:
                print("Invalid option selected.")
                continue
                
        elif browse_option == '3':
            pull_plant_phytochemicals()

        elif browse_option == '4':
            os.system("python3 ../main.py")

        elif browse_option == '5':
            print("Exiting...")
            break

        else:
            print("Invalid option selected.")
            continue

        if url:  # Check if url is not None before fetching data
            html_content = fetch_data(url)
            if html_content:
                table_data = parse_table(html_content)
                if table_data:
                    output_format = get_output_format()
                    if output_format:
                        output_extension = get_output_extension(output_format)
                        if output_extension:
                            output_path = get_output_path()
                            if output_path:
                                filename = input("Enter the name of the output file: ")
                                filename += f".{output_extension}"
                                save_to_file(table_data, os.path.join(output_path, filename), headings, output_format)

if __name__ == "__main__":
    main()