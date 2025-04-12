import json
import logging
from odoo import http
from .student_base_controller import StudentBaseController
from ..controllers.student_controller import StudentController
from ..utils.Validator import Validator

_logger = logging.getLogger(__name__)

class StudentAPI(StudentBaseController):
    """API endpoints for student management"""
    
    # === GET ENDPOINTS ===
    @http.route(['/api/students/<id>'], type='http', auth="none", sitemap=False, cors='*', csrf=False, methods=['GET'])
    def get_by_id(self, id, **kw):
        _logger.info(f"API: Get student by ID: {id}")
        try:
            dbname = self.get_db_name(kw)
            result = StudentController.get_by_id(dbname, id)
            return self.make_json_response(result)
        except Exception as e:
            return self.make_json_response(self.handle_exception(e, "getting student by ID"))

    @http.route(['/api/students'], type='http', auth="none", sitemap=False, cors='*', csrf=False, methods=['GET'])
    def get_all(self, **kw):
        _logger.info("API: Get all students")
        try:
            dbname = self.get_db_name(kw)
            result = StudentController.get_all(dbname)
            return self.make_json_response(result)
        except Exception as e:
            return self.make_json_response(self.handle_exception(e, "getting all students"))

    @http.route(['/api/students/page/<int:page>'], type='http', auth="none", sitemap=False, cors='*', csrf=False, methods=['GET'])
    def get_paginated(self, page, **kw):
        _logger.info(f"API: Get paginated students, page: {page}")
        try:
            dbname = self.get_db_name(kw)
            
            # Parse parameters
            size = int(kw.get('size', 10))
            order_param = kw.get('order', '')
            search = kw.get('search', '').strip()
            column_list = kw.get('columnlist', '').split(',') if kw.get('columnlist') else ['id', 'code', 'fullname', 'dob', 'class_id', 'email', 'phone']
            top_list = list(map(int, kw.get('toplist', '').split(','))) if kw.get('toplist') else []

            # Validate parameters
            if size < 1:
                return self.make_json_response({
                    "code": 400, 
                    "status": "error", 
                    "message": "Size must be at least 1", 
                    "data": None
                })

            result = StudentController.get_paginated(dbname, page, size, order_param, search, column_list, top_list)
            return self.make_json_response(result)
        except Exception as e:
            return self.make_json_response(self.handle_exception(e, "getting paginated students"))

    # === CREATE/UPDATE/DELETE ENDPOINTS ===
    @http.route(['/api/students'], type='http', auth="none", sitemap=False, cors='*', csrf=False, methods=['POST'])
    def create(self, **kw):
        _logger.info("API: Create new student")
        try:
            dbname = self.get_db_name(kw)
            
            # Parse JSON data from request body
            data = json.loads(http.request.httprequest.data.decode('utf-8'))
            
            # Validate data
            # valid, message = Validator.validate_creation_data(data)
            # if not valid:
            #     return self.make_json_response({
            #         "code": 400,
            #         "status": "error",
            #         "message": message,
            #         "data": None
            #     })
                
            result = StudentController.create(dbname, data)
            return self.make_json_response(result)
        except json.JSONDecodeError:
            return self.make_json_response({
                "code": 400,
                "status": "error",
                "message": "Invalid JSON in request body",
                "data": None
            })
        except Exception as e:
            return self.make_json_response(self.handle_exception(e, "creating student"))

    @http.route(['/api/students/<id>'], type='http', auth="none", sitemap=False, cors='*', csrf=False, methods=['POST'])
    def update(self, id, **kw):
        _logger.info(f"API: Update student, ID: {id}")
        try:
            dbname = self.get_db_name(kw)
            
            # Parse JSON data from request body
            data = json.loads(http.request.httprequest.data.decode('utf-8'))
            
            result = StudentController.update(dbname, id, data)
            return self.make_json_response(result)
        except json.JSONDecodeError:
            return self.make_json_response({
                "code": 400,
                "status": "error",
                "message": "Invalid JSON in request body",
                "data": None
            })
        except Exception as e:
            return self.make_json_response(self.handle_exception(e, "updating student"))

    @http.route(['/api/students/<id>'], type='http', auth="none", sitemap=False, cors='*', csrf=False, methods=['DELETE'])
    def delete(self, id, **kw):
        _logger.info(f"API: Delete student, ID: {id}")
        try:
            dbname = self.get_db_name(kw)
            result = StudentController.delete(dbname, id)
            return self.make_json_response(result)
        except Exception as e:
            return self.make_json_response(self.handle_exception(e, "deleting student"))

    # === BATCH OPERATIONS ===
    @http.route(['/api/students/delete'], type='http', auth="none", sitemap=False, cors='*', csrf=False, methods=['DELETE'])
    def mass_delete(self, **kw):
        _logger.info("API: Mass delete students")
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
                
            result = StudentController.mass_delete(dbname, id_list)
            return self.make_json_response(result)
        except json.JSONDecodeError:
            return self.make_json_response({
                "code": 400,
                "status": "error",
                "message": "Invalid JSON in request body",
                "data": None
            })
        except Exception as e:
            return self.make_json_response(self.handle_exception(e, "mass deleting students"))

    @http.route(['/api/students/<id>/copy'], type='http', auth="none", sitemap=False, cors='*', csrf=False, methods=['POST'])
    def copy(self, id, **kw):
        _logger.info(f"API: Copy student, ID: {id}")
        try:
            dbname = self.get_db_name(kw)
            
            # Parse JSON data from request body for additional settings if needed
                
            result = StudentController.copy(dbname, id)
            return self.make_json_response(result)
        except json.JSONDecodeError:
            return self.make_json_response({
                "code": 400,
                "status": "error",
                "message": "Invalid JSON in request body",
                "data": None
            })
        except Exception as e:
            return self.make_json_response(self.handle_exception(e, f"copying student with ID {id}"))

    # === IMPORT/EXPORT ===
    @http.route(['/api/students/import'], type='http', auth="none", sitemap=False, cors='*', csrf=False, methods=['POST'])
    def import_data(self, **kw):
        _logger.info("API: Import students")
        try:
            dbname = self.get_db_name(kw)
            
            # Get file attachment from request
            attachment = http.request.httprequest.files.get('file')
            if not attachment:
                return self.make_json_response({
                    "code": 400,
                    "status": "error",
                    "message": "Missing file attachment",
                    "data": None
                })
                
            result = StudentController.import_data(dbname, attachment)
            return self.make_json_response(result)
        except Exception as e:
            return self.make_json_response(self.handle_exception(e, "importing students"))

    @http.route(['/api/students/export'], type='http', auth="none", sitemap=False, cors='*', csrf=False, methods=['GET'])
    def export_all(self, **kw):
        _logger.info("API: Export all students")
        try:
            dbname = self.get_db_name(kw)
            
            # Parse parameters
            export_type = kw.get('type', 'csv').lower()
            column_list = kw.get('columnlist', '').split(',') if kw.get('columnlist') else ['id', 'code', 'fullname', 'dob', 'email', 'phone']
            
            if export_type not in ['csv', 'xlsx']:
                return self.make_json_response({
                    "code": 400,
                    "status": "error",
                    "message": "Invalid export type. Supported types are 'csv' and 'xlsx'",
                    "data": None
                })
                
            buffer, filename = StudentController.export_all(dbname, export_type, column_list)
            
            return http.request.make_response(buffer, headers=[
                ("Content-Type", "application/octet-stream"),
                ("Content-Disposition", http.content_disposition(filename))
            ])
        except Exception as e:
            return self.make_json_response(self.handle_exception(e, "exporting all students"))

    @http.route(['/api/students/export/<id>'], type='http', auth="none", sitemap=False, cors='*', csrf=False, methods=['GET'])
    def export_by_id(self, id, **kw):
        _logger.info(f"API: Export student by ID: {id}")
        try:
            dbname = self.get_db_name(kw)
            
            # Parse parameters
            export_type = kw.get('type', 'csv').lower()
            column_list = kw.get('columnlist', '').split(',') if kw.get('columnlist') else ['id', 'code', 'fullname', 'dob', 'email', 'phone']
            
            if export_type not in ['csv', 'xlsx']:
                return self.make_json_response({
                    "code": 400,
                    "status": "error",
                    "message": "Invalid export type. Supported types are 'csv' and 'xlsx'",
                    "data": None
                })
                
            buffer, filename = StudentController.export_by_id(dbname, id, export_type, column_list)
            
            return http.request.make_response(buffer, headers=[
                ("Content-Type", "application/octet-stream"),
                ("Content-Disposition", http.content_disposition(filename))
            ])
        except Exception as e:
            return self.make_json_response(self.handle_exception(e, "exporting student by ID"))

    @http.route(['/api/students/export'], type='http', auth="none", sitemap=False, cors='*', csrf=False, methods=['POST'])
    def mass_export(self, **kw):
        _logger.info("API: Mass export students")
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
            column_list = data.get('columnlist', ['id', 'code', 'fullname', 'dob', 'email', 'phone'])
            
            if export_type not in ['csv', 'xlsx']:
                return self.make_json_response({
                    "code": 400,
                    "status": "error",
                    "message": "Invalid export type. Supported types are 'csv' and 'xlsx'",
                    "data": None
                })
                
            buffer, filename = StudentController.mass_export(dbname, id_list, export_type, column_list)
            
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
            return self.make_json_response(self.handle_exception(e, "mass exporting students"))