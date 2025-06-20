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

task_status_parser: parser = subparsers.add_parser("status", help="Add a status to a task.")
task_status_parser.add_argument("task_id", help="The task ID to delete")
task_status_parser.add_argument("status_value",
                                choices=["started", "completed"],
                                help="The new status of a task (started or completed)")

# Options
parser.add_argument("--lall", "--listall", dest="command_name", action="store_const", const="lall",
                    help="List all the tasks in the database")

parser.add_argument("--s", "--started", dest="command_name", action="store_const", const="s",
                    help="List all tasks with a STARTED status")

parser.add_argument("--c", "--completed", dest="command_name", action="store_const", const="c",
                    help="List all tasks with a COMPLETED status")

args: parser = parser.parse_args()
