task-query
==========

SYNOPSIS
--------

**task query** [*options*] [<*query*>...]

Search or list tasks in this list.

QUERY will be concatenated using spaces and will be interpreted using the
Taskforge Query Language.

If no query is provided all tasks will be returned.

You can view information about the Taskforge Query Language using 'man task-ql'
or by visiting:

http://taskforge.io/docs/query_language

OPTIONS
-------


.. program:: task query 


.. option:: -o <format>, --output <format>

            How to display the tasks which match the query. Available
            formats are: json, csv, table, text which are described
            below.  [default: table]

OUTPUT FORMATS
--------------

Text output format is the same as for task next where each task will be
printed on one line with the format:

$TASK_ID: $TASK_TITLE

Table output format lists tasks in an ascii table and it looks like this:

| ID  | Created Date  | Completed Date  | Priority  | Title  | Context  |
| --- | ------------- | --------------- | --------- | ------ | -------- |
| $ID | $CREATED_DATE | $COMPLETED_DATE | $PRIORITY | $TITLE | $CONTEXT |

JSON output format will "pretty print" a JSON array of the tasks in the list
to stdout.  They will be properly indented 4 spaces and should be fairly
human readable.  This is useful for migrating from one list implementation
for another as you can redirect this output to a file then import it with:
'task add --from-file $YOUR_JSON_FILE'

CSV will output all task metadata in a csv format. It will write to stdout
so you can use shell redirection to put it into a csv file like so:

'task list --output csv > my_tasks.csv'

This is useful for importing tasks into spreadsheet programs like Excel.



