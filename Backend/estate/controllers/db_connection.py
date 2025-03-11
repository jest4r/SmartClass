import odoo
import logging

_logger = logging.getLogger(__name__)

class DatabaseConnection:
    """Handles database connections and environment setup"""
    
    @staticmethod
    def get_env(dbname):
        """
        Create and return an Odoo environment for the specified database.
        Returns a tuple of (env, cursor)
        """
        try:
            registry = odoo.modules.registry.Registry(dbname)
            cursor = registry.cursor()
            env = odoo.api.Environment(cursor, odoo.SUPERUSER_ID, {})
            return env, cursor
        except Exception as e:
            _logger.error(f"Failed to connect to database {dbname}: {e}")
            raise