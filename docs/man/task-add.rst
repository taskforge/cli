task-add
========

SYNOPSIS
--------

**task add** [*options*] [<*title*>...]

OPTIONS
-------

.. program:: task add

.. option:: -p <priority>, --priority <priority>

            Create the task with the indicated priority, this can be
            an integer or float [default: 1.0]

.. option:: -b <body>, --body <body>

            Body or description of the task

.. option:: -c <context>, --context <context>

            The context in which to create the task. This often maps
            to project or label. For example 'work' or 'home'.

.. option:: -t, --top

            Create this task with the highest priority in the current list

.. option:: -f <file>, --from-file <file>

            Import tasks from the indicated JSON file. If this option
            is provided all other options are ignored.
