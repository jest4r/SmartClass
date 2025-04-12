import json
import logging
from datetime import date, datetime
from odoo import http

_logger = logging.getLogger(__name__)

class StudentBaseController(http.Controller):
    """Base controller with shared functionality"""
    
    DEFAULT_DB = "odoo_demo"  # Set your default database name here
    
    @staticmethod
    def get_db_name(kw):
        """Get database name from request parameters or use default"""
        return kw.get('db', StudentBaseController.DEFAULT_DB)
    @staticmethod
    def make_json_response(data):
        """Convert response data to JSON string"""
        
        return json.dumps(data, default=lambda obj: obj.isoformat() if isinstance(obj, (date, datetime)) else None)
    
    @staticmethod
    def handle_exception(e, context=""):
        """Create a standardized error response"""
        _logger.error(f"Error {context}: {e}")
        return {
            "code": 500,
            "status": "error",
            "message": str(e),
            "data": None
        }
    