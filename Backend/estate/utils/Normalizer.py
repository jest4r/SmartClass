import logging
import re
from datetime import datetime

_logger = logging.getLogger(__name__)

class Normalizer:
    """
    Utility class to normalize data between different formats and representations.
    Provides methods to standardize, clean, and transform data.
    """
    
    @staticmethod
    def normalize_string(value, default=""):
        """
        Normalize a string value by trimming whitespace and handling None values.
        
        Args:
            value: The string to normalize
            default: Default value if the input is None or empty
            
        Returns:
            Normalized string
        """
        if value is None:
            return default
        
        try:
            return str(value).strip()
        except Exception as e:
            _logger.warning(f"Failed to normalize string: {e}")
            return default
    
    @staticmethod
    def normalize_code(code, default=""):
        """
        Normalize a code by converting to uppercase and removing special characters.
        
        Args:
            code: The code to normalize
            default: Default value if the input is None or empty
            
        Returns:
            Normalized code
        """
        if not code:
            return default
        
        try:
            # Remove special characters and convert to uppercase
            normalized = re.sub(r'[^A-Za-z0-9_-]', '', code).upper()
            return normalized or default
        except Exception as e:
            _logger.warning(f"Failed to normalize code: {e}")
            return default
    
    @staticmethod
    def normalize_integer(value, default=0):
        """
        Convert a value to an integer, handling errors gracefully.
        
        Args:
            value: The value to convert to integer
            default: Default value if conversion fails
            
        Returns:
            Normalized integer
        """
        if value is None:
            return default
        
        try:
            return int(float(value))
        except Exception:
            _logger.debug(f"Failed to normalize as integer: {value}")
            return default
    
    @staticmethod
    def normalize_float(value, precision=2, default=0.0):
        """
        Convert a value to a float with specified precision.
        
        Args:
            value: The value to convert to float
            precision: Decimal precision
            default: Default value if conversion fails
            
        Returns:
            Normalized float
        """
        if value is None:
            return default
        
        try:
            return round(float(value), precision)
        except Exception:
            _logger.debug(f"Failed to normalize as float: {value}")
            return default
    
    @staticmethod
    def normalize_boolean(value, default=False):
        """
        Normalize a boolean value, handling different representations.
        
        Args:
            value: The value to convert to boolean
            default: Default value if conversion fails
            
        Returns:
            Normalized boolean
        """
        if value is None:
            return default
        
        # Handle string representations
        if isinstance(value, str):
            value = value.lower().strip()
            if value in ('true', 't', 'yes', 'y', '1'):
                return True
            if value in ('false', 'f', 'no', 'n', '0'):
                return False
            return default
            
        # Handle numeric representations
        if isinstance(value, (int, float)):
            return bool(value)
            
        # Handle boolean
        if isinstance(value, bool):
            return value
            
        return default
    
    @staticmethod
    def normalize_date(value, format_str="%Y-%m-%d", default=None):
        """
        Normalize a date string to datetime object.
        
        Args:
            value: The date string to normalize
            format_str: Expected date format
            default: Default value if conversion fails
            
        Returns:
            Normalized datetime object or default
        """
        if not value:
            return default
            
        if isinstance(value, datetime):
            return value
            
        try:
            return datetime.strptime(str(value).strip(), format_str)
        except Exception:
            _logger.debug(f"Failed to normalize date: {value}")
            return default
    
    @staticmethod
    def normalize_dict(data, required_fields=None, defaults=None):
        """
        Normalize a dictionary by ensuring required fields and setting defaults.
        
        Args:
            data: Dictionary to normalize
            required_fields: List of required field names
            defaults: Dictionary of default values for fields
            
        Returns:
            Normalized dictionary
        """
        if not isinstance(data, dict):
            return {}
            
        result = data.copy()
        
        # Apply defaults
        if defaults:
            for field, default_value in defaults.items():
                if field not in result or result[field] is None:
                    result[field] = default_value
        
        # Check required fields
        if required_fields:
            for field in required_fields:
                if field not in result or result[field] is None:
                    _logger.warning(f"Required field {field} is missing or None")
        
        return result
    
    @staticmethod
    def normalize_list(data, item_normalizer=None):
        """
        Normalize a list by applying a normalizer function to each item.
        
        Args:
            data: List to normalize
            item_normalizer: Function to apply to each item
            
        Returns:
            Normalized list
        """
        if not isinstance(data, list):
            return []
            
        if item_normalizer is None:
            return data
            
        try:
            return [item_normalizer(item) for item in data]
        except Exception as e:
            _logger.warning(f"Failed to normalize list: {e}")
            return []
    
    @staticmethod
    def normalize_class_record(record_data):
        """
        Normalize class record data for use in the API.
        
        Args:
            record_data: Dictionary containing class record data
            
        Returns:
            Normalized class record dictionary
        """
        if not record_data:
            return {}
            
        normalized = {}
        
        # Normalize standard fields
        normalized['id'] = Normalizer.normalize_integer(record_data.get('id'))
        normalized['name'] = Normalizer.normalize_string(record_data.get('name'))
        normalized['description'] = Normalizer.normalize_string(record_data.get('description'))
        normalized['code'] = Normalizer.normalize_code(record_data.get('code'))
        
        # Include any additional fields present in the original data
        for key, value in record_data.items():
            if key not in normalized:
                normalized[key] = value
                
        return normalized
    @staticmethod
    def normalize_student_record(record_data):
        """
        Normalize student record data for use in the API.
        
        Args:
            record_data: Dictionary containing student record data
            
        Returns:
            Normalized student record dictionary
        """
        if not record_data:
            return {}
            
        normalized = {}
        
        # Normalize standard fields
        normalized['id'] = Normalizer.normalize_integer(record_data.get('id'))
        normalized['fullname'] = Normalizer.normalize_string(record_data.get('fullname'))
        normalized['code'] = Normalizer.normalize_code(record_data.get('code'))
        normalized['username'] = Normalizer.normalize_string(record_data.get('username'))
        
        # Handle dates
        if 'dob' in record_data:
            normalized['dob'] = record_data.get('dob')  # Keep original format for database compatibility
        
        # Handle optional fields with appropriate defaults
        normalized['sex'] = Normalizer.normalize_string(record_data.get('sex', ''))
        normalized['email'] = Normalizer.normalize_string(record_data.get('email', ''))
        normalized['address'] = Normalizer.normalize_string(record_data.get('address', ''))
        normalized['homecity'] = Normalizer.normalize_string(record_data.get('homecity', ''))
        normalized['phone'] = Normalizer.normalize_string(record_data.get('phone', ''))
        
        # Special handling for class_id (can be False or int)
        if 'class_id' in record_data:
            try:
                normalized['class_id'] = int(record_data.get('class_id')) if record_data.get('class_id') else False
            except (ValueError, TypeError):
                normalized['class_id'] = False
        
        # Include any additional fields present in the original data
        for key, value in record_data.items():
            if key not in normalized:
                normalized[key] = value
                
        return normalized

    @staticmethod
    def normalize_search_term(term):
        """
        Normalize a search term for use in database queries.
        
        Args:
            term: Search term to normalize
            
        Returns:
            Normalized search term
        """
        if not term:
            return ""
            
        # Remove special SQL characters
        normalized = re.sub(r'[%_\'";]', ' ', str(term))
        
        # Collapse multiple spaces
        normalized = re.sub(r'\s+', ' ', normalized).strip()
        
        return normalized