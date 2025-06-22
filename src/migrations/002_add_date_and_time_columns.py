#!/usr/bin/python3
"""This module adds the task_date column to the "tasks" database."""
import os, sys
import psycopg2
from dotenv import load_dotenv

# This ensures the script can find the project's root for imports if needed and for loading the .env file correctly.
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
load_dotenv()


def apply_migration():
    """Applies the migration to add the task_date column to the tasks table."""
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
            create_task_date_column = "ALTER TABLE tasks ADD COLUMN IF NOT EXISTS task_date_and_time timestamptz DEFAULT NULL;"
            print("Executing: ", create_task_date_column)
            cursor.execute(create_task_date_column)

            set_default_task_date = "UPDATE tasks SET task_date_and_time = '2025-01-01 12:00 UTC' WHERE task_date_and_time IS NULL;"
            print("Executing: ", set_default_task_date)
            cursor.execute(set_default_task_date)

            create_task_status_date_column = "ALTER TABLE tasks ADD COLUMN IF NOT EXISTS task_status_date_and_time timestamptz DEFAULT NULL;"
            print("Executing: ", create_task_status_date_column)
            cursor.execute(create_task_status_date_column)

            set_default_task_status_date = "UPDATE tasks SET task_status_date_and_time = '2025-01-01 12:00 UTC' WHERE task_status_date_and_time IS NULL;"
            print("Executing: ", set_default_task_status_date)
            cursor.execute(set_default_task_status_date)

        connection.commit()
        print(
            "Migration applied successfully: \"task_date_and_time\" and \"task_status_date_and_time\" columns added to \"tasks\" table.")
    except psycopg2.Error as error:
        print(f"Error applying migration: {error}")
        if connection:
            connection.rollback()
    finally:
        if connection:
            connection.close()


if __name__ == "__main__":
    apply_migration()
