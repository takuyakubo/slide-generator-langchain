import os
from dotenv import load_dotenv

load_dotenv()

LANGCHAIN_MAX_CONCURRENCY = int(os.getenv("LANGCHAIN_MAX_CONCURRENCY", 5))
