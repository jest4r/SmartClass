import json
import logging

_logger = logging.getLogger(__name__)

class ResponseSerializer:
    @staticmethod
    def serialize(response_data):
        """Serialize response data to JSON"""
        try:
            return json.dumps(response_data)
        except Exception as e:
            _logger.error(f"Error serializing response: {e}")
            error_response = {
                "code": 500,
                "status": "error",
                "message": "Failed to serialize response",
                "data": None
            }
            return json.dumps(error_response)
    
    @staticmethod
    def normalize_record(record, fields=None):
        """Convert record to a dictionary with specified fields"""
        if not fields:
            fields = ['id', 'name', 'description', 'code']
            
        result = {}
        for field in fields:
            try:
                result[field] = getattr(record, field, None)
            except Exception:
                result[field] = None
                
        return result