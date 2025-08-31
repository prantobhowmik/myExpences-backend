

from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

MONGODB_URL = os.getenv("MONGODB_URL")
if not MONGODB_URL:
	raise ValueError("MONGODB_URL environment variable not set. Please provide your MongoDB Atlas connection string.")
client = AsyncIOMotorClient(MONGODB_URL)
db = client.get_default_database()  # Uses database from Atlas URI
