# Tarkov Market App

This repository contains the source code for the Tarkov Market App. The app allows you to browse and search for items from the game Escape from Tarkov.
It utilizes the API provided by [tarkov-market](https://tarkov-market.com/)

## Installation

To compile the Tarkov Market App, follow the steps below.

If you prefer not to compile the app yourself, you can directly download the latest precompiled .exe file from the Releases section of this repository.

### Clone the Repository: 

Start by cloning this repository to your local machine using the following command:

    git clone https://github.com/ThomofBiloxi/TarkovMarket.git

### Install Dependencies:

    pip install -r requirements.txt

### Generate the Executable ([Pyinstaller](https://pyinstaller.org/en/stable/) recommended):

   Open the main.spec file in a text editor.
   Replace the pathex value with the actual path to the directory where your Python files are located. For example, pathex=['/path/to/your/project'].
   Ensure that the datas section includes the necessary Python files. In the provided main.spec, the datas section includes 'items_db.py' and 'tarkov_market.py'.

### Open a terminal or command prompt and navigate to the project directory. Run the following command to generate the executable:

    pyinstaller main.spec

### Obtain the Executable:

   After the PyInstaller process finishes successfully, find the generated executable file (Tarkov_Market.exe) in the dist directory. Copy it to a suitable location on your computer.

### Run the App:

   Double-click on the Tarkov_Market.exe file to launch the Tarkov Market App. The app window will open, allowing you to browse and search for items from Escape from Tarkov.

![image](https://github.com/ThomofBiloxi/TarkovMarket/assets/62316494/1508e7d3-bc6f-4ddc-8103-c95f358dad46)

![image](https://github.com/ThomofBiloxi/TarkovMarket/assets/62316494/81a43561-47f4-4ec3-8b7a-83ba19a6a155)

![image](https://github.com/ThomofBiloxi/TarkovMarket/assets/62316494/0d1dcfb2-02c5-4db4-af78-3c7e3ee9fbd8)
