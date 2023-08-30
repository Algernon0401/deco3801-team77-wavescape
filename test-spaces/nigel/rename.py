import os
import uuid


def rename_jpg_files_with_uuid(directory):
    jpg_files = [
        filename for filename in os.listdir(directory) if filename.endswith(".jpg")
    ]

    for jpg_file in jpg_files:
        old_path = os.path.join(directory, jpg_file)
        new_name = str(uuid.uuid4()) + ".jpg"
        new_path = os.path.join(directory, new_name)

        os.rename(old_path, new_path)
        print(f"Renamed '{jpg_file}' to '{new_name}'")


if __name__ == "__main__":
    target_directory = r"C:\Users\Forge-15 PRO\Downloads\train\Training images"

    rename_jpg_files_with_uuid(target_directory)
