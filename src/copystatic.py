import os
import shutil

def setup_public_dir(dest_dir_path):
    if os.path.exists(dest_dir_path):
        shutil.rmtree(dest_dir_path)
    os.mkdir(dest_dir_path)

def copy_files_recursive(source_dir_path, dest_dir_path):
    for item in os.listdir(source_dir_path):
        item_path = os.path.join(source_dir_path, item)
        if os.path.isfile(item_path):
            print(f"Now copying {item_path}...")
            shutil.copy(item_path, dest_dir_path)
        else:
            dest_path = os.path.join(dest_dir_path, item)
            os.mkdir(dest_path)
            copy_files_recursive(item_path, dest_path)
