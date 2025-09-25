# Image Perspective Correction App

## Overview
This App is a Python-based tool that allows you to save the locations of objects in images after correcting their perspective. The results are saved in a JSON file. 

## Installation
### Prerequisites
Ensure you have Python installed on your system. To check if Python is installed and determine its alias, run the following commands:

```sh
which python
which py
which python3
```

For most systems, the alias is `python3`.

### Setup
1. Create a virtual environment and install dependencies (instead of python3 use your alias):

   ```sh
   python3 -m venv venv
   . venv/bin/activate  # On macOS/Linux
   venv\bin\activate  # On Windows
   pip install -r requirements.txt
   ```

2. Start the application:

   ```sh
   python app.py
   ```

## Usage
1. **Configure Source and Destination**
  - Open `source_folders.json`.
  - Add the path to the folder containing the source images.
  - Add the path to the file where the object locations should be saved.

2. **Image Processing**
  - The app will prompt you to correct all images.
  - Click on the object, then insert the label.
  - When all the ojbects have been labeled click on "Save and Next" to proceed to the next image.
  - Repeat until all images are processed.

## Notes
- Ensure all required dependencies are installed before running the app.
