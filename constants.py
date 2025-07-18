import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_PATH = os.path.join(BASE_DIR, "data")
DATA_FILE = "data.json"
MASTER_FILE = "master.hash"
SALT_FILE = "secret_salt.bin"
LOCK_IMG_PATH = os.path.join(BASE_DIR, "img/lock.png")


def ensure_hash_file(folder_path, file_name) -> str:
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    file_path = os.path.join(folder_path, file_name)
    return str(file_path)


def ensure_bin_file(folder_path, file_name) -> str:
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    file_path = os.path.join(folder_path, file_name)
    return str(file_path)


def ensure_json_file(folder_path, file_name) -> str:
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    file_path = os.path.join(folder_path, file_name)
    return str(file_path)


DATA_PATH = ensure_json_file(FILE_PATH, DATA_FILE)
MASTER_PATH = ensure_hash_file(FILE_PATH, MASTER_FILE)
SALT_PATH = ensure_bin_file(FILE_PATH, SALT_FILE)
