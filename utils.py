from dropboxDriver import download_file, list_files
from reading import extract_text_from_docx, extract_text_from_pdf, extract_text_from_pptx


def process_files(dbx, folder_path=""):
    """Extract and return all text from Dropbox documents."""
    text_data = []
    files = list_files(dbx, folder_path)
    for file in files:
        print(f"Processing: {file.name}")
        file_bytes = download_file(dbx, file.path_lower)

        if file.name.endswith(".pdf"):
            text = extract_text_from_pdf(file_bytes)
        elif file.name.endswith(".pptx"):
            text = extract_text_from_pptx(file_bytes)
        elif file.name.endswith(".docx"):
            text = extract_text_from_docx(file_bytes)
        else:
            print(f"Skipping unsupported file: {file.name}")
            continue

        text_data.append({"filename": file.name, "text": text})
    return text_data
