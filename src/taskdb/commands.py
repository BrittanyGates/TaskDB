#!/usr/bin/python3
"""This module contains the CLI commands."""
import argparse

parser = argparse.ArgumentParser(
    prog="TaskDB",
    usage="\n%(prog)s [ADD | DELETE] [TASK]\n%(prog)s [OPTION] [TASK NUM]",
    description="A CLI To-do list tracking task status in a database.",
)

# Subparsers
subparsers: parser = parser.add_subparsers(title="Commands", dest="command_name", help="Available commands")

add_parser: parser = subparsers.add_parser("add", help="Add a task")
add_parser.add_argument("task_description", metavar='"Task Description"',
                        help="Description about the task to add in quotation marks")

delete_parser: parser = subparsers.add_parser("delete", help="Delete a task")
delete_parser.add_argument("--task-num=", dest="task_id", metavar='Task Number', type=int,
                           help="The task number to delete (Example Usage: --task-num=1)")

task_status_parser: parser = subparsers.add_parser("status", help="Add a status to a task")
task_status_parser.add_argument("--task-num=", dest="task_id", metavar='Task Number', type=int,
                                help="The task number to update the status (Example Usage: --task-num=1)")
task_status_parser.add_argument("status_value",
                                choices=["not-started", "started", "completed"],
                                help="The new status of a task (NOT STARTED, STARTED, COMPLETED)")

update_task_parser: parser = subparsers.add_parser("update", help="Update a task's description")
update_task_parser.add_argument("--task-num=", dest="task_id", metavar='Task Number', type=int,
                                help="The task number to update (Example Usage: --task-num=1)")
update_task_parser.add_argument("task_description", metavar='"Task Description"',
                                help="Description about the task to update in quotation marks")

# Options
parser.add_argument("--lall", "--listall", dest="command_name", action="store_const", const="lall",
                    help="List all the tasks in the database")

parser.add_argument("--s", "--started", dest="command_name", action="store_const", const="s",
                    help="List all tasks with a STARTED status")

parser.add_argument("--c", "--completed", dest="command_name", action="store_const", const="c",
                    help="List all tasks with a COMPLETED status")

parser.add_argument("--n", "--not-started", dest="command_name", action="store_const", const="n",
                    help="Lists all tasks with a NOT STARTED status")

args: parser = parser.parse_args()
