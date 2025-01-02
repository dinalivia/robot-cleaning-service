import unittest
from app import create_app, db
from app.db_queries import add_execution, get_all_executions, delete_execution


class TestDbQueries(unittest.TestCase):

    def setUp(self):
        """Set up the application and database before each test."""
        self.app = create_app(db)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        """Clean up database and context after each test."""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_db_queries(self):
        """Test the database query functions."""
        # Test add_execution
        execution = add_execution(db, 5, 10, 0.1)
        self.assertEqual(execution.result, 10)

        # Test get_all_executions
        execution_2 = add_execution(db, 20, 20, 0.1)
        all_executions = get_all_executions()
        self.assertGreaterEqual(len(all_executions), 2)

        # Test delete_execution
        delete_execution(db, execution)
        delete_execution(db, execution_2)


if __name__ == "__main__":
    unittest.main()
