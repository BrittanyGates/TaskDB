-- Create the TASKS table
CREATE TABLE IF NOT EXISTS tasks (
    task_id integer GENERATED ALWAYS AS IDENTITY,
    task text NOT NULL
);
