from app.models import Execution
from sqlalchemy.exc import SQLAlchemyError


def add_execution(db, commands_count, result, duration):
    try:
        execution = Execution(commands=commands_count, result=result, duration=duration)
        db.session.add(execution)
        db.session.commit()
        return execution
    except SQLAlchemyError as e:
        db.session.rollback()
        raise Exception(f"Database error: {str(e)}")


def get_all_executions():
    try:
        return Execution.query.limit(100).all()
    except SQLAlchemyError as e:
        raise Exception(f"Database error: {str(e)}")


def delete_execution(db, execution):
    try:
        db.session.delete(execution)
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        raise Exception(f"Database error: {str(e)}")
