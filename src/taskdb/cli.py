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
        sys.exit(1)


def list_tasks(status_filter: str | None = None):
    """Lists tasks from the database.
    :param status_filter: An optional status ('NOT STARTED', 'STARTED', or 'COMPLETED') for filtering.
    """
    connection = get_db_connection()

    query = "SELECT task_id, task, task_status, task_date_and_time, task_status_date_and_time FROM tasks"
    parameters = []

    if status_filter:
        query += " WHERE task_status = %s"
        parameters.append(status_filter)

    query += " ORDER BY task_id;"

    try:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(query, parameters)
                tasks = cursor.fetchall()
                if not tasks:
                    print("No tasks found matching that criteria.")
                for task_id, task, task_status, task_date_and_time, task_status_date_and_time in tasks:
                    # Provide a default status for display if it's None in the DB
                    status_display = task_status if task_status else "Not Started" or "NOT STARTED"
                    task_added_date: str = task_date_and_time.strftime("%m/%d/%Y")
                    if task_status_date_and_time is None:
                        print(
                            f"Task # {task_id} | {task} | Task Status: {status_display} | Task Added On: {task_added_date} | Task Modified On: Never")
                    else:
                        task_modified_date: str = task_status_date_and_time.strftime("%m/%d/%Y")
                        print(
                            f"Task # {task_id} | {task} | Task Status: {status_display} | Task Added On: {task_added_date} | Task Modified On: {task_modified_date}")
    except psycopg2.Error as error:
        print(f"Error listing tasks: {error}.", file=sys.stderr)
    finally:
        if connection:
            connection.close()


def add_task(description: str) -> str | None:
    """Adds a task, along with the current date and time of the end user's computer, to the database.
    :param description: A string of the task's description.
    :return: A string showing the task added to the database successfully, or None.
    """
    connection = get_db_connection()
    add_query: str = "INSERT INTO tasks (task, task_date_and_time, task_status) VALUES (%s, now(), 'NOT STARTED');"
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
                    print(f"Error: No task found with number \"{task_id}\".")
                else:
                    print(f"Task \"{task_id}\" successfully deleted from the database!")
    except psycopg2.Error as error:
        print(f"Error deleting task number {task_id} from the database: {error}.", file=sys.stderr)
    finally:
        if connection:
            connection.close()


def add_task_status(task_id: int, task_status: str) -> str | None:
    """Adds the status, along with the current date and time of the end user's computer, to a task via its ID.
    :param task_id: The ID number of the task as an int.
    :param task_status: The task's status (NOT STARTED, STARTED, or COMPLETED)
    :return: A string showing the task deleted from the database successfully, or None.
    """
    connection = get_db_connection()
    task_status_query = "UPDATE tasks SET task_status = %s, task_status_date_and_time = now() WHERE task_id = %s;"
    try:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(task_status_query, (task_status.upper(), task_id))
                if cursor.rowcount == 0:
                    print(f"Error: No task found with number \"{task_id}\".")
                else:
                    print(f"Successfully added a status to task number \"{task_id}\" to {task_status.upper()}")
    except psycopg2.Error as error:
        print(f"Error adding a status to task number {task_id}: {error}.", file=sys.stderr)
    finally:
        if connection:
            connection.close()


def update_task_description(task_id: int, new_description: str) -> str | None:
    """Updates the task's description via its ID.
    :param task_id: The ID number of the task as an int.
    :param new_description: The task's new description as a string.
    :return: A string showing the task deleted from the database successfully, or None.
    """
    connection = get_db_connection()
    task_update_query = "UPDATE tasks SET task = %s, task_date_and_time = now() WHERE task_id = %s;"
    try:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(task_update_query, (new_description, task_id))
                if cursor.rowcount == 0:
                    print(f"Error: No task found with number \"{task_id}\".")
                else:
                    print(f"Successfully updated task number {task_id} to \"{new_description}\"")
    except psycopg2.Error as error:
        print(f"Error updating task number {task_id}: {error}.", file=sys.stderr)
    finally:
        if connection:
            connection.close()


def main():
    """Main entry point for the CLI application.
    Parses arguments and calls the appropriate function.
    :return:
    """
    args = commands.args

    if args.command_name == "lall":
        list_tasks()
    elif args.command_name == "s":
        list_tasks("STARTED")
    elif args.command_name == "c":
        list_tasks("COMPLETED")
    elif args.command_name == "n":
        list_tasks("NOT STARTED")
    elif args.command_name == "add":
        add_task(args.task_description)
    elif args.command_name == "delete":
        try:
            task_id_to_delete: int = int(args.task_id)
            delete_task(task_id_to_delete)
        except ValueError:
            print(f"Error: Task ID must be a number. You provided: '{args.task_id}'")
    elif args.command_name == "status":
        try:
            task_id_status_to_add: int = int(args.task_id)
            new_status: str = args.status_value
            add_task_status(task_id_status_to_add, new_status)
        except ValueError:
            print(f"Error: Task ID must be a number. You provided: '{args.task_id}'")
    elif args.command_name == "update":
        try:
            task_id_update: int = int(args.task_id)
            updated_description: str = args.task_description
            update_task_description(task_id_update, updated_description)
        except ValueError:
            print(f"Error: Task ID must be a number. You provided: '{args.task_id}'")
    else:
        commands.parser.print_help()


if __name__ == '__main__':
    main()
