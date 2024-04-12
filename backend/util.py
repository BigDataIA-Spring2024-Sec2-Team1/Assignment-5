def get_summary_from_md(file_path):
    try:
        with open(file_path, "r") as md_file:
            summary_content = md_file.read()
        return summary_content
    except Exception as e:
        print(f"Error occurred while reading MD file: {e}")
        return None