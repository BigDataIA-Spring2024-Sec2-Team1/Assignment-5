#!/usr/bin/env python
import streamlit as st
import requests
import warnings
import os
import pandas as pd

from sqlalchemy import create_engine

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

# current_folder_path = os.getcwd()


def get_engine():
    engine = create_engine(
        f"snowflake://{SF_USERNAME}:{SF_PASSWORD}@{SF_ACCOUNT_IDENTIFIER}/"
    )
    return engine

def view_table(engine):
    with engine.connect() as connection:
        connection.execute(f"""USE DATABASE {DATABASE_NAME};""")
        result = connection.execute(f"""SHOW TABLES LIKE '{TABLE_NAME}'""")
        existing_tables = [row[1] for row in result.fetchall()]
        print(existing_tables)
        if TABLE_NAME.upper()  in existing_tables:
            # Create table
            result_cursor = connection.execute(
                f"""SELECT * FROM {TABLE_NAME}"""
            )
            result = result_cursor.fetchall()
            df_columns  = list(result[0])
            df = pd.DataFrame(result[1:], columns=df_columns)
            # Close cursor and connection
            result_cursor.close()
            print("Data fetched successfully.")
            engine.dispose()
            return df
        else:
            engine.dispose()
            print("Table does not exists.")
            return None




def view_table_from_snowflake():
    try:
        engine = get_engine()
        result = view_table(engine)
        print(result)
        print("Done")
        return result
    except Exception as e:
        # Log the error message
        print(f"Error while view_table_from_snowflake data : {e}")
        return False

# result = view_table_from_snowflake()
# print(result)

def upload_page():
    st.title("Upload File to S3")
    file = st.file_uploader("Choose a file", type=["pdf"])

    if file:
        progress_bar = st.progress(0)
        st.write("File ready to Upload!")

        # Button to trigger file upload
        if st.button("Upload to S3"):
            # Send file to FastAPI endpoint
            files = {"files": (file.name, file.getvalue())}
            response = requests.post("http://backend:8000/upload", files=files)

            total_size = int(response.headers.get('content-length', 0))

            uploaded_size = 0
            for chunk in response.iter_content(chunk_size=1024):
                uploaded_size += len(chunk)
                progress = uploaded_size / total_size
                progress_bar.progress(progress)

            if response.status_code == 200:
                st.success("File uploaded successfully to S3!")
            else:
                st.error("Failed to upload file. Error: {}".format(response.text))


def view_page():
    st.title("View Document")
    
    # Retrieve the uploaded file from session state
    data = view_table_from_snowflake()

    if data is not None:
        # Display the fetched data in a table
        st.write("Data fetched from Snowflake:")
        st.write(data)

    else:
        st.error("No document uploaded. Please go back to upload page.")

# Main function to manage page navigation
def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Upload", "View"])

    if page == "Upload":
        upload_page()
    elif page == "View":
        view_page()

if __name__ == "__main__":
    main()
