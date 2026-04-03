import os
import shutil
from datetime import datetime
from PIL import Image

# This script helps the "Dirty Road" crew organize massive amounts of photos
# It reads the "Hidden Date" (EXIF) inside a picture and moves it to a folder.

source_folder = "/mnt/c/Users/south/Pictures/messy_photos"
output_folder = "/mnt/c/Users/south/Pictures/Organized_Photos"source_folder = "/mnt/c/Users/south/Pictures/messy_photos"

# Ensure folders exist
for folder in [source_folder, output_folder]:
    if not os.path.exists(folder):
        os.makedirs(folder)
        print(f"Created folder: {folder}")

def get_date_taken(path):
    try:
        img = Image.open(path)
        # 36867 is the standard code for "Date Taken"
        info = img._getexif()
        if info and 36867 in info:
            return info[36867]
    except Exception as e:
        return None

def organize():
    files = [f for f in os.listdir(source_folder) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    
    if not files:
        print("No photos found in 'messy_photos'. Put some in there first!")
        return

    for filename in files:
        file_path = os.path.join(source_folder, filename)
        date_str = get_date_taken(file_path)
        
        if date_str:
            # Date usually looks like '2024:03:15 12:00:00'
            date_obj = datetime.strptime(date_str, '%Y:%m:%d %H:%M:%S')
            folder_name = date_obj.strftime('%Y-%B') # Results in '2024-March'
        else:
            folder_name = "Unknown_Date"

        target_dir = os.path.join(output_folder, folder_name)
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)

        shutil.move(file_path, os.path.join(target_dir, filename))
        print(f"Moved: {filename} -> {folder_name}")

if __name__ == "__main__":
    organize()
    print("\nOrganization complete. Check the 'organized_photos' folder.")import os
    import shutil
    from datetime import datetime
    from PIL import Image
    
    # This script helps the "Dirty Road" crew organize massive amounts of photos
    # It reads the "Hidden Date" (EXIF) inside a picture and moves it to a folder.
    
    source_folder = "messy_photos"
    output_folder = "organized_photos"
    
    # Ensure folders exist
    for folder in [source_folder, output_folder]:
        if not os.path.exists(folder):
            os.makedirs(folder)
            print(f"Created folder: {folder}")
    
    def get_date_taken(path):
        try:
            img = Image.open(path)
            # 36867 is the standard code for "Date Taken"
            info = img._getexif()
            if info and 36867 in info:
                return info[36867]
        except Exception as e:
            return None
    
    def organize():
        files = [f for f in os.listdir(source_folder) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        
        if not files:
            print("No photos found in 'messy_photos'. Put some in there first!")
            return
    
        for filename in files:
            file_path = os.path.join(source_folder, filename)
            date_str = get_date_taken(file_path)
            
            if date_str:
                # Date usually looks like '2024:03:15 12:00:00'
                date_obj = datetime.strptime(date_str, '%Y:%m:%d %H:%M:%S')
                folder_name = date_obj.strftime('%Y-%B') # Results in '2024-March'
            else:
                folder_name = "Unknown_Date"
    
            target_dir = os.path.join(output_folder, folder_name)
            if not os.path.exists(target_dir):
                os.makedirs(target_dir)
    
            shutil.move(file_path, os.path.join(target_dir, filename))
            print(f"Moved: {filename} -> {folder_name}")
    
    if __name__ == "__main__":
        organize()
        print("\nOrganization complete. Check the 'organized_photos' folder.")
