# HealthDocumentTracker

A Python Flask API for managing health documents with Azure Blob Storage integration.

## Features

- **Document Upload**: Upload health documents to Azure Blob Storage
- **Document Search**: Search functionality with text input (implementation ready for your custom logic)
- **Environment Configuration**: Secure credential management using environment variables
- **File Validation**: Support for common document formats (PDF, DOC, DOCX, TXT, images)

## Prerequisites

- Python 3.8 or higher
- Azure Storage Account with Blob Storage enabled
- Azure Storage connection string and API key

## Installation

1. **Clone the repository**
```bash
git clone https://github.com/gitika-bose/HealthDocumentTracker.git
cd HealthDocumentTracker
```

2. **Navigate to the Backend directory**
```bash
cd Backend
```

3. **Create and activate a virtual environment** (recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

4. **Install dependencies**
```bash
pip install -r requirements.txt
```

5. **Configure environment variables**

Copy the example environment file:
```bash
# Windows
copy .env.example .env

# Linux/Mac
cp .env.example .env
```

Edit `.env` and add your Azure Storage credentials:
```
AZURE_STORAGE_CONNECTION_STRING=your_actual_connection_string_here
AZURE_STORAGE_CONTAINER_NAME=health-documents
PORT=5000
FLASK_DEBUG=False
```

### Getting Your Azure Storage Connection String

1. Go to [Azure Portal](https://portal.azure.com)
2. Navigate to your Storage Account
3. Go to **Security + networking** → **Access keys**
4. Copy the **Connection string** from Key1 or Key2

## Running the API

Start the Flask application:
```bash
python app.py
```

The API will be available at `http://localhost:5000`

## API Endpoints

### 1. Upload Document

**Endpoint**: `POST /documents`

**Description**: Upload a document to Azure Blob Storage

**Request Type**: `multipart/form-data`

**Parameters**:
- `file` (required): The file to upload

**Supported File Types**: PDF, DOC, DOCX, TXT, JPG, JPEG, PNG

**Example using cURL**:
```bash
curl -X POST http://localhost:5000/documents \
  -F "file=@/path/to/your/document.pdf"
```

**Example using Python**:
```python
import requests

url = "http://localhost:5000/documents"
files = {'file': open('document.pdf', 'rb')}
response = requests.post(url, files=files)
print(response.json())
```

**Success Response** (201):
```json
{
  "message": "File uploaded successfully",
  "blob_name": "a1b2c3d4-e5f6-7890-abcd-ef1234567890_document.pdf",
  "original_filename": "document.pdf",
  "blob_url": "https://youraccount.blob.core.windows.net/health-documents/...",
  "container": "health-documents"
}
```

**Error Responses**:
- `400`: No file provided or invalid file type
- `500`: Upload failed or Azure configuration error

### 2. Search Documents

**Endpoint**: `POST /documents/search`

**Description**: Search for documents based on text query

**Request Type**: `application/json`

**Parameters**:
```json
{
  "query": "your search text here"
}
```

**Example using cURL**:
```bash
curl -X POST http://localhost:5000/documents/search \
  -H "Content-Type: application/json" \
  -d '{"query": "medical records"}'
```

**Example using Python**:
```python
import requests

url = "http://localhost:5000/documents/search"
data = {"query": "medical records"}
response = requests.post(url, json=data)
print(response.json())
```

**Success Response** (200):
```json
{
  "message": "Search endpoint ready",
  "query": "medical records",
  "note": "Add your search implementation here"
}
```

**Note**: The search endpoint is ready to accept requests. Add your custom search implementation logic in the `search_documents()` function in `app.py`.

**Error Responses**:
- `400`: No query provided or empty query
- `500`: Search operation failed

### 3. Health Check

**Endpoint**: `GET /health`

**Description**: Check if the API is running

**Example**:
```bash
curl http://localhost:5000/health
```

**Response** (200):
```json
{
  "status": "healthy",
  "service": "HealthDocumentTracker"
}
```

## Project Structure

```
HealthDocumentTracker/
├── Backend/
│   ├── app.py              # Main Flask application entry point
│   ├── config.py           # Shared configuration and utilities
│   ├── upload.py           # Document upload API endpoint
│   ├── search.py           # Document search API endpoint
│   ├── requirements.txt    # Python dependencies
│   ├── .env               # Environment variables (not in git)
│   └── .env.example       # Example environment configuration
├── .gitignore
└── README.md              # This file
```

### File Descriptions

- **app.py**: Main Flask application that registers blueprints and runs the server
- **config.py**: Shared configuration, environment variables, and utility functions for Azure Blob Storage
- **upload.py**: Blueprint containing the `/documents` POST endpoint for file uploads
- **search.py**: Blueprint containing the `/documents/search` POST endpoint for document search
- **requirements.txt**: Python package dependencies
- **.env.example**: Template for environment variables (copy to .env and configure)

## Security Considerations

- Never commit your `.env` file to version control
- Keep your Azure Storage connection string secure
- Use Azure's managed identities in production environments
- Consider implementing authentication/authorization for production use
- Validate and sanitize all user inputs
- Set appropriate CORS policies if needed

## Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `AZURE_STORAGE_CONNECTION_STRING` | Azure Storage account connection string | Yes | - |
| `AZURE_STORAGE_CONTAINER_NAME` | Blob container name | No | `health-documents` |
| `PORT` | Port for Flask server | No | `5000` |
| `FLASK_DEBUG` | Enable debug mode | No | `False` |

## Development

To run in debug mode, set in your `.env` file:
```
FLASK_DEBUG=True
```

## Troubleshooting

**Issue**: "Azure Storage connection string not configured"
- **Solution**: Ensure `AZURE_STORAGE_CONNECTION_STRING` is set in your `.env` file

**Issue**: Container creation fails
- **Solution**: Check your Azure Storage account permissions and ensure the connection string is correct

**Issue**: File upload fails
- **Solution**: Verify the file size is within Azure Blob Storage limits and the file type is allowed

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License.

## Support

For issues or questions, please open an issue in the GitHub repository.
