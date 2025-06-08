#!/usr/bin/python3
"""This module contains the database connection code."""
import os
import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Using the default PostgreSQL database to create the taskdb database.
DEFAULT_DB_USER: str = os.getenv("DEFAULT_DB_USER")
DEFAULT_DB_PASSWORD: str = os.getenv("DEFAULT_DB_PASSWORD")
DEFAULT_DB_HOST: str = os.getenv("DEFAULT_DB_HOST")
DEFAULT_DB_PORT: str = os.getenv("DEFAULT_DB_PORT")
DEFAULT_DB_NAME: str = os.getenv("DEFAULT_DB_NAME")

# New database details
TASKDB_NAME: str = os.getenv("TASKDB_NAME")
TASKDB_USER: str = os.getenv("TASKDB_USER")
TASKDB_PASSWORD: str = os.getenv("TASKDB_PASSWORD")
TASKDB_HOST: str = os.getenv("TASKDB_HOST")
TASKDB_PORT: str = os.getenv("TASKDB_PORT")


def check_if_db_exists(dbname, user, password, host, port, default_db="postgres") -> bool:
    """Checks if the default PostgreSQL database already exists.
    :param dbname: The database name (should be postgres)
    :param user: The database's username to log into the database (should be postgres)
    :param password: The database's password
    :param host: The database's hostname (should be localhost)
    :param port: The database's port number (should be 5432)
    :param default_db: PostgreSQL installs the postgres database by default.
    :return: True if the database exists, but False if it doesn't.
    """
    connection_check = None
    try:
        connection_check = psycopg2.connect(
            dbname=default_db,
            user=user,
            password=password,
            host=host,
            port=port
        )
        connection_check.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor_check = connection_check.cursor()
        cursor_check.execute(sql.SQL("SELECT 1 FROM pg_database WHERE datname = %s"), (dbname,))
        db_exists = cursor_check.fetchone() is not None
        cursor_check.close()
        return db_exists
    except psycopg2.Error as error:
        print(f"Error occurred while checking if database \"{dbname}\" exists: {error}")
        return False
    finally:
        if connection_check:
            connection_check.close()


def create_database_if_not_exists(db_name_to_create, user, password, host, port,
                                  default_db_connection="postgres") -> bool:
    """Creates the taskdb database if it doesn't exist. It connects to the default database to create the database.
    :param db_name_to_create: The new database's name (taskdb)
    :param user: The database's username
    :param password: The database's password
    :param host: The database's hostname
    :param port: The database's port number
    :param default_db_connection: PostgreSQL installs the postgres database by default.
    :return: True if the database exists, but False if it doesn't.
    """
    connection = None
    if check_if_db_exists(db_name_to_create, user, password, host, port, default_db_connection):
        print(f"The \"{db_name_to_create}\" database already exists.")
        return True

    try:
        # Connect to the default PostgreSQL database
        connection = psycopg2.connect(
            dbname=default_db_connection,
            user=user,
            password=password,
            host=host,
            port=port
        )
        print(f"Connected to the \"{default_db_connection}\" database.")

        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = connection.cursor()
        create_db_query = sql.SQL("CREATE DATABASE {} WITH OWNER {}").format(sql.Identifier(db_name_to_create),
                                                                          sql.Identifier(user))
        cursor.execute(create_db_query)
        print(f"Database \"{db_name_to_create}\" created successfully (or already exists).")
        cursor.close()
        return True
    except psycopg2.Error as error:
        print(f"Error creating database \"{db_name_to_create}\": {error}")
        return False
    finally:
        if connection:
            connection.close()
            print(f"Connection to \"{default_db_connection}\" closed.")


def apply_schema(db_name, user, password, host, port, schema_file_path):
    """Applies the schema from a .sql file to the taskdb database.
    :param db_name: The database's name (taskdb)
    :param user: The database's username
    :param password: The database's password
    :param host: The database's hostname
    :param port: The database's port number
    :param schema_file_path: The schema's pathname
    :return: None
    """
    connection = None
    try:
        connection = psycopg2.connect(
            dbname=db_name,
            user=user,
            password=password,
            host=host,
            port=port,
        )
        cursor = connection.cursor()
        print(f"Connected to \"{db_name}\" to apply schema from \"{schema_file_path}.\"")

        with open(schema_file_path, 'r') as file:
            sql_script: str = file.read()
            cursor.execute(sql_script)
        connection.commit()
        print(f"Schema from \"{schema_file_path}\" applied successfully to \"{db_name}.\"")
        cursor.close()
    except FileNotFoundError:
        print(f"Error: Schema file \"{schema_file_path}\" not found.")
    except psycopg2.Error as error:
        print(f"Error applying schema to \"{db_name}\": {error}")
        if connection:
            connection.rollback()  # Rollback in case of error
    finally:
        if connection:
            connection.close()


if __name__ == "__main__":
    # First step: Create the taskdb database if it doesn't exist
    db_created_successfully: bool = create_database_if_not_exists(
        TASKDB_NAME,
        DEFAULT_DB_USER,
        DEFAULT_DB_PASSWORD,
        DEFAULT_DB_HOST,
        DEFAULT_DB_PORT,
        default_db_connection=DEFAULT_DB_NAME
    )

    if db_created_successfully:
        print(f"\nProceeding to apply schema to \"{TASKDB_NAME}\"...")
        # Second step: Apply the schema to the newly created taskdb database
        apply_schema(
            TASKDB_NAME,
            TASKDB_USER,
            TASKDB_PASSWORD,
            TASKDB_HOST,
            TASKDB_PORT,
            "../../data/schema.sql"
        )
    else:
        print(f"\nDatabase creation for \"{TASKDB_NAME}\" failed. Cannot apply schema.")
