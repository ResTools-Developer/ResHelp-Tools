# ResHelp Tools

![ResHelp Tools Logo](reshelp_tools_logo.png)

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

## Requirements

- Python 3.x
- Requests library (install via `pip install requests`)

## Usage

1. Clone the repository to your local machine:

    ```bash
    git clone https://github.com/your-username/reshelp-tools.git
    ```

2. Navigate to the project directory:

    ```bash
    cd reshelp-tools
    ```

3. Run the main tool:

    ```bash
    python main.py
    ```

4. Follow the on-screen instructions to choose the tool and proceed with the desired functionality.

## Tools

### 1. SDF 3D Conformer Downloader

- PubChem 3D Conformer SDF File Downloader is a Python-based tool that allows users to download SDF (Structure Data File) files of chemical molecules from PubChem. The tool provides two options for inputting chemical names: either manually entering the names or uploading a .txt file containing the names. It then searches for the PubChem Compound ID (CID) for each chemical name and downloads the corresponding 3D conformer SDF file.

## Contributors

- Manav Choudhary (@manavchoudhary)

## License

This project is licensed under the [MIT License](LICENSE).

---

Feel free to customize the README according to your project specifics, such as adding installation instructions, usage examples, or additional features. You can also include screenshots or additional visual elements to enhance the documentation.