import json
import logging
from odoo import http
from .class_base_controller import BaseController
from ..controllers.class_controller import ClassController
from ..utils.Validator import Validator

_logger = logging.getLogger(__name__)

class ClassAPI(BaseController):
    """API endpoints for class management"""
    
    # === GET ENDPOINTS ===
    @http.route(['/api/classes/<id>'], type='http', auth="none", sitemap=False, cors='*', csrf=False, methods=['GET'])
    def get_by_id(self, id, **kw):
        _logger.info(f"API: Get class by ID: {id}")
        try:
            dbname = self.get_db_name(kw)
            result = ClassController.get_by_id(dbname, id)
            return self.make_json_response(result)
        except Exception as e:
            return self.make_json_response(self.handle_exception(e, "getting class by ID"))

    @http.route(['/api/classes'], type='http', auth="none", sitemap=False, cors='*', csrf=False, methods=['GET'])
    def get_all(self, **kw):
        _logger.info("API: Get all classes")
        try:
            dbname = self.get_db_name(kw)
            result = ClassController.get_all(dbname)
            return self.make_json_response(result)
        except Exception as e:
            return self.make_json_response(self.handle_exception(e, "getting all classes"))

    @http.route(['/api/classes/page/<int:page>'], type='http', auth="none", sitemap=False, cors='*', csrf=False, methods=['GET'])
    def get_paginated(self, page, **kw):
        _logger.info(f"API: Get paginated classes, page: {page}")
        try:
            dbname = self.get_db_name(kw)
            
            # Parse parameters
            size = int(kw.get('size', 10))
            order_param = kw.get('order', '')
            search = kw.get('search', '').strip()
            column_list = kw.get('columnlist', '').split(',') if kw.get('columnlist') else ['id', 'code', 'name', 'description']
            top_list = list(map(int, kw.get('toplist', '').split(','))) if kw.get('toplist') else []

            # Validate parameters
            if size < 1:
                return self.make_json_response({
                    "code": 400, 
                    "status": "error", 
                    "message": "Size must be at least 1", 
                    "data": None
                })

            result = ClassController.get_paginated(dbname, page, size, order_param, search, column_list, top_list)
            return self.make_json_response(result)
        except Exception as e:
            return self.make_json_response(self.handle_exception(e, "getting paginated classes"))

    # === CREATE/UPDATE/DELETE ENDPOINTS ===
    @http.route(['/api/classes'], type='http', auth="none", sitemap=False, cors='*', csrf=False, methods=['POST'])
    def create(self, **kw):
        _logger.info("API: Create new class")
        try:
            dbname = self.get_db_name(kw)
            
            # Parse JSON data from request body
            data = json.loads(http.request.httprequest.data.decode('utf-8'))
            
            # Validate data
            valid, message = Validator.validate_creation_data(data)
            if not valid:
                return self.make_json_response({
                    "code": 400,
                    "status": "error",
                    "message": message,
                    "data": None
                })
                
            result = ClassController.create(dbname, data)
            return self.make_json_response(result)
        except json.JSONDecodeError:
            return self.make_json_response({
                "code": 400,
                "status": "error",
                "message": "Invalid JSON in request body",
                "data": None
            })
        except Exception as e:
            return self.make_json_response(self.handle_exception(e, "creating class"))

    @http.route(['/api/classes/<id>'], type='http', auth="none", sitemap=False, cors='*', csrf=False, methods=['POST'])
    def update(self, id, **kw):
        _logger.info(f"API: Update class, ID: {id}")
        try:
            dbname = self.get_db_name(kw)
            
            # Parse JSON data from request body
            data = json.loads(http.request.httprequest.data.decode('utf-8'))
            
            result = ClassController.update(dbname, id, data)
            return self.make_json_response(result)
        except json.JSONDecodeError:
            return self.make_json_response({
                "code": 400,
                "status": "error",
                "message": "Invalid JSON in request body",
                "data": None
            })
        except Exception as e:
            return self.make_json_response(self.handle_exception(e, "updating class"))

    @http.route(['/api/classes/<id>'], type='http', auth="none", sitemap=False, cors='*', csrf=False, methods=['DELETE'])
    def delete(self, id, **kw):
        _logger.info(f"API: Delete class, ID: {id}")
        try:
            dbname = self.get_db_name(kw)
            result = ClassController.delete(dbname, id)
            return self.make_json_response(result)
        except Exception as e:
            return self.make_json_response(self.handle_exception(e, "deleting class"))

    # === BATCH OPERATIONS ===
    @http.route(['/api/classes/delete'], type='http', auth="none", sitemap=False, cors='*', csrf=False, methods=['DELETE'])
    def mass_delete(self, **kw):
        _logger.info("API: Mass delete classes")
        try:
            dbname = self.get_db_name(kw)
            
            # Parse JSON data from request body
            data = json.loads(http.request.httprequest.data.decode('utf-8'))
            
            if 'idlist' not in data:
                return self.make_json_response({
                    "code": 400,
                    "status": "error",
                    "message": "Missing idlist parameter",
                    "data": None
                })
                
            id_list = data['idlist']
            if not isinstance(id_list, list):
                return self.make_json_response({
                    "code": 400,
                    "status": "error",
                    "message": "idlist must be an array",
                    "data": None
                })
                
            result = ClassController.mass_delete(dbname, id_list)
            return self.make_json_response(result)
        except json.JSONDecodeError:
            return self.make_json_response({
                "code": 400,
                "status": "error",
                "message": "Invalid JSON in request body",
                "data": None
            })
        except Exception as e:
            return self.make_json_response(self.handle_exception(e, "mass deleting classes"))

    @http.route(['/api/classes/<id>/copy'], type='http', auth="none", sitemap=False, cors='*', csrf=False, methods=['POST'])
    def copy(self, id, **kw):
        _logger.info(f"API: Copy class, ID: {id}")
        try:
            dbname = self.get_db_name(kw)
            
            # Parse JSON data from request body for additional settings if needed
                
            result = ClassController.copy(dbname, id)
            return self.make_json_response(result)
        except json.JSONDecodeError:
            return self.make_json_response({
                "code": 400,
                "status": "error",
                "message": "Invalid JSON in request body",
                "data": None
            })
        except Exception as e:
            return self.make_json_response(self.handle_exception(e, f"copying class with ID {id}"))

    # === IMPORT/EXPORT ===
    @http.route(['/api/classes/import'], type='http', auth="none", sitemap=False, cors='*', csrf=False, methods=['POST'])
    def import_data(self, **kw):
        _logger.info("API: Import classes")
        try:
            dbname = self.get_db_name(kw)
            
            # Get file attachment from request
            attachment = http.request.httprequest.files.get('attachment')
            if not attachment:
                return self.make_json_response({
                    "code": 400,
                    "status": "error",
                    "message": "Missing file attachment",
                    "data": None
                })
                
            result = ClassController.import_data(dbname, attachment)
            return self.make_json_response(result)
        except Exception as e:
            return self.make_json_response(self.handle_exception(e, "importing classes"))

    @http.route(['/api/classes/export'], type='http', auth="none", sitemap=False, cors='*', csrf=False, methods=['GET'])
    def export_all(self, **kw):
        _logger.info("API: Export all classes")
        try:
            dbname = self.get_db_name(kw)
            
            # Parse parameters
            export_type = kw.get('type', 'csv').lower()
            column_list = kw.get('columnlist', '').split(',') if kw.get('columnlist') else ['id', 'code', 'name', 'description']
            
            if export_type not in ['csv', 'xlsx']:
                return self.make_json_response({
                    "code": 400,
                    "status": "error",
                    "message": "Invalid export type. Supported types are 'csv' and 'xlsx'",
                    "data": None
                })
                
            buffer, filename = ClassController.export_all(dbname, export_type, column_list)
            
            return http.request.make_response(buffer, headers=[
                ("Content-Type", "application/octet-stream"),
                ("Content-Disposition", http.content_disposition(filename))
            ])
        except Exception as e:
            return self.make_json_response(self.handle_exception(e, "exporting all classes"))

    @http.route(['/api/classes/export/<id>'], type='http', auth="none", sitemap=False, cors='*', csrf=False, methods=['GET'])
    def export_by_id(self, id, **kw):
        _logger.info(f"API: Export class by ID: {id}")
        try:
            dbname = self.get_db_name(kw)
            
            # Parse parameters
            export_type = kw.get('type', 'csv').lower()
            column_list = kw.get('columnlist', '').split(',') if kw.get('columnlist') else ['id', 'code', 'name', 'description']
            
            if export_type not in ['csv', 'xlsx']:
                return self.make_json_response({
                    "code": 400,
                    "status": "error",
                    "message": "Invalid export type. Supported types are 'csv' and 'xlsx'",
                    "data": None
                })
                
            buffer, filename = ClassController.export_by_id(dbname, id, export_type, column_list)
            
            return http.request.make_response(buffer, headers=[
                ("Content-Type", "application/octet-stream"),
                ("Content-Disposition", http.content_disposition(filename))
            ])
        except Exception as e:
            return self.make_json_response(self.handle_exception(e, "exporting class by ID"))

    @http.route(['/api/classes/export'], type='http', auth="none", sitemap=False, cors='*', csrf=False, methods=['POST'])
    def mass_export(self, **kw):
        _logger.info("API: Mass export classes")
        try:
            dbname = self.get_db_name(kw)
            
            # Parse JSON data from request body
            data = json.loads(http.request.httprequest.data.decode('utf-8'))
            
            if 'idlist' not in data:
                return self.make_json_response({
                    "code": 400,
                    "status": "error",
                    "message": "Missing idlist parameter",
                    "data": None
                })
                
            id_list = data['idlist']
            if not isinstance(id_list, list):
                return self.make_json_response({
                    "code": 400,
                    "status": "error",
                    "message": "idlist must be an array",
                    "data": None
                })
                
            # Parse other parameters
            export_type = data.get('type', 'csv').lower()
            column_list = data.get('columnlist', ['id', 'code', 'name', 'description'])
            
            if export_type not in ['csv', 'xlsx']:
                return self.make_json_response({
                    "code": 400,
                    "status": "error",
                    "message": "Invalid export type. Supported types are 'csv' and 'xlsx'",
                    "data": None
                })
                
            buffer, filename = ClassController.mass_export(dbname, id_list, export_type, column_list)
            
            return http.request.make_response(buffer, headers=[
                ("Content-Type", "application/octet-stream"),
                ("Content-Disposition", http.content_disposition(filename))
            ])
        except json.JSONDecodeError:
            return self.make_json_response({
                "code": 400,
                "status": "error",
                "message": "Invalid JSON in request body",
                "data": None
            })
        except Exception as e:
            return self.make_json_response(self.handle_exception(e, "mass exporting classes"))