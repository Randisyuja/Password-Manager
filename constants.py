import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOCK_IMG_PATH = os.path.join(BASE_DIR, "img/lock.png")
DATA_FILE = os.path.join(BASE_DIR, "data/data.json")
MASTER_FILE = "data/master.hash"
SALT_PATH = "data/secret_salt.bin"
