from dotenv import load_dotenv
load_dotenv()
import os
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
print(os.getenv('GOOGLE_API_KEY'))