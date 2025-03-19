import logging
import csv
import io
import pandas as pd

_logger = logging.getLogger(__name__)

class ImportFactory:
    @staticmethod
    def create_importer(file_extension):
        """Factory method to create the appropriate importer"""
        if file_extension.lower() == 'csv':
            return CSVImporter()
        elif file_extension.lower() in ['xlsx', 'xls']:
            return ExcelImporter()
        else:
            raise ValueError(f"Unsupported file extension: {file_extension}")

class BaseImporter:
    def import_data(self, file_content):
        """Import data from the file content"""
        raise NotImplementedError()

class CSVImporter(BaseImporter):
    def import_data(self, file_content):
        """Import data from CSV content"""
        try:
            csv_content = file_content.decode('utf-8')
            csv_file = io.StringIO(csv_content)
            csv_reader = csv.DictReader(csv_file)
            data_rows = list(csv_reader)
            return data_rows
        except Exception as e:
            _logger.error(f"Error importing from CSV: {e}")
            raise

class ExcelImporter(BaseImporter):
    def import_data(self, file_content):
        """Import data from Excel content"""
        try:
            excel_file = io.BytesIO(file_content)
            df = pd.read_excel(excel_file)
            data_rows = df.to_dict('records')
            return data_rows
        except Exception as e:
            _logger.error(f"Error importing from Excel: {e}")
            raise