from dotenv import load_dotenv
import os

load_dotenv()

MISO_API_KEY = os.environ.get("MISO_API_KEY")
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASE_URL = os.environ.get("DATABASE_URL", f"sqlite:///{BASE_DIR}/local.db")