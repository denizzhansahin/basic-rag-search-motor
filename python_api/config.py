import os
from dotenv import load_dotenv

# .env dosyasındaki değişkenleri yükle
load_dotenv()

ACCEPT_URL = os.getenv("ACCEPT_URL").split(",")
SECRET_KEY = os.getenv("SECRET_KEY")






