import odoo
import logging
import json
import csv
import io
import pandas as pd
from odoo import http

_logger = logging.getLogger(__name__)

class Students(http.Controller):
    @http.route(['/students/<dbname>/<id>'], type='http', auth="none", sitemap=False, cors='*', csrf=False, methods=['GET'])
    def student_get_by_ID(self, dbname, id, **kw):
        model_name = "students"
        _logger.info(f"Handling request for database: {dbname}, property ID: {id}")
        try:
            registry = odoo.modules.registry.Registry(dbname)
            with registry.cursor() as cr:
                env = odoo.api.Environment(cr, odoo.SUPERUSER_ID, {})
                rec = env[model_name].search([('id', '=', int(id))], limit=1)
                if rec:
                    response = {
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
                            "class_id": rec.class_id.id,
                            "username": rec.username,
                        }   
                    }
                else:
                    response = {
                        "code": 404,
                        "status": "error",
                        "message": "Record not found",
                        "data": "class not found"
                    }
        except Exception as e:
            _logger.error(f"Error handling request: {e}")
            response = {
                "code": 500,
                "status": "error",
                "message": str(e),
                "data": None
            }
        return json.dumps(response)
    @http.route(['/students/<dbname>/page/<int:init>'], type='http', auth="none", sitemap=False, cors='*', csrf=False, methods=['GET'])
    def students_get_by_page(self, dbname, init, **kw):
        model_name = "students"
        _logger.info(f"Handling request for database: {dbname}, page: {init}, params: {kw}")

        try:
            # Parse parameters
            page = max(init, 1)  # Ensure page is at least 1
            size = int(kw.get('size', 10))  # Default 10 records per page
            order_param = kw.get('order', '')  # Example format: [co:1-na:0]
            search = kw.get('search', '').strip()
            column_list = kw.get('columnlist', '').split(',') if kw.get('columnlist') else ['id', 'code', 'fullname', 'dob', 'class_id', 'email', 'phone']
            top_list = list(map(int, kw.get('toplist', '').split(','))) if kw.get('toplist') else []

            # Validate size
            if size < 1:
                return json.dumps({"code": 400, "status": "error", "message": "Size must be at least 1", "data": None})

            # Parse order parameter
            order_by = []
            if order_param:
                order_items = order_param.strip('[]').split('-')
                for item in order_items:
                    try:
                        field, direction = item.split(':')
                        order_by.append(f"{field} {'DESC' if direction == '1' else 'ASC'}")
                    except ValueError:
                        return json.dumps({"code": 400, "status": "error", "message": "Invalid order format", "data": None})

            registry = odoo.modules.registry.Registry(dbname)
            with registry.cursor() as cr:
                env = odoo.api.Environment(cr, odoo.SUPERUSER_ID, {})

                # Build domain for search
                domain = []
                if search:
                    domain = ['|', '|', '|',
                            ('fullname', 'ilike', search),
                            ('dob', 'ilike', search),
                            ('code', 'ilike', search),
                            ('id', 'ilike', search)]

                # Get total count
                total_items = env[model_name].search_count(domain)
                total_pages = (total_items + size - 1) // size

                # Validate page number
                if total_items > 0 and page > total_pages:
                    return json.dumps({
                        "code": 400,
                        "status": "error",
                        "message": f"Page number {page} exceeds total pages {total_pages}",
                        "data": None
                    })

                # Get records for current page
                offset = (page - 1) * size
                records = env[model_name].search(
                    domain,
                    order=','.join(order_by) if order_by else 'id ASC',
                    limit=size,
                    offset=offset
                )

                # Get top list records
                top_records = env[model_name].browse(top_list) if top_list else []

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

                response = {
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
            _logger.error(f"Error handling request: {e}")
            response = {
                "code": 500,
                "status": "error",
                "message": str(e),
                "data": None
            }
        return json.dumps(response)

    @http.route(['/students/<dbname>'], type='http', auth="none", sitemap=False, cors='*', csrf=False, methods=['GET'])
    def students_get_all(self, dbname, **kw):
        model_name = "students"
        _logger.info(f"Fetching all records from database: {dbname}")
        try:
            registry = odoo.modules.registry.Registry(dbname)
            with registry.cursor() as cr:
                env = odoo.api.Environment(cr, odoo.SUPERUSER_ID, {})
                records = env[model_name].search([])  # Remove any search criteria to get all records
                result = []
                for rec in records:
                    result.append({
                        "id": rec.id,
                        "fullname": rec.fullname,
                        "code": rec.code,
                        "dob": rec.dob,
                    })
                response = {
                    "code": 200,
                    "status": "ok",
                    "message": "Records retrieved successfully",
                    "data": result
                }
        except Exception as e:
            _logger.error(f"Error handling request: {e}")
            response = {
                "code": 500,
                "status": "error",
                "message": str(e),
                "data": None
            }
        return json.dumps(response)
    @http.route(['/students/<dbname>'], type='http', auth="none", sitemap=False, cors='*', csrf=False, methods=['POST'])
    def student_create(self, dbname, **kw):
        model_name = "students"
        _logger.info(f"Creating new record in database: {dbname}")
        try:
            # Parse JSON data from request body
            data = json.loads(http.request.httprequest.data.decode('utf-8'))
            required_fields = ['fullname', 'dob', 'code', 'username', 'password']
            
            # Validate required fields
            if not all(field in data for field in required_fields):
                response = {
                    "code": 400,
                    "status": "error",
                    "message": "Missing required fields: fullname, dob, code, username, password",
                    "data": None
                }
                return json.dumps(response)

            registry = odoo.modules.registry.Registry(dbname)
            with registry.cursor() as cr:
                env = odoo.api.Environment(cr, odoo.SUPERUSER_ID, {})
                
                # Check for duplicate code
                existing_record = env[model_name].search([('code', '=', data['code'])], limit=1)
                if existing_record:
                    response = {
                        "code": 400,
                        "status": "error",
                        "message": f"Record with code {data['code']} already exists",
                        "data": None
                    }
                    return json.dumps(response)

                # Create new record with all fields
                new_record = env[model_name].create({
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
                
                response = {
                    "code": 200,
                    "status": "success",
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
            _logger.error(f"Error creating record: {e}")
            response = {
                "code": 500,
                "status": "error",
                "message": str(e),
                "data": None
            }
        return json.dumps(response)
    @http.route(['/students/<dbname>/<id>'], type='http', auth="none", sitemap=False, cors='*', csrf=False, methods=['PUT'])
    def students_update(self, dbname, id, **kw):
        model_name = "students"
        _logger.info(f"Updating record in database: {dbname}, ID: {id}")
        try:
            # Parse JSON data from request body
            data = json.loads(http.request.httprequest.data.decode('utf-8'))
            
            registry = odoo.modules.registry.Registry(dbname)
            with registry.cursor() as cr:
                env = odoo.api.Environment(cr, odoo.SUPERUSER_ID, {})
                record = env[model_name].search([('id', '=', int(id))], limit=1)
                
                if not record:
                    return json.dumps({
                        "code": 404, 
                        "status": "error",
                        "message": f"Record with ID {id} not found",
                        "data": None
                    })

                # If code is being updated, check for duplicates
                if 'code' in data and data['code'] != record.code:
                    existing_record = env[model_name].search([
                        ('code', '=', data['code']),
                        ('id', '!=', int(id))
                    ], limit=1)
                    if existing_record:
                        return json.dumps({
                            "code": 400,
                            "status": "error",
                            "message": f"Record with code {data['code']} already exists",
                            "data": None
                        })
        
                # Update record
                record.write(data)
                cr.commit()

                response = {
                    "code": 200,
                    "status": "success",
                    "message": "Record updated successfully",
                    "data": {
                        "id": record.id
                    }
                }

        except Exception as e:
            _logger.error(f"Error updating record: {e}")
            response = {
                "code": 500,
                "status": "error",
                "message": str(e),
                "data": None
            }
        return json.dumps(response)
    @http.route(['/students/<dbname>/<id>'], type='http', auth="none", sitemap=False, cors='*', csrf=False, methods=['DELETE'])
    def students_delete(self, dbname, id, **kw):
        model_name = "students"
        _logger.info(f"Deleting record in database: {dbname}, ID: {id}")
        try:
            registry = odoo.modules.registry.Registry(dbname)
            with registry.cursor() as cr:
                env = odoo.api.Environment(cr, odoo.SUPERUSER_ID, {})
                record = env[model_name].search([('id', '=', int(id))], limit=1)
                
                if not record:
                    return json.dumps({
                        "code": 404,
                        "status": "error",
                        "message": f"Record with ID {id} not found",
                        "data": None
                    })

                # Delete the record
                record.unlink()
                cr.commit()

                response = {
                    "code": 200,
                    "status": "success",
                    "message": "Record deleted successfully",
                    "data": {
                        "id": int(id)
                    }
                }

        except Exception as e:
            _logger.error(f"Error deleting record: {e}")
            response = {
                "code": 500,
                "status": "error",
                "message": str(e),
                "data": None
            }
        return json.dumps(response)
    @http.route(['/students/<dbname>/delete'], type='http', auth="none", sitemap=False, cors='*', csrf=False, methods=['DELETE'])
    def students_mass_delete(self, dbname, **kw):
        model_name = "students"
        try:
            # Parse JSON data from request body to get idlist
            data = json.loads(http.request.httprequest.data.decode('utf-8'))
            if 'idlist' not in data:
                return json.dumps({
                    "code": 400,
                    "status": "error",
                    "message": "Missing idlist parameter",
                    "data": None
                })

            id_list = data['idlist']
            if not isinstance(id_list, list):
                return json.dumps({
                    "code": 400,
                    "status": "error",
                    "message": "idlist must be an array",
                    "data": None
                })

            _logger.info(f"Mass deleting records in database: {dbname}, IDs: {id_list}")

            registry = odoo.modules.registry.Registry(dbname)
            with registry.cursor() as cr:
                env = odoo.api.Environment(cr, odoo.SUPERUSER_ID, {})
                
                # Convert all IDs to integers
                id_list = [int(id) for id in id_list]
                
                # Find existing records
                records = env[model_name].search([('id', 'in', id_list)])
                
                if not records:
                    return json.dumps({
                        "code": 404,
                        "status": "error",
                        "message": "No records found with the provided IDs",
                        "data": None
                    })

                # Get the IDs of found records
                deleted_ids = records.mapped('id')
                
                # Delete the records
                records.unlink()
                cr.commit()

                response = {
                    "code": 200,
                    "status": "success",
                    "message": f"Successfully deleted {len(deleted_ids)} records",
                    "data": {
                        "ids": deleted_ids
                    }
                }

        except Exception as e:
            _logger.error(f"Error in mass delete: {e}")
            response = {
                "code": 500,
                "status": "error",
                "message": str(e),
                "data": None
            }
        return json.dumps(response)
    @http.route(['/students/<dbname>/copy'], type='http', auth="none", sitemap=False, cors='*', csrf=False, methods=['POST'])
    def students_mass_copy(self, dbname, **kw):
        model_name = "students"
        try:
            # Parse JSON data from request body
            data = json.loads(http.request.httprequest.data.decode('utf-8'))
            if 'idlist' not in data:
                return json.dumps({
                    "code": 400,
                    "status": "error",
                    "message": "Missing idlist parameter",
                    "data": None
                })

            id_list = data['idlist']
            if not isinstance(id_list, list):
                return json.dumps({
                    "code": 400,
                    "status": "error",
                    "message": "idlist must be an array",
                    "data": None
                })
            
            _logger.info(f"Mass copying records in database: {dbname}, IDs: {id_list}")
            
            registry = odoo.modules.registry.Registry(dbname)
            with registry.cursor() as cr:
                env = odoo.api.Environment(cr, odoo.SUPERUSER_ID, {})
                
                # Convert all IDs to integers
                id_list = [int(id) for id in id_list]
                
                # Find existing records
                records = env[model_name].search([('id', 'in', id_list)])
                
                if not records:
                    return json.dumps({
                        "code": 404,
                        "status": "error",
                        "message": "No records found with the provided IDs",
                        "data": None
                    })

                new_records_data = []
                
                # Copy each record
                for record in records:
                    # Generate new code
                    new_code = f"{record.code}-copy"
                    copy_counter = 1
                    while env[model_name].search([('code', '=', new_code)], limit=1):
                        new_code = f"{record.code}-copy{copy_counter}"
                        copy_counter += 1

                    # Create new record
                    new_record = env[model_name].create({
                        'fullname': f"{record.name} (Copy)",
                        'dob': record.dob,
                        'code': new_code
                    })
                    
                    new_records_data.append({
                        "id": new_record.id,
                        "code": new_record.code,
                        "fullname": new_record.name,
                        "dob": new_record.dob
                    })
                
                cr.commit()
                
                response = {
                    "code": 200,
                    "status": "success",
                    "message": f"Successfully copied {len(new_records_data)} records",
                    "data": new_records_data
                }

        except Exception as e:
            _logger.error(f"Error in mass copy: {e}")
            response = {
                "code": 500,
                "status": "error",
                "message": str(e),
                "data": None
            }
        return json.dumps(response)
    @http.route(['/students/<dbname>/import'], type='http', auth="none", sitemap=False, cors='*', csrf=False, methods=['POST'])
    def students_import(self, dbname, **kw):
        model_name = "students"
        try:
            # Get file attachment from request
            attachment = http.request.httprequest.files.get('attachment')
            if not attachment:
                return json.dumps({
                    "code": 400,
                    "status": "error",
                    "message": "Missing file attachment",
                    "data": None
                })

            filename = attachment.filename.lower()
            if not (filename.endswith('.csv') or filename.endswith('.xlsx')):
                return json.dumps({
                    "code": 400,
                    "status": "error",
                    "message": "Only CSV and XLSX files are supported",
                    "data": None
                })

            # Read file content
            file_content = attachment.read()
            data_rows = []

            if filename.endswith('.csv'):
                # Process CSV file
                csv_content = file_content.decode('utf-8')
                csv_file = io.StringIO(csv_content)
                csv_reader = csv.DictReader(csv_file)
                data_rows = list(csv_reader)
            else:
                # Process XLSX file
                excel_file = io.BytesIO(file_content)
                df = pd.read_excel(excel_file)
                data_rows = df.to_dict('records')

            registry = odoo.modules.registry.Registry(dbname)
            with registry.cursor() as cr:
                env = odoo.api.Environment(cr, odoo.SUPERUSER_ID, {})
                imported_records = []

                for row in data_rows:
                    # Convert all keys to strings for consistency
                    row = {str(k): str(v) for k, v in row.items() if pd.notna(v)}

                    # Validate required fields
                    if not all(field in row for field in ['code', 'fullname', 'dob']):
                        continue

                    # Check for duplicate code
                    existing_record = env[model_name].search([('code', '=', row['code'])], limit=1)
                    if existing_record:
                        continue

                    # Create new record
                    new_record = env[model_name].create({
                        'code': row['code'],
                        'fullname': row['fullname'],
                        'dob': row['dob']
                    })

                    imported_records.append({
                        "id": new_record.id,
                        "code": new_record.code,
                        "fullname": new_record.name,
                        "dob": new_record.dob
                    })

                cr.commit()

                response = {
                    "code": 200,
                    "status": "success",
                    "message": f"Successfully imported {len(imported_records)} records",
                    "data": imported_records
                }

        except Exception as e:
            _logger.error(f"Error importing records: {e}")
            response = {
                "code": 500,
                "status": "error",
                "message": str(e),
                "data": None
            }
        return json.dumps(response)
    
    @http.route(['/students/<dbname>/export'], type='http', auth="none", sitemap=False, cors='*', csrf=False, methods=['GET'])
    def students_export(self, dbname, **kw):
        model_name = "students"
        try:
            # Parse parameters
            export_type = kw.get('type', 'csv').lower()
            column_list = kw.get('columnlist', '').split(',') if kw.get('columnlist') else ['id', 'code', 'name', 'description']

            if export_type not in ['csv', 'xlsx']:
                return json.dumps({
                    "code": 400,
                    "status": "error",
                    "message": "Invalid export type. Supported types are 'csv' and 'xlsx'",
                    "data": None
                })

            registry = odoo.modules.registry.Registry(dbname)
            with registry.cursor() as cr:
                env = odoo.api.Environment(cr, odoo.SUPERUSER_ID, {})
                records = env[model_name].search([])

                # Prepare data for export
                data = []
                for rec in records:
                    row = {col: getattr(rec, col, '') for col in column_list}
                    data.append(row)

                if export_type == 'csv':
                    output = io.StringIO()
                    writer = csv.DictWriter(output, fieldnames=column_list)
                    writer.writeheader()
                    writer.writerows(data)
                    buffer = output.getvalue().encode('utf-8')
                    output.close()
                    filename = 'students.csv'
                else:
                    df = pd.DataFrame(data)
                    output = io.BytesIO()
                    df.to_excel(output, index=False)
                    buffer = output.getvalue()
                    output.close()
                    filename = 'students.xlsx'

                # Encode buffer to base64
                # encoded_content = base64.b64encode(buffer).decode('utf-8')

                # response = {
                #     "code": 200,
                #     "status": "success",
                #     "message": "Records exported successfully",
                #     "data": {
                #         "filename": filename,
                #         "content": encoded_content,
                #         "type": export_type
                #     }
                # }

            return http.request.make_response(buffer, headers=[
                    ("Content-Type", "application/octet-stream"),
                    ("Content-Disposition", http.content_disposition(filename))
                ])

        except Exception as e:
            _logger.error(f"Error exporting records: {e}")
            response = {
                "code": 500,
                "status": "error",
                "message": str(e),
                "data": None
            }
            return json.dumps(response)
    @http.route(['/students/<dbname>/export'], type='http', auth="none", sitemap=False, cors='*', csrf=False, methods=['GET'])
    def students_export(self, dbname, **kw):
        model_name = "students"
        try:
            # Parse parameters
            export_type = kw.get('type', 'csv').lower()
            column_list = kw.get('columnlist', '').split(',') if kw.get('columnlist') else ['id', 'code', 'fullname', 'dob']

            if export_type not in ['csv', 'xlsx']:
                return json.dumps({
                    "code": 400,
                    "status": "error",
                    "message": "Invalid export type. Supported types are 'csv' and 'xlsx'",
                    "data": None
                })

            registry = odoo.modules.registry.Registry(dbname)
            with registry.cursor() as cr:
                env = odoo.api.Environment(cr, odoo.SUPERUSER_ID, {})
                records = env[model_name].search([])

                # Prepare data for export
                data = []
                for rec in records:
                    row = {col: getattr(rec, col, '') for col in column_list}
                    data.append(row)

                if export_type == 'csv':
                    output = io.StringIO()
                    writer = csv.DictWriter(output, fieldnames=column_list)
                    writer.writeheader()
                    writer.writerows(data)
                    buffer = output.getvalue().encode('utf-8')
                    output.close()
                    filename = 'students.csv'
                else:
                    df = pd.DataFrame(data)
                    output = io.BytesIO()
                    df.to_excel(output, index=False)
                    buffer = output.getvalue()
                    output.close()
                    filename = 'students.xlsx'

                # Encode buffer to base64
                # encoded_content = base64.b64encode(buffer).decode('utf-8')

                # response = {
                #     "code": 200,
                #     "status": "success",
                #     "message": "Records exported successfully",
                #     "data": {
                #         "filename": filename,
                #         "content": encoded_content,
                #         "type": export_type
                #     }
                # }

            return http.request.make_response(buffer, headers=[
                    ("Content-Type", "application/octet-stream"),
                    ("Content-Disposition", http.content_disposition(filename))
                ])

        except Exception as e:
            _logger.error(f"Error exporting records: {e}")
            response = {
                "code": 500,
                "status": "error",
                "message": str(e),
                "data": None
            }
            return json.dumps(response)    
    @http.route(['/students/<dbname>/export/<id>'], type='http', auth="none", sitemap=False, cors='*', csrf=False, methods=['GET'])
    def students_export_by_id(self, dbname, id, **kw):
        model_name = "students"
        try:
            # Parse parameters
            export_type = kw.get('type', 'csv').lower()
            column_list = kw.get('columnlist', '').split(',') if kw.get('columnlist') else ['id', 'code', 'name', 'description']

            if export_type not in ['csv', 'xlsx']:
                return json.dumps({
                    "code": 400,
                    "status": "error",
                    "message": "Invalid export type. Supported types are 'csv' and 'xlsx'",
                    "data": None
                })

            registry = odoo.modules.registry.Registry(dbname)
            with registry.cursor() as cr:
                env = odoo.api.Environment(cr, odoo.SUPERUSER_ID, {})
                record = env[model_name].search([('id', '=', int(id))], limit=1)

                if not record:
                    return json.dumps({
                        "code": 404,
                        "status": "error",
                        "message": f"Record with ID {id} not found",
                        "data": None
                    })

                # Prepare data for export
                data = [{col: getattr(record, col, '') for col in column_list}]

                if export_type == 'csv':
                    output = io.StringIO()
                    writer = csv.DictWriter(output, fieldnames=column_list)
                    writer.writeheader()
                    writer.writerows(data)
                    buffer = output.getvalue().encode('utf-8')
                    output.close()
                    filename = f'class_{id}.csv'
                else:
                    df = pd.DataFrame(data)
                    output = io.BytesIO()
                    df.to_excel(output, index=False)
                    buffer = output.getvalue()
                    output.close()
                    filename = f'class_{id}.xlsx'

            return http.request.make_response(buffer, headers=[
                    ("Content-Type", "application/octet-stream"),
                    ("Content-Disposition", http.content_disposition(filename))
                ])

        except Exception as e:
            _logger.error(f"Error exporting record: {e}")
            response = {
                "code": 500,
                "status": "error",
                "message": str(e),
                "data": None
            }
            return json.dumps(response)
    @http.route(['/students/<dbname>/export'], type='http', auth="none", sitemap=False, cors='*', csrf=False, methods=['POST'])
    def students_mass_export(self, dbname, **kw):
        model_name = "students"
        try:
            # Parse JSON data from request body to get idlist
            data = json.loads(http.request.httprequest.data.decode('utf-8'))
            if 'idlist' not in data:
                return json.dumps({
                    "code": 400,
                    "status": "error",
                    "message": "Missing idlist parameter",
                    "data": None
                })

            id_list = data['idlist']
            if not isinstance(id_list, list):
                return json.dumps({
                    "code": 400,
                    "status": "error",
                    "message": "idlist must be an array",
                    "data": None
                })

            # Parse other parameters
            export_type = data.get('type', 'csv').lower()
            column_list = data.get('columnlist', ['id', 'code', 'name', 'description'])
            if isinstance(column_list, str):
                column_list = column_list.split(',')

            if export_type not in ['csv', 'xlsx']:
                return json.dumps({
                    "code": 400,
                    "status": "error",
                    "message": "Invalid export type. Supported types are 'csv' and 'xlsx'",
                    "data": None
                })

            registry = odoo.modules.registry.Registry(dbname)
            with registry.cursor() as cr:
                env = odoo.api.Environment(cr, odoo.SUPERUSER_ID, {})
                
                # Convert all IDs to integers
                id_list = [int(id) for id in id_list]
                
                # Find existing records
                records = env[model_name].search([('id', 'in', id_list)])
                
                if not records:
                    return json.dumps({
                        "code": 404,
                        "status": "error",
                        "message": "No records found with the provided IDs",
                        "data": None
                    })

                # Prepare data for export
                data = []
                for rec in records:
                    row = {col: getattr(rec, col, '') for col in column_list}
                    data.append(row)

                if export_type == 'csv':
                    output = io.StringIO()
                    writer = csv.DictWriter(output, fieldnames=column_list)
                    writer.writeheader()
                    writer.writerows(data)
                    buffer = output.getvalue().encode('utf-8')
                    output.close()
                    filename = 'students.csv'
                else:
                    df = pd.DataFrame(data)
                    output = io.BytesIO()
                    df.to_excel(output, index=False)
                    buffer = output.getvalue()
                    output.close()
                    filename = 'students.xlsx'

                return http.request.make_response(buffer, headers=[
                    ("Content-Type", "application/octet-stream"),
                    ("Content-Disposition", http.content_disposition(filename))
                ])

        except Exception as e:
            _logger.error(f"Error exporting records: {e}")
            response = {
                "code": 500,
                "status": "error",
                "message": str(e),
                "data": None
            }
            return json.dumps(response)