import os
import logging
from fastapi import FastAPI, Path, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
from pinecone import Pinecone
from backend.src.utility import *
from dotenv import load_dotenv


# Load environment variables
load_dotenv()

# get root logger
# the __name__ resolve to "main" since we are at the root of the project.
logger = logging.getLogger(__name__)
# This will get the root logger since no logger in the configuration has this name.

# Initialize FastAPI app
app = FastAPI()

# Initialize OpenAI and Pinecone clients
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
MODEL = "text-embedding-3-small"
pinecone_client = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

# CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://frontend:8501"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)


@app.get("/")
def hello():
    logger.info(f"Backend is running.")
    return {"message": "Backend is running"}


@app.get("/get_data")
def get_sf_data():
    try:
        data = []
        logger.info(f"Success fetching data.")
        return {"data": data}
    except Exception as e:
        logger.error(f"Error fetching data: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/get_summary_data/{topic_name}")
def get_summary_data(topic_name: str = Path(...)):
    try:
        local_folder_path = f"/app/backend/src/md_files/"
        file_name = f"{topic_name}_technical_summary.md"
        local_file_path = os.path.join(
            local_folder_path, os.path.basename(file_name))
        if os.path.exists(local_file_path):
            with open(local_file_path, "r") as md_file:
                summary_content = md_file.read()
            return {"data": summary_content}
        else:
            raise HTTPException(
                status_code=404, detail=f"Summary data for topic '{topic_name}' not found.")
    except Exception as e:
        logger.error(f"Error fetching summary data: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/get_qa_data/{topic_name}/{set_name}")
def get_qa_data(topic_name: str = Path(...), set_name: str = Path(...)):
    try:
        qa_data = []
        file_name = generate_qa_filename(topic_name, "json", set_name)
        local_folder_path = f"/app/backend/src/json_files/"
        local_file_path = os.path.join(
            local_folder_path, os.path.basename(file_name))
        if os.path.exists(local_file_path):
            with open(local_file_path, "r") as file:
                qa_data = file.read()
            return {"data": qa_data}
        else:
            raise HTTPException(
                status_code=404, detail=f"QA data for topic '{topic_name}' not found.")
    except Exception as e:
        logger.error(f"Error fetching QA data: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/get_answer_by_gpt_with_pc_summary_context")
def get_answer_by_gpt_with_pc_summary_context(req_data: ReqData):
    try:
        question_dict = req_data.question
        topic = req_data.topic
        question_markdown_text = gen_markdown_from_question(question_dict)
        answer_instance = get_answer_by_summary_from_gpt(
            question_markdown_text, topic)
        logger.info(
            f"Answer by GPT with PC summary context: {answer_instance}")
        answer_markdown_text = gen_markdown_from_Answer(answer_instance)
        return {"markdown_text": answer_markdown_text}
    except Exception as e:
        logger.error(
            f"Error fetching answer by GPT with PC summary context: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/get_answer_by_gpt_with_pc_qa_context")
def get_answer_by_gpt_with_pc_qa_context(req_data: ReqData, answer_in_markdown_text=True):
    result = {"markdown_text": "", "answer": None}
    try:
        req_data = ReqData(**req_data)
        question_dict = req_data.question
        topic = req_data.topic
        question_markdown_text = gen_markdown_from_question(question_dict)
        answer_instance = get_answer_by_gpt_vector_from_pc(
            question_markdown_text, topic)
        logger.info(f"Answer by GPT with PC QA context: {answer_instance}")
        if answer_in_markdown_text:
            answer_markdown_text = gen_markdown_from_Answer(answer_instance)
            result = {"markdown_text": answer_markdown_text}
        else:
            result = {'answer': answer_instance}
    except Exception as e:
        print(str(e))
        logger.error(
            f"Error fetching answer by GPT with PC QA context: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    return result
