import logging
import csv
import io
import pandas as pd

_logger = logging.getLogger(__name__)

class ExportFactory:
    @staticmethod
    def create_exporter(export_type):
        """Factory method to create the appropriate exporter"""
        if export_type.lower() == 'csv':
            return CSVExporter()
        elif export_type.lower() == 'xlsx':
            return ExcelExporter()
        else:
            raise ValueError(f"Unsupported export type: {export_type}")

class BaseExporter:
    def export(self, data, column_list):
        """Export data to the specified format"""
        raise NotImplementedError()

class CSVExporter(BaseExporter):
    def export(self, data, column_list):
        """Export data to CSV format"""
        try:
            output = io.StringIO()
            writer = csv.DictWriter(output, fieldnames=column_list)
            writer.writeheader()
            writer.writerows(data)
            buffer = output.getvalue().encode('utf-8')
            output.close()
            return buffer, 'csv'
        except Exception as e:
            _logger.error(f"Error exporting to CSV: {e}")
            raise

class ExcelExporter(BaseExporter):
    def export(self, data, column_list):
        """Export data to Excel format"""
        try:
            df = pd.DataFrame(data)
            output = io.BytesIO()
            df.to_excel(output, index=False)
            buffer = output.getvalue()
            output.close()
            return buffer, 'xlsx'
        except Exception as e:
            _logger.error(f"Error exporting to Excel: {e}")
            raise