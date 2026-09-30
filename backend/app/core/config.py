from dotenv import load_dotenv
import os

load_dotenv()

# Automatically load backend/.env if present
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.abspath(os.path.join(current_dir, "..", ".."))
backend_env = os.path.join(backend_dir, ".env")
if os.path.exists(backend_env):
    load_dotenv(backend_env)

class Settings:
    APP_NAME = os.getenv("APP_NAME", "Basewise API")
    APP_VERSION = os.getenv("APP_VERSION", "0.1.0")
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    DATABASE_URL = os.getenv("DATABASE_URL")
settings = Settings()

#Instead of hardcoding values in our code, we load them from environment variables. 
#Later, API keys and database URLs will also go here.