import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

# Load .env for local dev; Render will inject env vars automatically
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")

# Debugging print for Render logs
print(f"🔍 MONGO_URI: {MONGO_URI}")
print(f"🔍 DB_NAME: {DB_NAME}")

if not MONGO_URI:
    raise ValueError("❌ MONGO_URI not found in environment variables")
if not DB_NAME:
    raise ValueError("❌ DB_NAME not found in environment variables")

# Initialize MongoDB client
client = AsyncIOMotorClient(MONGO_URI)
database = client[DB_NAME]

def get_db():
    return database
