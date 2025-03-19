import logging

_logger = logging.getLogger(__name__)

class ClassValidator:
    @staticmethod
    def validate_creation_data(data):
        """Validate data for class creation"""
        required_fields = ['name', 'description', 'code']
        
        if not isinstance(data, dict):
            return False, "Request body must be a JSON object"
            
        # Check for required fields
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return False, f"Missing required fields: {', '.join(missing_fields)}"
        
        # Validate field types
        if not isinstance(data.get('name', ''), str) or not data.get('name', '').strip():
            return False, "Name must be a non-empty string"
            
        if not isinstance(data.get('description', ''), str):
            return False, "Description must be a string"
            
        if not isinstance(data.get('code', ''), str) or not data.get('code', '').strip():
            return False, "Code must be a non-empty string"
            
        return True, "Data is valid"
    
    @staticmethod
    def validate_pagination_params(params):
        """Validate pagination parameters"""
        try:
            page = int(params.get('page', 1))
            size = int(params.get('size', 10))
            
            if page < 1:
                return False, "Page number must be at least 1"
                
            if size < 1:
                return False, "Size must be at least 1"
                
            return True, "Parameters are valid"
        except ValueError:
            return False, "Page and size must be integers"