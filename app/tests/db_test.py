import unittest

from flask_sqlalchemy import SQLAlchemy
from app import create_app
from app.db_queries import ExecutionQueryService

db_test = SQLAlchemy()
db_service = ExecutionQueryService(db_test)


class TestDbQueries(unittest.TestCase):

    def setUp(self):
        """Set up the application and database before each test."""
        self.app = create_app(db_test)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db_test.create_all()

    def test_db_queries(self):
        """Test the database query functions."""
        # Test add_execution
        execution = db_service.add_execution(5, 10, 0.1)
        self.assertEqual(execution.result, 10)

        # Test get_all_executions
        execution_2 = db_service.add_execution(20, 20, 0.1)
        all_executions = db_service.get_last_executions()
        self.assertEqual(all_executions[0].id, execution_2.id)
        self.assertEqual(all_executions[1].id, execution.id)

        # Test delete_execution
        db_service.delete_execution(execution)
        db_service.delete_execution(execution_2)


if __name__ == "__main__":
    unittest.main()
