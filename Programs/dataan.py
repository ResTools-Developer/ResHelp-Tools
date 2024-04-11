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
import glob
from tqdm import tqdm

def print_purple(text):
    print("\033[95m {}\033[00m" .format(text))

def display_intro():
    print_purple("""
 __                                  ______                       __                                         
|  \                                /      \                     |  \                                        
| $$       ______    ______        |  $$$$$$\ _______    ______  | $$ __    __   _______   ______    ______  
| $$      /      \  /      \       | $$__| $$|       \  |      \ | $$|  \  |  \ /       \ /      \  /      \ 
| $$     |  $$$$$$\|  $$$$$$\      | $$    $$| $$$$$$$\  \$$$$$$\| $$| $$  | $$|  $$$$$$$|  $$$$$$\|  $$$$$$\
| $$     | $$  | $$| $$  | $$      | $$$$$$$$| $$  | $$ /      $$| $$| $$  | $$ \$$    \ | $$    $$| $$   \$$
| $$_____| $$__/ $$| $$__| $$      | $$  | $$| $$  | $$|  $$$$$$$| $$| $$__/ $$ _\$$$$$$\| $$$$$$$$| $$      
| $$     \\$$    $$ \$$    $$      | $$  | $$| $$  | $$ \$$    $$| $$ \$$    $$|       $$ \$$     \| $$      
 \$$$$$$$$ \$$$$$$  _\$$$$$$$       \$$   \$$ \$$   \$$  \$$$$$$$ \$$ _\$$$$$$$ \$$$$$$$   \$$$$$$$ \$$      
                   |  \__| $$                                        |  \__| $$                              
                    \$$    $$                                         \$$    $$                              
                     \$$$$$$                                           \$$$$$$                               
                                                
    """)
    print("ResHelp Tools")
    print("Version: 1.05")
    print("Developer: Manav Choudhary")
    print("Description: Analyse log files after docking and display results for best docking poses")
    print("\n")

def get_log_directory():
    log_dir = input("Please enter the directory containing the log files: ")
    return log_dir

def parse_log_files(log_dir):
    results = []
    log_files = glob.glob(os.path.join(log_dir, '*.pdbqt_log.log'))
    for log_file in tqdm(log_files, desc="Parsing log files"):
        try:
            with open(log_file, 'r') as f:
                lines = f.readlines()
            cid = os.path.basename(log_file).split('.')[0]
            for line in lines:
                if line.strip().startswith('1'):
                    affinity = float(line.split()[1])
                    results.append((cid, affinity))
                    break
        except Exception as e:
            print(f"Error reading file {log_file}: {str(e)}")
    return results

def write_results(results, log_dir):
    results.sort(key=lambda x: x[1])
    output_file = os.path.join(log_dir, 'results.txt')
    col_widths = [15, 20]  # adjust column widths as needed
    try:
        with open(output_file, 'w') as f:
            f.write(' | '.join(str(item).ljust(width) for item, width in zip(["CID", "Affinity (kcal/mol)"], col_widths)) + '\n')
            f.write('='*40 + '\n')  # adjust as per your formatting needs
            for cid, affinity in results:
                f.write(' | '.join(str(item).ljust(width) for item, width in zip((cid, affinity), col_widths)) + '\n')
        print("Results written successfully to", output_file)
    except Exception as e:
        print(f"Error writing to file {output_file}: {str(e)}")

# usage
if __name__ == "__main__":
    display_intro()
    log_dir = get_log_directory()  # get directory from user
    results = parse_log_files(log_dir)
    write_results(results, log_dir)

