import logging
from .db_connection import DatabaseConnection
from ..utils.Export_Factory import ExportFactory
from ..utils.Import_Factory import ImportFactory

_logger = logging.getLogger(__name__)

class ClassController:
    MODEL_NAME = "classes"
    
    @staticmethod
    def get_by_id(dbname, id):
        """Get a class by ID"""
        try:
            env, cr = DatabaseConnection.get_env(dbname)
            rec = env[ClassController.MODEL_NAME].search([('id', '=', int(id))], limit=1)
            
            if not rec:
                return {
                    "code": 404,
                    "status": "error",
                    "message": "Record not found",
                    "data": "class not found"
                }
                
            return {
                "code": 200,
                "status": "ok",
                "message": "Record retrieved successfully",
                "data": {
                    "id": rec.id,
                    "name": rec.name,
                    "description": rec.description,
                    "code": rec.code,
                }
            }
        except Exception as e:
            _logger.error(f"Error retrieving class with id {id}: {e}")
            return {
                "code": 500,
                "status": "error",
                "message": str(e),
                "data": None
            }
    
    @staticmethod
    def get_all(dbname):
        """Get all classes"""
        try:
            env, cr = DatabaseConnection.get_env(dbname)
            records = env[ClassController.MODEL_NAME].search([])
            
            result = []
            for rec in records:
                result.append({
                    "id": rec.id,
                    "name": rec.name,
                    "description": rec.description,
                    "code": rec.code,
                })
                
            return {
                "code": 200,
                "status": "ok",
                "message": "Records retrieved successfully",
                "data": result
            }
        except Exception as e:
            _logger.error(f"Error retrieving all classes: {e}")
            return {
                "code": 500,
                "status": "error",
                "message": str(e),
                "data": None
            }

    @staticmethod
    def get_paginated(dbname, page, size, order_param, search, column_list, top_list):
        """Get paginated classes with filtering and ordering"""
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
                        ('name', 'ilike', search),
                        ('description', 'ilike', search),
                        ('code', 'ilike', search),
                        ('id', 'ilike', search)]

            # Get total count
            total_items = env[ClassController.MODEL_NAME].search_count(domain)
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
            records = env[ClassController.MODEL_NAME].search(
                domain,
                order=','.join(order_by) if order_by else 'id ASC',
                limit=size,
                offset=offset
            )

            # Get top list records
            top_records = env[ClassController.MODEL_NAME].browse(top_list) if top_list else []

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
            _logger.error(f"Error retrieving paginated classes: {e}")
            return {
                "code": 500,
                "status": "error",
                "message": str(e),
                "data": None
            }

    @staticmethod
    def create(dbname, data):
        """Create a new class"""
        try:
            env, cr = DatabaseConnection.get_env(dbname)
            
            # Check for duplicate code
            existing_record = env[ClassController.MODEL_NAME].search([('code', '=', data['code'])], limit=1)
            if existing_record:
                return {
                    "code": 409,
                    "status": "error",
                    "content": f"Record with code {data['code']} already exists",
                    "data": None
                }

            # Create record
            next_id = env[ClassController.MODEL_NAME].search([], order='id desc', limit=1).id + 1 if env[ClassController.MODEL_NAME].search([], order='id desc', limit=1) else 1
            new_record = env[ClassController.MODEL_NAME].create({
                'id': next_id,
                'name': data['name'],
                'description': data['description'],
                'code': data['code']
            })
            cr.commit()
            
            return {
                "code": 201,
                "status": "ok",
                "message": "Record created successfully",
                "data": {
                    "id": new_record.id
                }
            }
            
        except Exception as e:
            _logger.error(f"Error creating class: {e}")
            return {
                "code": 500,
                "status": "error",
                "message": str(e),
                "data": None
            }
    
    @staticmethod
    def update(dbname, id, data):
        """Update a class"""
        try:
            env, cr = DatabaseConnection.get_env(dbname)
            record = env[ClassController.MODEL_NAME].search([('id', '=', int(id))], limit=1)
            
            if not record:
                return {
                    "code": 404, 
                    "status": "error",
                    "message": f"Record with ID {id} not found",
                    "data": None
                }

            # If code is being updated, check for duplicates
            if 'code' in data and data['code'] != record.code:
                existing_record = env[ClassController.MODEL_NAME].search([
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
            _logger.error(f"Error updating class with id {id}: {e}")
            return {
                "code": 500,
                "status": "error",
                "message": str(e),
                "data": None
            }
    
    @staticmethod
    def delete(dbname, id):
        """Delete a class"""
        try:
            env, cr = DatabaseConnection.get_env(dbname)
            record = env[ClassController.MODEL_NAME].search([('id', '=', int(id))], limit=1)
            
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
            _logger.error(f"Error deleting class with id {id}: {e}")
            return {
                "code": 500,
                "status": "error",
                "message": str(e),
                "data": None
            }
    
    @staticmethod
    def mass_delete(dbname, id_list):
        """Delete multiple classes"""
        try:
            env, cr = DatabaseConnection.get_env(dbname)
            
            # Convert all IDs to integers
            id_list = [int(id) for id in id_list]
            
            # Find existing records
            records = env[ClassController.MODEL_NAME].search([('id', 'in', id_list)])
            
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
    def copy(dbname, id):
        """Copy a single class by ID"""
        try:
            env, cr = DatabaseConnection.get_env(dbname)
            
            # Find existing record
            record = env[ClassController.MODEL_NAME].search([('id', '=', int(id))], limit=1)
            
            if not record:
                return {
                    "code": 404,
                    "status": "error",
                    "message": f"Record with ID {id} not found",
                    "data": None
                }

            # Generate new code
            new_code = f"{record.code}-copy"
            copy_counter = 1
            while env[ClassController.MODEL_NAME].search([('code', '=', new_code)], limit=1):
                new_code = f"{record.code}-copy{copy_counter}"
                copy_counter += 1

            # Create new record
            new_record = env[ClassController.MODEL_NAME].create({
                'name': f"{record.name} (Copy)",
                'description': record.description,
                'code': new_code
            })
            
            cr.commit()
            
            return {
                "code": 200,
                "status": "success",
                "message": "Record copied successfully",
                "data": {
                    "id": new_record.id,
                    "code": new_record.code,
                    "name": new_record.name,
                    "description": new_record.description
                }
            }
        except Exception as e:
            _logger.error(f"Error copying class with id {id}: {e}")
            return {
                "code": 500,
                "status": "error",
                "message": str(e),
                "data": None
            }

    @staticmethod
    def export_all(dbname, export_type, column_list):
        """Export all classes"""
        try:
            env, cr = DatabaseConnection.get_env(dbname)
            
            # Get all records
            records = env[ClassController.MODEL_NAME].search([])
            
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
            
            filename = f"classes_export.{extension}"
            return buffer, filename
            
        except Exception as e:
            _logger.error(f"Error exporting all classes: {e}")
            raise
    
    # @staticmethod
    # def export_by_id(dbname, id, export_type, column_list):
    #     """Export a single class by ID"""
    #     try:
    #         env, cr = DatabaseConnection.get_env(dbname)
            
    #         # Get the record
    #         record = env[ClassController.MODEL_NAME].search([('id', '=', int(id))], limit=1)
            
    #         if not record:
    #             return [], f"class_{id}_not_found.txt"
            
    #         # Extract data
    #         data = []
    #         record_data = {}
    #         for col in column_list:
    #             record_data[col] = getattr(record, col, '')
    #         data.append(record_data)
            
    #         # Use export factory to create the appropriate exporter
    #         exporter = ExportFactory.create_exporter(export_type)
    #         buffer, extension = exporter.export(data, column_list)
            
    #         filename = f"class_{id}_export.{extension}"
    #         return buffer, filename
            
    #     except Exception as e:
    #         _logger.error(f"Error exporting class with id {id}: {e}")
    #         raise
    
    @staticmethod
    def mass_export(dbname, id_list, export_type, column_list):
        """Export multiple classes"""
        try:
            env, cr = DatabaseConnection.get_env(dbname)
            
            # Convert all IDs to integers
            id_list = [int(id) for id in id_list]
            
            # Get the records
            records = env[ClassController.MODEL_NAME].search([('id', 'in', id_list)])
            
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
            
            filename = f"classes_selected_export.{extension}"
            return buffer, filename
            
        except Exception as e:
            _logger.error(f"Error in mass export: {e}")
            raise
    
    @staticmethod
    def import_data(dbname, attachment):
        """Import classes from file"""
        try:
            env, cr = DatabaseConnection.get_env(dbname)
            
            # Get the file extension
            filename = attachment.filename
            extension = filename.split('.')[-1].lower()
            
            # Use import factory to create the appropriate importer
           
            importer = ImportFactory.create_importer(extension)
            
            # Read the file content
            file_content = attachment.read()
            
            # Import data
            data_rows = importer.import_data(file_content)
            
            if not data_rows:
                return {
                    "code": 400,
                    "status": "error",
                    "message": "No data found in the file",
                    "data": None
                }
            
            # Process each row
            created_records = []
            updated_records = []
            skipped_records = []
            
            for row in data_rows:
                code = row.get('code')
                
                if not code:
                    skipped_records.append({
                        "row": row,
                        "reason": "Missing code"
                    })
                    continue
                
                # Check if record exists
                existing_record = env[ClassController.MODEL_NAME].search([('code', '=', code)], limit=1)
                
                if existing_record:
                    # Update existing record
                    try:
                        existing_record.write({
                            'name': row.get('name', existing_record.name),
                            'description': row.get('description', existing_record.description)
                        })
                        updated_records.append({
                            "id": existing_record.id,
                            "code": code
                        })
                    except Exception as e:
                        skipped_records.append({
                            "row": row,
                            "reason": str(e)
                        })
                else:
                    # Create new record
                    try:
                        new_record = env[ClassController.MODEL_NAME].create({
                            'name': row.get('name', ''),
                            'description': row.get('description', ''),
                            'code': code
                        })
                        created_records.append({
                            "id": new_record.id,
                            "code": code,
                            "description": new_record.description
                        })
                    except Exception as e:
                        skipped_records.append({
                            "row": row,
                            "reason": str(e)
                        })
            
            cr.commit()
            
            return {
                "code": 200,
                "status": "success",
                "message": f"Import completed: {len(created_records)} created, {len(updated_records)} updated, {len(skipped_records)} skipped",
                "data": {
                    "created": created_records,
                    "updated": updated_records,
                    "skipped": skipped_records
                }
            }
        except Exception as e:
            _logger.error(f"Error importing classes: {e}")
            return {
                "code": 500,
                "status": "error",
                "message": str(e),
                "data": None
            }