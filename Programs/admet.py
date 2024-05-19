import requests
import pandas as pd
import time
from tqdm import tqdm

def get_admet_data(smiles):
    url = "https://admetlab3.scbdd.com/api/admet/"
    headers = {'Content-Type': 'application/json'}
    payload = {'smiles': smiles}
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for SMILES '{smiles}': {e}")
        return None

def main():
    smiles_file = input("Enter the path to the text file containing Canonical SMILES: ")
    output_csv = input("Enter the path where the CSV file should be stored: ")

    try:
        with open(smiles_file, 'r') as file:
            smiles_list = [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        print(f"The file {smiles_file} was not found.")
        return
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        return

    data = []
    for smiles in tqdm(smiles_list, desc="Processing SMILES"):
        result = get_admet_data(smiles)
        if result:
            data.append(result)
        time.sleep(0.2)  # To prevent hitting the rate limit

    if data:
        try:
            df = pd.DataFrame(data)
            df.to_csv(output_csv, index=False)
            print(f"Results have been saved to {output_csv}")
        except Exception as e:
            print(f"An error occurred while saving the CSV file: {e}")
    else:
        print("No data was retrieved.")

if __name__ == "__main__":
    main()
