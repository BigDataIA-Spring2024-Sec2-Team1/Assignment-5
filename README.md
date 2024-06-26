
## Problem Statement
The assignment involves leveraging Pinecone and OpenAI APIs to develop intelligent applications for knowledge retrieval and Question-Answering tasks within the enterprise. By conducting experiments using these technologies, we aim to evaluate their efficacy in addressing information curation challenges. The assignment requires data acquisition, development of Streamlit applications, implementation of functionalities, and comprehensive documentation, with evaluation based on accuracy, efficiency, and adherence to requirements.

## Project Goals
Goal is to leverage Pinecone and OpenAI api’s for creating knowledge summaries using OpenAI’s GPT, generating a knowledge base (Q/A) providing context, using a vector database to find and answer questions, use the knowledge summaries from 1 to answer questions

## Technologies Used
Web Scraping: Beautiful Soup, Scrapy
Database Upload: Pinecone
Open API GPT


## Project Structure
```
.
├── Dockerfile
├── README.md
├── backend
│   ├── Dockerfile
│   ├── __init__.py
│   ├── __pycache__
│   │   ├── __init__.cpython-39.pyc
│   │   └── main.cpython-39.pyc
│   ├── main.py
│   └── requirements.txt
├── diagrams
│   ├── __init__.py
│   └── diagram.py
├── docker-compose.yaml
├── frontend
│   ├── Dockerfile
│   ├── __init__.py
│   ├── main.py
│   ├── requirements.txt
│   └── stremlit.py
├── plugins
└── requirements.txt

```

## Important links
https://codelabs-preview.appspot.com/?file_id=1XmhLCE-nVoEAsEVM39BFWTvhlYFqiZ8ezFJiu62wbmM#0

## How to run Application locally

1. Clone the repository
2. Install dependencies
3. Set up environment variables
4. Run streamlit application
5. Select the topic and set of questions to trigger Fast API
6. View the result in the application.

## References
•	https://docs.pinecone.io/guides/getting-started/quickstart/Using_Pinecone_for_embeddings_search.ipynb
•	https://github.com/openai/openai-cookbook/blob/main/examples/vector_databases/pinecone/
•	https://github.com/openai/openai-cookbook/blob/main/examples/vector_databases/pinecone/GPT4_Retrieval_Augmentation.ipynb
•	https://github.com/pinecone-io/examples/tree/master/learn/search/question-answering
     
## Learning Outcomes
Hands-on experience with Web Scraping Techniques
Proficiency in streamlit applicatons
Understanding of Database Management and Integration
Familiarity with open API

## Team Information and Contribution 

Name            | Contribution %| Contributions |

Aniket Giram    | 35%            |Step 1, 2     |
Sudarshan Dudhe | 35%            |Step 3, 4     |
Rasika Kole     | 30%            |Frontend, documentation|