# Minimal RAG API with Dropbox Integration

This project implements a Retrieval-Augmented Generation (RAG) API that integrates with Dropbox to process and analyze documents. The system allows users to upload documents to Dropbox and query them using natural language.

## Features

- Document processing from Dropbox
- Support for multiple document formats (PDF, DOCX, PPTX)
- Text extraction and OCR capabilities
- Vector-based document retrieval
- Natural language querying using LLM

## Prerequisites

- Python 3.8 or higher
- Dropbox account with API access
- Dropbox folder filled with internal documents (PDF, DOCX, PPTX, ...)
- OpenRouter API key for LLM access
- Tesseract OCR is installed on your system

## Installation

1. Clone the repository:
```bash
git clone git@github.com:Nolab0/test-technique-tc.git
cd test-technique-tc
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Install Tesseract OCR:
- On Ubuntu/Debian:
```bash
sudo apt-get install tesseract-ocr
```
- On macOS:
```bash
brew install tesseract
```
- On Windows: Download and install from [Tesseract GitHub releases](https://github.com/UB-Mannheim/tesseract/wiki)

## Environment Setup

Create a `.env` file in the root directory. An example is provided by `.env.example`.

### Obtaining API Keys

1. **Dropbox Access Token**:
   - Go to [Dropbox App Console](https://www.dropbox.com/developers/apps)
   - Create a new app or select an existing one
   - Generate an access token with the necessary permissions

2. **OpenRouter API Key**:
   - Sign up at [OpenRouter](https://openrouter.ai/)
   - Generate an API key from your dashboard

## Running the Application

1. Start the FastAPI server:
```bash
python main.py
```

2. The API will be available at `http://localhost:8000`


## Technical Approach

The application follows a RAG (Retrieval-Augmented Generation) architecture:

1. **Document Processing**:
   - Documents are retrieved from Dropbox
   - Text is extracted using appropriate libraries (pdfplumber, python-docx, python-pptx)
   - OCR is applied when needed using Tesseract

2. **Vector Storage**:
   - Documents are chunked into smaller segments
   - Text embeddings are generated using sentence-transformers
   - FAISS is used for efficient similarity search on CPU

3. **Query Processing**:
   - User queries are converted to embeddings
   - Relevant document chunks are retrieved using similarity search
   - Context is provided to the LLM for generating responses
   - I have choosen Llama3.8-8B-instruct model from Meta for this project
   - OpenRouter is used to access the model, it ensures model availability through OpenAI API

4. **API Layer**:
   - FastAPI provides a RESTful interface
   - Documents loading + vectorization are done at startup to avoid latency during requests


## API Endpoints

- `GET` `/query?question=<question>`: Query the processed documents

Example with Paris wikipedia page in Dropbox folder:
```bash
curl -X GET "http://localhost:8000/query?question=How%20many%20tourists%20in%20Paris%20region%20in%202019%3F" -H "Accept: application/json" 
```

## Points for improvement
- Adjust ```chunk size``` and ```chunk overlap``` according to the document type.
- Test and benchmark multiple models (Llama, OpenAI, Gemma, ...)
- Deploy in a production environment
