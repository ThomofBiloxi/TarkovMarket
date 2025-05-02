# utils.py
import sys
import os
try:
    import platformdirs # Import the library for user directories
    PLATFORMDIRS_AVAILABLE = True
except ImportError:
    PLATFORMDIRS_AVAILABLE = False
    print("Warning: 'platformdirs' library not found. Database will be stored in the script directory.")
    print("         Install using: pip install platformdirs")


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
        # print(f"Bundled mode: Base path is {base_path}")
    except Exception:
        # If not bundled, use the directory containing this utils script
        base_path = os.path.abspath(os.path.dirname(__file__))
        # print(f"Development mode: Base path is {base_path}")

    # print(f"Resource path for '{relative_path}': {os.path.join(base_path, relative_path)}")
    return os.path.join(base_path, relative_path)

def get_user_data_dir(app_name="TarkovMarketApp"):
     """ Gets the platform-specific user data directory. """
     if PLATFORMDIRS_AVAILABLE:
         # Example: C:\Users\<User>\AppData\Local\TarkovMarketApp\TarkovMarketApp on Windows
         #          /Users/<User>/Library/Application Support/TarkovMarketApp on macOS
         #          /home/<User>/.local/share/TarkovMarketApp on Linux
         datadir = platformdirs.user_data_dir(app_name, appauthor=False) # appauthor=False uses only app_name
         # print(f"Using platformdirs: User data directory is {datadir}")
     else:
         # Fallback to script directory if platformdirs is not installed
         datadir = os.path.abspath(os.path.dirname(__file__))
         # print(f"Fallback: User data directory is {datadir}")

     try:
         os.makedirs(datadir, exist_ok=True) # Ensure the directory exists
         # print(f"Ensured directory exists: {datadir}")
     except OSError as e:
         print(f"Error creating data directory '{datadir}': {e}")
         # Fallback to script directory in case of error creating the user data dir
         datadir = os.path.abspath(os.path.dirname(__file__))
         print(f"Error Fallback: User data directory is {datadir}")

     return datadir

# Example usage (don't run this file directly)
# if __name__ == '__main__':
#    print("Resource path for 'icon.png':", resource_path('icon.png'))
#    print("User data directory:", get_user_data_dir())