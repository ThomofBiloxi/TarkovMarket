# create_assets.py
import os
try:
    from PIL import Image, ImageDraw
    print("Pillow library found.")
except ImportError:
    print("Error: Pillow library not found.")
    print("Please install it using: pip install Pillow")
    exit()

def create_placeholder(filename="placeholder.png", size=(128, 128), color=(128, 128, 128)):
    """Creates a solid gray placeholder image."""
    try:
        img = Image.new('RGB', size, color=color)
        img.save(filename)
        print(f"Successfully created opaque placeholder: '{filename}'")
    except Exception as e:
        print(f"Error creating '{filename}': {e}")

def create_error_icon(filename="error.png", size=(128, 128), bg_color=(128, 128, 128), x_color=(255, 0, 0), line_width=8):
    """Creates a solid gray image with an opaque red X."""
    try:
        img = Image.new('RGB', size, color=bg_color)
        draw = ImageDraw.Draw(img)

        # Calculate coordinates for the X lines
        # Line 1: Top-left to Bottom-right
        draw.line([(0, 0), (size[0] - 1, size[1] - 1)], fill=x_color, width=line_width)
        # Line 2: Top-right to Bottom-left
        draw.line([(size[0] - 1, 0), (0, size[1] - 1)], fill=x_color, width=line_width)

        img.save(filename)
        print(f"Successfully created opaque error icon: '{filename}'")
    except Exception as e:
        print(f"Error creating '{filename}': {e}")

if __name__ == "__main__":
    print("Creating image assets using Pillow...")

    # Define the output directory (current directory where the script is run)
    output_dir = os.path.dirname(os.path.abspath(__file__))
    placeholder_path = os.path.join(output_dir, "placeholder.png")
    error_path = os.path.join(output_dir, "error.png")

    # --- Safety Check: Delete existing files first ---
    if os.path.exists(placeholder_path):
        print(f"Deleting existing '{placeholder_path}'...")
        try:
            os.remove(placeholder_path)
        except OSError as e:
            print(f"  Error deleting file: {e}")
    if os.path.exists(error_path):
        print(f"Deleting existing '{error_path}'...")
        try:
            os.remove(error_path)
        except OSError as e:
            print(f"  Error deleting file: {e}")
    # --- End Safety Check ---


    create_placeholder(filename=placeholder_path)
    create_error_icon(filename=error_path)
    print("Finished.")