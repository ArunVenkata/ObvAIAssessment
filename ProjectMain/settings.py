from dotenv import load_dotenv
import os


load_dotenv(override=True)
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key") 
AUTH_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

DATABASE_URL =  os.getenv("DATABASE_URI", f"sqlite:///{os.path.join(BASE_DIR, 'books.db')}")
