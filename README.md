# AI Document Chat Assistant

An interactive chatbot that allows users to upload documents and ask questions about their content using AI-powered responses.

## Features

- Document upload and processing
- Real-time chat interface
- AI-powered responses using OpenAI
- Persistent chat history
- Vector document indexing

## Setup Instructions

### Environment Setup

1. Create a `.env` file in the root directory:
    ```plaintext
    OPENAI_API_KEY=your-openai-api-key-here
    ```
    
### Local Development

1. Clone the repository:
    ```bash
    git clone https://github.com/KHefnawy/Document-AI-assistant
    cd Document-AI-assistant
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Run the application:
    ```bash
    streamlit run app.py
    ```

### Docker Deployment

1. Build the Docker image:
    ```bash
    docker build -t doc-chat-assistant .
    ```

2. Run the container:
    ```bash
    docker run -p 8501:8501 -e OPENAI_API_KEY=your_api_key_here doc-chat-assistant
    ```

Access the application at `http://localhost:8501`

## API Documentation

The application uses the following key components:

### Document Processing
- Supports multiple file formats (PDF, TXT, DOCX)
- Automatic document ingestion and indexing
- Vector-based similarity search

### Chat Interface
- Real-time message updates
- Persistent chat history
- Context-aware responses with memory 

## Project Structure

```
- `app.py`: Main application entry point
- `conversation_engine.py`: Chat interaction management
- `document_uploader.py`: Document processing logic
- `index_builder.py`: Vector index creation
- `global_settings.py`: Configuration settings
- `requirements.txt`: Project dependencies
- `.env`: Environment variables containing API keys
```

