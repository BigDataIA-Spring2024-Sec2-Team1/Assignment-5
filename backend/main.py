from fastapi import FastAPI
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
