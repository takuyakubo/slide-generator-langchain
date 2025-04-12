import os

from dotenv import load_dotenv

load_dotenv()

LANGCHAIN_MAX_CONCURRENCY = int(os.getenv("LANGCHAIN_MAX_CONCURRENCY", 5))
LANGFUSE_SECRET_KEY = os.getenv("LANGFUSE_SECRET_KEY", "")
LANGFUSE_PUBLIC_KEY = os.getenv("LANGFUSE_PUBLIC_KEY", "")
LANGFUSE_HOST = os.getenv("LANGFUSE_HOST", "http://localhost:3000")
USE_LANGFUSE = bool(os.getenv("USE_LANGFUSE", False))

DEBUG_MODE = False
