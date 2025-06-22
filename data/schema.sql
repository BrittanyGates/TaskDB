-- Create the TASKS table
CREATE TABLE IF NOT EXISTS tasks (
    task_id integer GENERATED ALWAYS AS IDENTITY,
    task text NOT NULL,
    task_status text NULL,
    task_date_and_time timestamptz NULL,
    task_status_date_and_time timestamptz NULL
);