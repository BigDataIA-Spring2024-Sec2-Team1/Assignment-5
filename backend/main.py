import os
from dotenv import load_dotenv
from fastapi import FastAPI, Path, HTTPException,Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
from pinecone import Pinecone
from backend.utility import *
load_dotenv()

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
    return {"message": "Backend is running"}


@app.get("/get_data")
def get_sf_data():
    try:
        data = []
        return {"data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/get_summary_data/{topic_name}")
def get_summary_data(topic_name: str = Path(...)):
    try:
        local_folder_path = f"/app/backend/md_files/"
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
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/get_qa_data/{topic_name}/{set_name}")
def get_qa_data(topic_name: str = Path(...), set_name: str = Path(...)):
    try:
        qa_data = []
        file_name = generate_qa_filename(topic_name, "json", set_name)
        local_folder_path = f"/app/backend/json_files/"
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
        raise HTTPException(status_code=500, detail=str(e))


# class RequestData(BaseModel):
#     question: str


class Question(BaseModel):
    question: str
    options: List[str]
    answer: str
    justification: str

@app.post("/get_answer_by_gpt_with_pc_summary_context")
def get_answer_by_gpt_with_pc_summary_context(question: Question):
    markdown_text = f"### {question.question}\n\n"
    markdown_text += "Options:\n\n"
    for option in question.options:
        markdown_text += f"- {option}\n"
    markdown_text += f"\n**Answer:** {question.answer}\n\n"
    markdown_text += f"Justification: {question.justification}\n\n"
    answer_text = get_summary_from_gpt(markdown_text)
    response = answer_text.choices[0].text
    print(response)
    return {"markdown_text": response}



# @app.post("/get_answer_by_gpt_with_pc_summary_context/{topic_name}")
# def get_answer_by_gpt_with_pc_summary_context(topic_name: str, data):
#     try:
#         print(topic_name)
#         print(data)
#         text = convert_to_markdown(data)
#         answer = get_summary_from_gpt(text, topic_name)
#         if answer:
#             return {"data": answer}
#         else:
#             raise HTTPException(
#                 status_code=404, detail=f"Summary data for topic '{topic_name}' not found.")
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
