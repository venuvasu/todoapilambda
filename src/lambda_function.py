import json
import logging
import os
from datetime import UTC, datetime
from typing import Dict, Any
from .todo_service import TodoService

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Environment configuration
MAX_TITLE_LENGTH = int(os.environ.get('MAX_TITLE_LENGTH', '200'))
DYNAMODB_TABLE = os.environ.get('DYNAMODB_TABLE', 'todos')

# Global service instance
todo_service = TodoService(table_name=DYNAMODB_TABLE)

def lambda_handler(event: Dict[str, Any], context) -> Dict[str, Any]:
    try:
        method = event['httpMethod']
        path = event.get('path', '')
        query_params = event.get('queryStringParameters') or {}
        
        logger.info(f"Processing {method} {path}")
        
        # Handle CORS preflight
        if method == 'OPTIONS':
            return {
                'statusCode': 200,
                'headers': get_cors_headers(),
                'body': ''
            }
        
        # Parse body if present
        body = None
        if raw_body := event.get('body'):  # Python 3.8 walrus operator
            try:
                body = json.loads(raw_body)
            except json.JSONDecodeError:
                return error_response(400, "Invalid JSON in request body")
        
        # Route handling
        if method == 'GET' and path == '/todos':
            completed = query_params.get('completed')
            if completed is not None:
                completed = completed.lower() == 'true'
            todos = todo_service.get_all(completed=completed)
            return success_response(200, todos)
            
        elif method == 'GET' and (todo_id := extract_todo_id(path)):
            if todo := todo_service.get_by_id(todo_id):
                return success_response(200, todo)
            return error_response(404, f"Todo {todo_id} not found")
            
        elif method == 'POST' and path == '/todos':
            if not body or 'title' not in body:
                return error_response(400, "Title is required")
            try:
                title = validate_title(body['title'])
                todo = todo_service.create(title)
                return success_response(201, todo)
            except ValueError as e:
                return error_response(400, str(e))
                
        elif method == 'PUT' and (todo_id := extract_todo_id(path)):
            if not body:
                return error_response(400, "Request body is required")
            try:
                # Validate updates
                validated_updates = validate_updates(body)
                if todo := todo_service.update(todo_id, **validated_updates):
                    return success_response(200, todo)
                return error_response(404, f"Todo {todo_id} not found")
            except ValueError as e:
                return error_response(400, str(e))
            
        elif method == 'DELETE' and (todo_id := extract_todo_id(path)):
            if todo_service.delete(todo_id):
                return success_response(204, None)
            return error_response(404, f"Todo {todo_id} not found")
        
        return error_response(404, "Endpoint not found")
        
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        return error_response(500, "Internal server error")

def validate_title(title: str, /) -> str:
    """Validate and sanitize todo title."""
    if not title or not (title := title.strip()):
        raise ValueError("Title cannot be empty")
    if len(title) > MAX_TITLE_LENGTH:
        raise ValueError(f"Title too long (max {MAX_TITLE_LENGTH} characters)")
    return title

def validate_updates(updates: Dict[str, Any], /) -> Dict[str, Any]:
    """Validate update fields."""
    allowed_fields = {'title', 'completed'}
    invalid_fields = set(updates.keys()) - allowed_fields
    if invalid_fields:
        raise ValueError(f"Invalid fields: {list(invalid_fields)}")
    
    validated = {}
    if 'title' in updates:
        validated['title'] = validate_title(updates['title'])
    if 'completed' in updates:
        if not isinstance(updates['completed'], bool):
            raise ValueError("completed must be a boolean")
        validated['completed'] = updates['completed']
    
    return validated

def get_cors_headers() -> Dict[str, str]:
    """Get CORS headers for responses."""
    return {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET,POST,PUT,DELETE,OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key'
    }

def extract_todo_id(path: str, /) -> str:  # Python 3.8 positional-only
    parts = path.strip('/').split('/')
    return parts[1] if len(parts) == 2 and parts[0] == 'todos' else None

def success_response(status_code: int, data: Any, /) -> Dict[str, Any]:
    response = {
        'statusCode': status_code,
        'headers': get_cors_headers()
    }
    if data is not None:
        response['body'] = json.dumps(data)
    else:
        response['body'] = ''
    return response

def error_response(status_code: int, message: str, /) -> Dict[str, Any]:
    return {
        'statusCode': status_code,
        'headers': get_cors_headers(),
        'body': json.dumps({
            'error': message,
            'timestamp': datetime.now(UTC).replace(tzinfo=None).isoformat()
        })
    }
