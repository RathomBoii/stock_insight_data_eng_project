import os

def check_existing_raw_data(file_path: str) -> bool :
    is_existing_file_path = os.path.exists(file_path)
    if is_existing_file_path:
        print(f"Raw partition exists for {file_path}, reading from disk...")
        return True
    else:
        print(f"Raw partition does not exist for {file_path}, fetching data...")
        return False