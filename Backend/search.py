"""
Search API endpoint for document search functionality
"""
from flask import Blueprint, request, jsonify
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
import os

# Create Blueprint
search_bp = Blueprint('search', __name__)

@search_bp.route('/documents/search', methods=['POST'])
def search_documents():
    """
    Search for documents based on text input
    
    Expected: JSON body with 'query' field
    Returns: JSON response using Azure AI Projects agent
    """
    try:
        # Get JSON data from request
        data = request.get_json()
        
        if not data or 'query' not in data:
            return jsonify({'error': 'No query provided'}), 400
        
        query = data.get('query', '').strip()
        
        if not query:
            return jsonify({'error': 'Query cannot be empty'}), 400
        
        myEndpoint = "https://health-tracker-resource.services.ai.azure.com/api/projects/health-tracker"

        project_client = AIProjectClient(
            endpoint=myEndpoint,
            credential=DefaultAzureCredential(),
        )

        myAgent = "health-tracker-agent"
        # Get an existing agent
        agent = project_client.agents.get(agent_name=myAgent)
        print(f"Retrieved agent: {agent.name}")

        openai_client = project_client.get_openai_client()
        response = openai_client.responses.create(
            input=[{"role": "user", "content": query}],
            extra_body={"agent": {"name": agent.name, "type": "agent_reference"}},
        )

        print(f"Response output: {response.output_text}")
        
        return jsonify({
            'message': response.output_text,
            'query': query,
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Search failed: {str(e)}'}), 500
