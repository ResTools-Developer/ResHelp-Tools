# ResHelp Tools

![ResHelp Tools Logo](logo.png)

## Overview

ResHelp Tools is a collection of Python-based utilities designed to assist researchers in their work. The toolset includes functionalities for downloading SDF (Structure Data File) files of chemical molecules from PubChem, providing a user-friendly interface for ease of use.

## Features

### Main Tool (main.py)

- Provides an introduction to ResHelp Tools.
- Allows users to select from a list of available tools.
- Currently supports one tool: SDF 3D Conformer Downloader.

### SDF 3D Conformer Downloader (pubchemsdf.py)

- Downloads SDF files of molecules with provided names from a text file to a specified location.
- Supports two input options:
  - Manual entry of chemical names.
  - Upload of a .txt file containing chemical names.
- Downloads 3D conformer SDF files from PubChem for the specified chemicals.

### Adding Hydrogen to Molecules tool

- Asks user for location of SDF files
- In the software PyMOL, adds hydrogen to each molecule and saves the file in .pdb format
- Command used in PyMOL : h_add
- Location of PyMOL should be : C:\ProgramData\pymol\PyMOLWin.exe

## Requirements

- Python 3.8
- Requests library (install via `pip install requests`)

## Usage

1. Clone the repository to your local machine:

    ```bash
    git clone https://github.com/manavc-13/ResHelp-Tools.git
    ```

2. Navigate to the project directory:

    ```bash
    cd reshelp-tools
    ```

3. Run the main tool:

    ```bash
    python3.8 main.py
    ```

4. Follow the on-screen instructions to choose the tool and proceed with the desired functionality.

## Tools

### 1. SDF 3D Conformer Downloader

- PubChem 3D Conformer SDF File Downloader is a Python-based tool that allows users to download SDF (Structure Data File) files of chemical molecules from PubChem. The tool provides two options for inputting chemical names: either manually entering the names or uploading a .txt file containing the names. It then searches for the PubChem Compound ID (CID) for each chemical name and downloads the corresponding 3D conformer SDF file.

## Contributors

- Manav Choudhary (@manavc-13)

---