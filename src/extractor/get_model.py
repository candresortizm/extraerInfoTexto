from langchain_aws import ChatBedrock
import os
from dotenv import load_dotenv

load_dotenv()

MODEL_LLM = None  
BEDROCK_MODEL_ID = "amazon.nova-lite-v1:0"
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID', None)
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY', None)
AWS_DEFAULT_REGION = os.environ.get('AWS_DEFAULT_REGION', None)

def get_model_llm():
    global MODEL_LLM
    if not MODEL_LLM:
        # Prepare the DB.
        print("AWS_ACCESS_KEY_ID")
        print(AWS_ACCESS_KEY_ID)
        MODEL_LLM = ChatBedrock(model_id=BEDROCK_MODEL_ID,
                                aws_access_key_id=AWS_ACCESS_KEY_ID,
                                aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                                region_name=AWS_DEFAULT_REGION)
        print(f"✅ Init Model LLM {MODEL_LLM}")

    return MODEL_LLM