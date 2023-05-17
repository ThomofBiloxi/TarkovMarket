#Tarkov Market App

This repository contains the source code for the Tarkov Market App. The app allows you to browse and search for items from the game Escape from Tarkov.
Installation

##Installation

To use the Tarkov Market App, follow the steps below:

###Clone the Repository: Start by cloning this repository to your local machine using the following command:

git clone [https://github.com/your-username/tarkov-market-app.git](https://github.com/ThomofBiloxi/TarkovMarket.git)

Install Dependencies:

pip install -r requirements.txt

Generate the Executable:

    Open the main.spec file in a text editor.
    Replace the pathex value with the actual path to the directory where your Python files are located. For example, pathex=['/path/to/your/project'].
    Ensure that the datas section includes the necessary Python files. In the provided main.spec, the datas section includes 'items_db.py' and 'tarkov_market.py'.

Open a terminal or command prompt and navigate to the project directory. Run the following command to generate the executable:

pyinstaller main.spec

Obtain the Executable:
After the PyInstaller process finishes successfully, find the generated executable file (Tarkov_Market.exe) in the dist directory. Copy it to a suitable location on your computer.

Run the App:
Double-click on the Tarkov_Market.exe file to launch the Tarkov Market App. The app window will open, allowing you to browse and search for items from Escape from Tarkov.
