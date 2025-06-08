#!/usr/bin/python3
"""This module contains the CLI commands."""
import argparse

parser = argparse.ArgumentParser(
    prog="TaskDB",
    usage="\n%(prog)s [ADD | DELETE] [TASK]\n%(prog)s [OPTION] [TASK ID]",
    description="A CLI To-do list tracking task status in a database.",
)

# Subparsers
subparsers: parser = parser.add_subparsers(title="Commands", dest="command_name", help="Available commands")

add_parser: parser = subparsers.add_parser("add", help="Add a task")
add_parser.add_argument("task_description", help="Description about the task to add in quotation marks")

delete_parser: parser = subparsers.add_parser("delete", help="Delete a task")
delete_parser.add_argument("task_id", help="The task ID to delete")

# Options
parser.add_argument("--lall", "--listall", dest="command_name", action="store_true",
                    help="List all the tasks in the database")

args: parser = parser.parse_args()
