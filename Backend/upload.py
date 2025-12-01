"""
Upload API endpoint for document uploads to Azure Blob Storage
"""
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
import uuid
from config import (
    allowed_file,
    get_blob_service_client,
    AZURE_STORAGE_CONTAINER_NAME,
    ALLOWED_EXTENSIONS
)

# Create Blueprint
upload_bp = Blueprint('upload', __name__)

@upload_bp.route('/documents', methods=['POST'])
def upload_document():
    """
    Upload a document to Azure Blob Storage
    
    Expected: multipart/form-data with 'file' field
    Returns: JSON with blob URL and metadata
    """
    try:
        # Check if file is present in request
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        # Check if file is empty
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Validate file extension (optional)
        if not allowed_file(file.filename):
            return jsonify({'error': f'File type not allowed. Allowed types: {", ".join(ALLOWED_EXTENSIONS)}'}), 400
        
        # Secure the filename and generate unique blob name
        original_filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4()}_{original_filename}"
        
        # Get blob service client
        blob_service_client = get_blob_service_client()
        
        # Get container client (create container if it doesn't exist)
        container_client = blob_service_client.get_container_client(AZURE_STORAGE_CONTAINER_NAME)
        try:
            container_client.create_container()
        except Exception:
            # Container already exists
            pass
        
        # Upload file to blob storage
        blob_client = blob_service_client.get_blob_client(
            container=AZURE_STORAGE_CONTAINER_NAME,
            blob=unique_filename
        )
        
        # Upload the file
        file.seek(0)  # Reset file pointer to beginning
        blob_client.upload_blob(file, overwrite=True)
        
        # Get blob URL
        blob_url = blob_client.url
        
        return jsonify({
            'message': 'File uploaded successfully',
            'blob_name': unique_filename,
            'original_filename': original_filename,
            'blob_url': blob_url,
            'container': AZURE_STORAGE_CONTAINER_NAME
        }), 201
        
    except ValueError as ve:
        return jsonify({'error': str(ve)}), 500
    except Exception as e:
        return jsonify({'error': f'Failed to upload file: {str(e)}'}), 500
