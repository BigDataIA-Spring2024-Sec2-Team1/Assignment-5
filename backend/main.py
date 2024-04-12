import re
from fastapi import FastAPI, Path
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import warnings
import os
from dotenv import load_dotenv
load_dotenv()

warnings.filterwarnings("ignore")

SF_USERNAME = os.getenv("USERNAME")
SF_PASSWORD = os.getenv("PASSWORD")
SF_ACCOUNT_IDENTIFIER = os.getenv("ACCOUNT_IDENTIFIER")
DATABASE_NAME = os.getenv("DATABASE_NAME")
TABLE_NAME = os.getenv("TABLE_NAME")
WAREHOUSE_NAME = os.getenv("WAREHOUSE_NAME")
STAGE_NAME = os.getenv("STAGE_NAME")
STAGE_PATH = os.getenv("STAGE_PATH")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://frontend:8501"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)


@app.get("/")
def hello():
    return {"message": "Backend is running"}


@app.get("/get_data")
async def get_sf_data():
    try:
        print("calling function to get data from snowflake ")
        data = []
        return {"data": data}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

def get_summary_from_md(file_path):
    try:
        with open(file_path, "r") as md_file:
            summary_content = md_file.read()
            print(summary_content)
        return summary_content
    except Exception as e:
        print(f"Error occurred while reading MD file: {e}")
        return None
    
def generate_qa_filename(topic, filetype, set='A'):
    # Remove special characters and replace spaces with underscores
    clean_topic = re.sub(r'[^a-zA-Z0-9\s]', '', topic)
    filename = clean_topic.replace(' ', '_').lower(
    ) + f"_technical_qa_set{set}.{filetype}"
    return filename

@app.get("/get_summary_data/{topic_name}")
async def get_summary_data(topic_name: str = Path(...)):
    try:
        print(topic_name)
        local_folder_path = f"/app/backend/md_files/"
        # local_folder_path = os.path.join("/app/", file_path)
        file_name = f"{topic_name}_technical_summary.md"
        local_file_path = os.path.join(local_folder_path, os.path.basename(file_name))
        print(os.path.exists(local_file_path))
        if os.path.exists(local_file_path):
            summary_content = get_summary_from_md(local_file_path)
            return {"data": summary_content}
        else:
            return {"error": f"Summary data for topic '{topic_name}' not found."}
    except Exception as e:
        return {"error": str(e)}


@app.get("/get_qa_data/{topic_name}/{set_name}")
async def get_summary_data(topic_name: str = Path(...),set_name: str = Path(...)):
    try:
        file_name = generate_qa_filename(topic_name, "json", set_name)
        print(file_name)
        local_folder_path = f"/app/backend/json_files/"
        # local_folder_path = os.path.join("/app/", file_path)
        local_file_path = os.path.join(local_folder_path, os.path.basename(file_name))
        print(os.path.exists(local_file_path))
        if os.path.exists(local_file_path):
            summary_content = get_summary_from_md(local_file_path)
            return {"data": summary_content}
        else:
            return {"error": f"Summary data for topic '{topic_name}' not found."}
    except Exception as e:
        return {"error": str(e)}
