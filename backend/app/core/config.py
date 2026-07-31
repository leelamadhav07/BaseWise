from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    APP_NAME = os.getenv("APP_NAME", "Basewise API")
    APP_VERSION = os.getenv("APP_VERSION", "0.1.0")
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"

settings = Settings()

#Instead of hardcoding values in our code, we load them from environment variables. 
#Later, API keys and database URLs will also go here.