from app import create_app, db
from app.db_queries import add_execution, get_first_execution, delete_execution


def test_db_queries():
    app = create_app(db)

    with app.app_context():
        db.create_all()

        # Test add_execution
        execution = add_execution(db, 5, 10, 0.1)
        assert execution.result == 10

        # Test get_first_execution
        fetched_execution = get_first_execution(db)
        print(fetched_execution)
        breakpoint()
        assert fetched_execution.result == 10

        # Test delete_execution
        delete_execution(db, fetched_execution)
        assert get_first_execution(db) is None


if __name__ == "__main__":
    test_db_queries()
