import os


def rename_jpg_files_with_count(directory):
    jpg_files = [
        filename for filename in os.listdir(directory) if filename.startswith("WIN")
    ]

    count = 89

    for jpg_file in jpg_files:
        old_path = os.path.join(directory, jpg_file)
        new_name = f"{count}.jpg"
        new_path = os.path.join(directory, new_name)

        os.rename(old_path, new_path)
        print(f"Renamed '{jpg_file}' to '{new_name}'")

        count += 1


if __name__ == "__main__":
    target_directory = r"C:\Users\Forge-15 PRO\OneDrive\Pictures\Camera Roll\img_deco"

    rename_jpg_files_with_count(target_directory)
