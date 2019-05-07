from dotenv import load_dotenv
import os

DATA_DIR = os.path.abspath(os.getenv('DATA_DIR'))

load_dotenv(dotenv_path='.env', verbose=True)
