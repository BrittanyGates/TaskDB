#!/usr/bin/python3
"""This module adds the task_status column to the "tasks" database."""
import os, sys
import psycopg2
from dotenv import load_dotenv

# This ensures the script can find the project's root for imports if needed and for loading the .env file correctly.
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
load_dotenv()


def apply_migration():
    """Applies the migration to add the task_status column to the tasks table."""
    connection = None
    try:
        print("Connecting to the database to apply migration...")
        connection = psycopg2.connect(
            dbname=os.getenv("TASKDB_NAME"),
            user=os.getenv("TASKDB_USER"),
            password=os.getenv("TASKDB_PASSWORD"),
            host=os.getenv("TASKDB_HOST"),
            port=os.getenv("TASKDB_PORT")
        )
        with connection.cursor() as cursor:
            create_task_status_column = "ALTER TABLE tasks ADD COLUMN IF NOT EXISTS task_status text DEFAULT NULL;"
            print("Executing: ", create_task_status_column)
            cursor.execute(create_task_status_column)

            set_default_task_status = "UPDATE tasks SET task_status = 'No status' WHERE task_status IS NULL;"
            print("Executing: ", set_default_task_status)
            cursor.execute(set_default_task_status)

        connection.commit()
        print("Migration applied successfully: \"task_status\" column added to \"tasks\" table.")
    except psycopg2.Error as error:
        print(f"Error applying migration: {error}")
        if connection:
            connection.rollback()
    finally:
        if connection:
            connection.close()


if __name__ == "__main__":
    apply_migration()
