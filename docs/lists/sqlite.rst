SQLite TaskList
===============

A task list backed by a local sqlite database.

Why Use the SQLite TaskList
---------------------------

The SQLite list is very fast, has 0 external dependencies, and is
shipped by default with Python. This means it can be used with 0
dependencies and 0 configuration. For these reasons it's the default
list when using the taskforge CLI.

Configuration
-------------

The SQLite list takes the following configuration keys:

directory (optional)
++++++++++++++++++++

If provided the SQLite database will a file at path a created by
joining directory with ``tasks.sqlite3``.

file_name (required if directory not provided)
++++++++++++++++++++++++++++++++++++++++++++++

An absolute file path which will be used as the SQLite database file.


Example Configuration
---------------------

An example configuration would look like:

.. code::

   [list.config]
   directory = "~/Taskforge"


Or specifying ``file_name``:

.. code::

   [list.config]
   file_name = "/tmp/taskforge.sqlite"
