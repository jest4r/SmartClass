import logging
from .db_connection import DatabaseConnection
from ..utils.Export_Factory import ExportFactory
from ..utils.Import_Factory import ImportFactory

_logger = logging.getLogger(__name__)

class StudentController:
    MODEL_NAME = "students"
    
    @staticmethod
    def get_by_id(dbname, id):
        """Get a student by ID"""
        try:
            env, cr = DatabaseConnection.get_env(dbname)
            rec = env[StudentController.MODEL_NAME].search([('id', '=', int(id))], limit=1)
            
            if not rec:
                return {
                    "code": 404,
                    "status": "error",
                    "message": "Record not found",
                    "data": "student not found"
                }
                
            return {
                "code": 200,
                "status": "ok",
                "message": "Record retrieved successfully",
                "data": {
                    "id": rec.id,
                    "fullname": rec.fullname,
                    "code": rec.code,
                    "dob": rec.dob,
                    "sex": rec.sex,
                    "email": rec.email,
                    "address": rec.address,
                    "homecity": rec.homecity,
                    "phone": rec.phone,
                    "class_id": rec.class_id.id if rec.class_id else False,
                    "username": rec.username,
                }
            }
        except Exception as e:
            _logger.error(f"Error retrieving student with id {id}: {e}")
            return {
                "code": 500,
                "status": "error",
                "message": str(e),
                "data": None
            }
    
    @staticmethod
    def get_all(dbname):
        """Get all students"""
        try:
            env, cr = DatabaseConnection.get_env(dbname)
            records = env[StudentController.MODEL_NAME].search([])
            
            result = []
            for rec in records:
                result.append({
                    "id": rec.id,
                    "fullname": rec.fullname,
                    "code": rec.code,
                    "dob": rec.dob,
                })
                
            return {
                "code": 200,
                "status": "ok",
                "message": "Records retrieved successfully",
                "data": result
            }
        except Exception as e:
            _logger.error(f"Error retrieving all students: {e}")
            return {
                "code": 500,
                "status": "error",
                "message": str(e),
                "data": None
            }

    @staticmethod
    def get_paginated(dbname, page, size, order_param, search, column_list, top_list):
        """Get paginated students with filtering and ordering"""
        try:
            env, cr = DatabaseConnection.get_env(dbname)
            
            # Parse order parameter
            order_by = []
            if order_param:
                order_items = order_param.strip('[]').split('-')
                for item in order_items:
                    try:
                        field, direction = item.split(':')
                        order_by.append(f"{field} {'DESC' if direction == '1' else 'ASC'}")
                    except ValueError:
                        return {
                            "code": 400, 
                            "status": "error", 
                            "message": "Invalid order format", 
                            "data": None
                        }

            # Build domain for search
            domain = []
            if search:
                domain = ['|', '|', '|',
                        ('fullname', 'ilike', search),
                        ('dob', 'ilike', search),
                        ('code', 'ilike', search),
                        ('id', 'ilike', search)]

            # Get total count
            total_items = env[StudentController.MODEL_NAME].search_count(domain)
            total_pages = (total_items + size - 1) // size

            # Validate page number
            if total_items > 0 and page > total_pages:
                return {
                    "code": 400,
                    "status": "error",
                    "message": f"Page number {page} exceeds total pages {total_pages}",
                    "data": None
                }

            # Get records for current page
            offset = (page - 1) * size
            records = env[StudentController.MODEL_NAME].search(
                domain,
                order=','.join(order_by) if order_by else 'id ASC',
                limit=size,
                offset=offset
            )

            # Get top list records
            top_records = env[StudentController.MODEL_NAME].browse(top_list) if top_list else []

            # Prepare records data
            records_data = []

            def extract_data(rec):
                return {col: getattr(rec, col, None) for col in column_list}

            # Add top list records first
            seen_ids = set()
            for rec in top_records:
                seen_ids.add(rec.id)
                records_data.append(extract_data(rec))

            # Add paginated records, avoiding duplicates from top_list
            for rec in records:
                if rec.id not in seen_ids:
                    records_data.append(extract_data(rec))

            return {
                "code": 200,
                "status": "success",
                "message": "Records retrieved successfully",
                "data": {
                    "page_info": {
                        "total_items": total_items,
                        "total_pages": total_pages,
                        "current": page,
                        "size": size
                    },
                    "records": records_data
                }
            }
            
        except Exception as e:
            _logger.error(f"Error retrieving paginated students: {e}")
            return {
                "code": 500,
                "status": "error",
                "message": str(e),
                "data": None
            }

    @staticmethod
    def create(dbname, data):
        """Create a new student"""
        try:
            env, cr = DatabaseConnection.get_env(dbname)
            
            # Check for required fields
            required_fields = ['fullname', 'dob', 'code', 'username', 'password']
            if not all(field in data for field in required_fields):
                return {
                    "code": 400,
                    "status": "error",
                    "message": "Missing required fields: fullname, dob, code, username, password",
                    "data": None
                }
            
            # Check for duplicate code
            existing_record = env[StudentController.MODEL_NAME].search([('code', '=', data['code'])], limit=1)
            if existing_record:
                return {
                    "code": 409,
                    "status": "error",
                    "message": f"Record with code {data['code']} already exists",
                    "data": None
                }

            # Create student record
            new_record = env[StudentController.MODEL_NAME].create({
                'fullname': data['fullname'],
                'dob': data['dob'],
                'code': data['code'],
                'username': data['username'],
                'password': data['password'],
                'sex': data.get('sex', ''),
                'email': data.get('email', ''),
                'address': data.get('address', ''),
                'homecity': data.get('homecity', ''),
                'phone': data.get('phone', ''),
                'class_id': int(data.get('class_id', 0)) or False
            })
            
            cr.commit()
            
            return {
                "code": 201,
                "status": "ok",
                "message": "Record created successfully",
                "data": {
                    "id": new_record.id,
                    "fullname": new_record.fullname,
                    "code": new_record.code,
                    "dob": new_record.dob,
                    "username": new_record.username
                }
            }
            
        except Exception as e:
            _logger.error(f"Error creating student: {e}")
            return {
                "code": 500,
                "status": "error",
                "message": str(e),
                "data": None
            }
    
    @staticmethod
    def update(dbname, id, data):
        """Update a student"""
        try:
            env, cr = DatabaseConnection.get_env(dbname)
            record = env[StudentController.MODEL_NAME].search([('id', '=', int(id))], limit=1)
            
            if not record:
                return {
                    "code": 404, 
                    "status": "error",
                    "message": f"Record with ID {id} not found",
                    "data": None
                }

            # If code is being updated, check for duplicates
            if 'code' in data and data['code'] != record.code:
                existing_record = env[StudentController.MODEL_NAME].search([
                    ('code', '=', data['code']),
                    ('id', '!=', int(id))
                ], limit=1)
                if existing_record:
                    return {
                        "code": 400,
                        "status": "error",
                        "message": f"Record with code {data['code']} already exists",
                        "data": None
                    }
        
            # Convert class_id to integer or False
            if 'class_id' in data:
                try:
                    data['class_id'] = int(data['class_id']) if data['class_id'] else False
                except (ValueError, TypeError):
                    data['class_id'] = False
            
            # Update record
            record.write(data)
            cr.commit()

            return {
                "code": 200,
                "status": "success",
                "message": "Record updated successfully",
                "data": {
                    "id": record.id
                }
            }
        except Exception as e:
            _logger.error(f"Error updating student with id {id}: {e}")
            return {
                "code": 500,
                "status": "error",
                "message": str(e),
                "data": None
            }
    
    @staticmethod
    def delete(dbname, id):
        """Delete a student"""
        try:
            env, cr = DatabaseConnection.get_env(dbname)
            record = env[StudentController.MODEL_NAME].search([('id', '=', int(id))], limit=1)
            
            if not record:
                return {
                    "code": 404,
                    "status": "error",
                    "message": f"Record with ID {id} not found",
                    "data": None
                }

            # Delete the record
            record.unlink()
            cr.commit()

            return {
                "code": 200,
                "status": "success",
                "message": "Record deleted successfully",
                "data": {
                    "id": int(id)
                }
            }
        except Exception as e:
            _logger.error(f"Error deleting student with id {id}: {e}")
            return {
                "code": 500,
                "status": "error",
                "message": str(e),
                "data": None
            }
    
    @staticmethod
    def mass_delete(dbname, id_list):
        """Delete multiple students"""
        try:
            env, cr = DatabaseConnection.get_env(dbname)
            
            # Convert all IDs to integers
            id_list = [int(id) for id in id_list]
            
            # Find existing records
            records = env[StudentController.MODEL_NAME].search([('id', 'in', id_list)])
            
            if not records:
                return {
                    "code": 404,
                    "status": "error",
                    "message": "No records found with the provided IDs",
                    "data": None
                }

            # Get the IDs of found records
            deleted_ids = records.mapped('id')
            
            # Delete the records
            records.unlink()
            cr.commit()

            return {
                "code": 200,
                "status": "success",
                "message": f"Successfully deleted {len(deleted_ids)} records",
                "data": {
                    "ids": deleted_ids
                }
            }
        except Exception as e:
            _logger.error(f"Error in mass delete: {e}")
            return {
                "code": 500,
                "status": "error",
                "message": str(e),
                "data": None
            }
    
    @staticmethod
    def mass_copy(dbname, id_list):
        """Copy multiple students"""
        try:
            env, cr = DatabaseConnection.get_env(dbname)
            
            # Convert all IDs to integers
            id_list = [int(id) for id in id_list]
            
            # Find existing records
            records = env[StudentController.MODEL_NAME].search([('id', 'in', id_list)])
            
            if not records:
                return {
                    "code": 404,
                    "status": "error",
                    "message": "No records found with the provided IDs",
                    "data": None
                }

            new_records_data = []
            
            # Copy each record
            for record in records:
                # Generate new code
                new_code = f"{record.code}-copy"
                copy_counter = 1
                while env[StudentController.MODEL_NAME].search([('code', '=', new_code)], limit=1):
                    new_code = f"{record.code}-copy{copy_counter}"
                    copy_counter += 1

                # Create new record with core fields
                new_record = env[StudentController.MODEL_NAME].create({
                    'fullname': f"{record.fullname} (Copy)",
                    'dob': record.dob,
                    'code': new_code,
                    'username': f"{record.username}_copy",
                    'password': record.password,
                    'class_id': record.class_id.id if record.class_id else False
                })
                
                new_records_data.append({
                    "id": new_record.id,
                    "code": new_record.code,
                    "fullname": new_record.fullname,
                    "dob": new_record.dob
                })
            
            cr.commit()
            
            return {
                "code": 200,
                "status": "success",
                "message": f"Successfully copied {len(new_records_data)} records",
                "data": new_records_data
            }
        except Exception as e:
            _logger.error(f"Error in mass copy: {e}")
            return {
                "code": 500,
                "status": "error",
                "message": str(e),
                "data": None
            }

    @staticmethod
    def export_all(dbname, export_type, column_list):
        """Export all students"""
        try:
            env, cr = DatabaseConnection.get_env(dbname)
            
            # Get all records
            records = env[StudentController.MODEL_NAME].search([])
            
            if not records:
                return [], "empty_export.txt"
            
            # Extract data
            data = []
            for record in records:
                record_data = {}
                for col in column_list:
                    record_data[col] = getattr(record, col, '')
                data.append(record_data)
            
            # Use export factory to create the appropriate exporter
            exporter = ExportFactory.create_exporter(export_type)
            buffer, extension = exporter.export(data, column_list)
            
            filename = f"students_export.{extension}"
            return buffer, filename
            
        except Exception as e:
            _logger.error(f"Error exporting all students: {e}")
            raise
    
    @staticmethod
    def export_by_id(dbname, id, export_type, column_list):
        """Export a single student by ID"""
        try:
            env, cr = DatabaseConnection.get_env(dbname)
            
            # Get the record
            record = env[StudentController.MODEL_NAME].search([('id', '=', int(id))], limit=1)
            
            if not record:
                return [], f"student_{id}_not_found.txt"
            
            # Extract data
            data = []
            record_data = {}
            for col in column_list:
                record_data[col] = getattr(record, col, '')
            data.append(record_data)
        # Use export factory to create the appropriate exporter
            exporter = ExportFactory.create_exporter(export_type)
            buffer, extension = exporter.export(data, column_list)
            
            filename = f"class_{id}_export.{extension}"
            return buffer, filename
            
        except Exception as e:
            _logger.error(f"Error exporting class with id {id}: {e}")
            raise
        # Use export factory to create the appropriate exporter
            exporter = ExportFactory.create_exporter(export_type)
            buffer, extension = exporter.export(data, column_list)
            
            filename = f"class_{id}_export.{extension}"
            return buffer, filename
            
        except Exception as e:
            _logger.error(f"Error exporting class with id {id}: {e}")
            raise