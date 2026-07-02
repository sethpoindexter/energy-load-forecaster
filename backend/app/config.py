from dotenv import load_dotenv
import os

load_dotenv()

MISO_API_KEY = os.environ.get("MISO_API_KEY")
DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./local.db")