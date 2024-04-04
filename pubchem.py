#HariOm
import os
import requests
import time
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor
from tenacity import retry, retry_if_exception_type, wait_exponential, stop_after_attempt
import speedtest

MAX_RETRIES = 20
RETRY_DELAY = 3  # Delay between retries in seconds
MAX_CONCURRENT_REQUESTS = 10 # Maximum number of concurrent requests
THROTTLING_DELAY = 0.2  # Delay between each concurrent request in seconds


def print_green(text):
    print("\033[92m {}\033[00m" .format(text))

def display_intro():
    print_green("""
              
  _______             __         ______   __                                      _______              __                __                                     
|       \           |  \       /      \ |  \                                    |       \            |  \              |  \                                    
| $$$$$$$\ __    __ | $$____  |  $$$$$$\| $$____    ______   ______ ____        | $$$$$$$\  ______  _| $$_     ______  | $$____    ______    _______   ______  
| $$__/ $$|  \  |  \| $$    \ | $$   \$$| $$    \  /      \ |      \    \       | $$  | $$ |      \|   $$ \   |      \ | $$    \  |      \  /       \ /      \ 
| $$    $$| $$  | $$| $$$$$$$\| $$      | $$$$$$$\|  $$$$$$\| $$$$$$\$$$$\      | $$  | $$  \$$$$$$\\$$$$$$    \$$$$$$\| $$$$$$$\  \$$$$$$\|  $$$$$$$|  $$$$$$|
| $$$$$$$ | $$  | $$| $$  | $$| $$   __ | $$  | $$| $$    $$| $$ | $$ | $$      | $$  | $$ /      $$ | $$ __  /      $$| $$  | $$ /      $$ \$$    \ | $$    $$
| $$      | $$__/ $$| $$__/ $$| $$__/  \| $$  | $$| $$$$$$$$| $$ | $$ | $$      | $$__/ $$|  $$$$$$$ | $$|  \|  $$$$$$$| $$__/ $$|  $$$$$$$ _\$$$$$$\| $$$$$$$$
| $$       \$$    $$| $$    $$ \$$    $$| $$  | $$ \$$     \| $$ | $$ | $$      | $$    $$ \$$    $$  \$$  $$ \$$    $$| $$    $$ \$$    $$|       $$ \$$     
 \$$        \$$$$$$  \$$$$$$$   \$$$$$$  \$$   \$$  \$$$$$$$ \$$  \$$  \$$       \$$$$$$$   \$$$$$$$   \$$$$   \$$$$$$$ \$$$$$$$   \$$$$$$$ \$$$$$$$   \$$$$$$$                                                                                                                                                             
                                                                                                                                                 
""")
    print("PubChem Structure File Downloader")
    print("Version: 1.05")
    print("Developer: Manav Choudhary")
    print("Description: Downloads Structure files of molecules with provided names from a text file to a particular location to be set by the user.")
    print("\n")

def measure_ping_speed():
    st = speedtest.Speedtest()
    st.get_best_server()
    return st.results.ping

def adjust_parameters():
    ping_speed = measure_ping_speed()
    # Adjust max concurrent requests and throttling delay based on ping speed
    if ping_speed < 60:
        MAX_CONCURRENT_REQUESTS = 20
        THROTTLING_DELAY = 0.1
    elif ping_speed < 100:
        MAX_CONCURRENT_REQUESTS = 15
        THROTTLING_DELAY = 0.2
    else:
        MAX_CONCURRENT_REQUESTS = 10
        THROTTLING_DELAY = 0.3

    return MAX_CONCURRENT_REQUESTS, THROTTLING_DELAY

def log_error(error_msg, log_file):
    with open(log_file, 'a') as f:
        f.write(error_msg + '\n')

def download_file(url, save_folder, filename, log_file):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(os.path.join(save_folder, filename), 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
        return True
    else:
        error_msg = f"Failed to download {filename}: {response.status_code} - {response.reason}"
        log_error(error_msg, log_file)
        response.raise_for_status()  # Raise an exception for non-200 responses

def search_and_download(names, save_folder, file_type):
    total_chemicals = len(names)
    downloaded_count = 0
    error_names = []
    start_time = time.time()

    log_file = os.path.join(save_folder, "download_errors.log")

    with tqdm(total=total_chemicals, desc="Downloading", unit="chemical") as pbar:
        with ThreadPoolExecutor(max_workers=MAX_CONCURRENT_REQUESTS) as executor:
            futures = []
            for name in names:
                name = name.strip()  # Remove leading/trailing whitespace and newline characters
                url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{name}/cids/JSON?name_type=word"
                future = executor.submit(download_and_track_progress, url, save_folder, file_type, pbar, log_file)
                futures.append(future)
                time.sleep(THROTTLING_DELAY)  # Introduce a delay between each concurrent request
            
            for future in futures:
                result = future.result()
                if result:
                    downloaded_count += 1
                else:
                    error_names.append(name)

    return error_names

@retry(retry=retry_if_exception_type(requests.HTTPError),
       wait=wait_exponential(multiplier=1, min=1, max=12),
       stop=stop_after_attempt(30))
def download_and_track_progress(url, save_folder, file_type, pbar, log_file):
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if 'IdentifierList' in data:
            cid = data['IdentifierList']['CID'][0]
            url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/CID/{cid}/record/{file_type}/?record_type=3d"
            if download_file(url, save_folder, f"{cid}.{file_type}", log_file):
                pbar.update(1)
                return True
    elif response.status_code == 503:
        for i in range(MAX_RETRIES, 0, -1):
            print(f"Server is busy. Retrying in {RETRY_DELAY} seconds. Retries left: {i}")
            time.sleep(RETRY_DELAY)
        print("Retrying now...")
    else:
        error_msg = f"Failed to download {file_type} file for {url}: {response.status_code} - {response.reason}"
        log_error(error_msg, log_file)
    return False

def process_option(option):
    if option == '1' or option == '2':
        save_folder = input("Enter the path to the folder where you want to DOWNLOAD files: ")
        file_type = input("Enter the file type you want to download (sdf, json, xml, asnt): ")
        if file_type.lower() not in ['sdf', 'json', 'xml', 'asnt']:
            print("Invalid file type specified.")
            return None
        if option == '1':
            chemicals = []
            print("Enter names of chemicals (press Enter twice to finish): ")
            while True:
                chemical = input().strip()
                if not chemical:
                    break
                chemicals.append(chemical)
        elif option == '2':
            names_file = input("Enter the path to the text file containing chemical names: ")
            with open(names_file, 'r') as file:
                chemicals = [line.strip() for line in file.readlines()]
        error_names = search_and_download(chemicals, save_folder, file_type)
        if error_names:
            with open(os.path.join(save_folder, "error_sdf.txt"), 'w') as error_file:
                error_file.write("\n".join(error_names))
        download_more = input("Do you want to download more files? (Y/N): ").strip().lower()
        if download_more == 'y':
            return option
        else:
            return 'return_to_main'
    elif option == '3':
        return 'return_to_main'
    elif option == '4':
        return 'exit'
    else:
        print("Invalid option. Please select a valid option.")
        return None

if __name__ == "__main__":
    display_intro()
    print("Options:")
    print("1. Enter names of chemicals")
    print("2. Upload .txt file with chemical names")
    print("3. Return to ResHelp Tools")
    print("4. Exit")
    option = input("Enter option number: ")
    while option:
        option = process_option(option)
        if option == 'return_to_main':
            os.system("python3 main.py")
        elif option == 'exit':
            print("Exiting...")
            exit()