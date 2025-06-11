#!/usr/bin/python3
"""This module contains the CLI logic."""
import os, sys
import psycopg2
from . import commands
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def get_db_connection():
    """Establishes a new database connection.
    :return: A new database connection.
    """
    try:
        connection = psycopg2.connect(
            dbname=os.getenv("TASKDB_NAME"),
            user=os.getenv("TASKDB_USER"),
            password=os.getenv("TASKDB_PASSWORD"),
            host=os.getenv("TASKDB_HOST"),
            port=os.getenv("TASKDB_PORT")
        )
        return connection
    except psycopg2.OperationalError as error:
        print(f"Error: Could not connect to the database. Have you run the setup script in database.py?",
              file=sys.stderr)
        print(f"Details: {error}", file=sys.stderr)
        sys.exit(1)  # Exit if we can't connect


def list_all_tasks() -> tuple[str, str] | str | None:
    """Lists all the tasks in the database.
    :return: A tuple containing both the task and its ID number, a string showing the error, or None.
    """
    connection = get_db_connection()
    try:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT task_id, task, task_status FROM tasks ORDER BY task_id;")
                tasks = cursor.fetchall()
                if not tasks:
                    print("No tasks found.")
                for task_id, task, task_status in tasks:
                    print(f"Task ID: {task_id} | {task} | Task Status: {task_status}")
    except psycopg2.Error as error:
        print(f"Error listing all the tasks in the database: {error}.", file=sys.stderr)
    finally:
        if connection:
            connection.close()


def add_task(description: str) -> str | None:
    """Adds a task to the database.
    :param description: A string of the task's description.
    :return: A string showing the task added to the database successfully, or None.
    """
    connection = get_db_connection()
    add_query: str = "INSERT INTO tasks (task) VALUES (%s);"
    try:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(add_query, (description,))
            print(f"Task \"{description}\" successfully added to the database!")
    except psycopg2.Error as error:
        print(f"Error adding {description} to the database: {error}.", file=sys.stderr)
    finally:
        if connection:
            connection.close()


def delete_task(task_id: int) -> str | None:
    """Deletes a task from the database.
    :param task_id: The ID number of the task as an int.
    :return: A string showing the task deleted from the database successfully, or None.
    """
    connection = get_db_connection()
    delete_query = "DELETE FROM tasks WHERE task_id = %s RETURNING task;"
    try:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(delete_query, (task_id,))
                if cursor.rowcount == 0:
                    print(f"Error: No task found with ID \"{task_id}\".")
                else:
                    print(f"Task \"{task_id}\" successfully deleted from the database!")
    except psycopg2.Error as error:
        print(f"Error deleting {task_id} from the database: {error}.", file=sys.stderr)
    finally:
        if connection:
            connection.close()


def add_task_status(task_id: int, task_status: str) -> str | None:
    """Adds the status to a task via its ID.
    :param task_id: The ID number of the task as an int.
    :param task_status: The task's status (STARTED or COMPLETED)
    :return: A string showing the task deleted from the database successfully, or None.
    """
    connection = get_db_connection()
    task_status_query = "UPDATE tasks SET task_status = %s WHERE task_id = %s;"
    try:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(task_status_query, (task_status.upper(), task_id))
                if cursor.rowcount == 0:
                    print(f"Error: No task found with ID \"{task_id}\".")
                else:
                    print(f"Successfully added a status to Task \"{task_id}\" to {task_status.upper()}")
    except psycopg2.Error as error:
        print(f"Error adding a status to Task {task_id}: {error}.", file=sys.stderr)
    finally:
        if connection:
            connection.close()


def main():
    """Main entry point for the CLI application.
    Parses arguments and calls the appropriate function.
    :return:
    """
    args = commands.args

    if args.command_name is True:
        list_all_tasks()
    elif args.command_name == "add":
        add_task(args.task_description)
    elif args.command_name == "delete":
        try:
            task_id_to_delete: int = int(args.task_id)
            delete_task(task_id_to_delete)
        except ValueError:
            print(f"Error: Task ID must be an integer. You provided: '{args.task_id}'")
    elif args.command_name == "status":
        try:
            task_id_status_to_add: int = int(args.task_id)
            new_status: str = args.status_value
            add_task_status(task_id_status_to_add, new_status)
        except ValueError:
            print(f"Error: Task ID must be an integer. You provided: '{args.task_id}'")
    else:
        commands.parser.print_help()


if __name__ == '__main__':
    main()
