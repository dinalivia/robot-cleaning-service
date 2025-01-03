from app.models import Execution
from sqlalchemy.exc import SQLAlchemyError


class ExecutionQueryService:
    def __init__(self, db):
        self.db = db

    def add_execution(self, commands_count, result, duration):
        try:
            execution = Execution(
                commands=commands_count, result=result, duration=duration
            )
            self.db.session.add(execution)
            self.db.session.commit()
            return execution
        except SQLAlchemyError as e:
            self.db.session.rollback()
            raise Exception(f"Database error: {str(e)}")

    def get_last_executions(self):
        try:
            return Execution.query.order_by(Execution.timestamp.desc()).limit(100).all()
        except SQLAlchemyError as e:
            raise Exception(f"Database error: {str(e)}")

    def delete_execution(self, execution):
        try:
            self.db.session.delete(execution)
            self.db.session.commit()
        except SQLAlchemyError as e:
            self.db.session.rollback()
            raise Exception(f"Database error: {str(e)}")


# def add_execution(db, commands_count, result, duration):
#     try:
#         execution = Execution(commands=commands_count, result=result, duration=duration)
#         db.session.add(execution)
#         db.session.commit()
#         return execution
#     except SQLAlchemyError as e:
#         db.session.rollback()
#         raise Exception(f"Database error: {str(e)}")


# def get_all_executions():
#     try:
#         return Execution.query.limit(100).all()
#     except SQLAlchemyError as e:
#         raise Exception(f"Database error: {str(e)}")


# def delete_execution(db, execution):
#     try:
#         db.session.delete(execution)
#         db.session.commit()
#     except SQLAlchemyError as e:
#         db.session.rollback()
#         raise Exception(f"Database error: {str(e)}")
