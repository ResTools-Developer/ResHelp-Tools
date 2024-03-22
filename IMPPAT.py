import os
from bs4 import BeautifulSoup
import requests
import pandas as pd

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
    print("Version: 1.00.001")
    print("Developer: Manav Choudhary")
    print("Description: Collection of tools to help researchers in their work")
    print("\n")

def fetch_data(url):
    # Fetch HTML content from the URL
    response = requests.get(url)
    if response.status_code == 200:
        return response.content
    else:
        print("Failed to fetch data from URL:", url)
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

def go_back():
    return input("Press Enter to go back...")

def main():
    display_intro()
    url = None
    
    while True:
        print("Browse")
        print("1. Phytochemical Associations")
        print("2. Therapeutic Use")
        print("3. Exit")
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