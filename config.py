# app/config.py
import os
from dotenv import load_dotenv
load_dotenv() 

def load_env(key: str):
    value = os.getenv(key)
    if not value:
        raise RuntimeError(f"❌ Missing env variable: {key}")
    print(f"✅ Loaded config: {key}")
    return value


AZURE_OPENAI_API_KEY = load_env("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_ENDPOINT = load_env("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_API_VERSION = load_env("AZURE_OPENAI_API_VERSION")

EMBEDDING_DEPLOYMENT = load_env("AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME")
LLM_DEPLOYMENT = load_env("AZURE_OPENAI_DEPLOYMENT_NAME")