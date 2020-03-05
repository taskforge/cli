Taskforge Server
================

This design describes the behavior and API of the Taskforge Server

.. contents::

Goals
-----

- Use Unix sockets and / or network sockets for communication
- No knowledge of common server runners like ``gunicorn`` is necessary to run
  the server
- Use websockets as the primary communication method, this allows other
  languages to use standard packages to communicate without the overhead of
  designing, maintaining, and implementing a custom protocol.
- Configurable socket name, listen address / port, log file.
- Config file can disable use of server since not every list will need it and
  some users would prefer to skip the overhead.
- A TaskList implementation that speaks the server protocol
- Docker container which can be used to run the Taskforge server
 

Design
------

The Task class already has a good API for serializing and deserializing JSON.
Given that and the fact we're using websockets, this server will speak and deal
with tasks using JSON. It will expose an API that matches closely that of the
List API.

Server Configuration
++++++++++++++++++++

With the ``task`` CLI client the configuration for the server will add a new
section to the file. It will have the following options and defaults:

.. code::

   [server]
   # By default use a unix socket not a network socket
   socket = /var/run/taskforge.sock
   # host = localhost
   # port = 8080
   # Only used with network communication
   # secret_file = ~/.taskforge.d/server_secret

Additionally, it will add the following options to the new "general" section.

.. code::

   [general]
   # If true the server will not be started and Taskforge will run using TaskList
   # implementations directly.
   # disable_server = false
   # Only used with network server communication
   # secret_file = ~/.taskforge.d/server_secret



Server Message Structure
++++++++++++++++++++++++
    
The server will speak JSON messages which have the following structure:

.. code::

   {
       "method": "$METHOD_NAME",
       "payload": $OBJECT // Task as JSON: {}, or Array of Tasks as JSON [{}]
                          // depending on method as described below.
   }

Server Methods
++++++++++++++

The server will expose methods which map directly to the TaskList API. The only
exception being there will be two methods ``search`` and ``query``. Search will
take an AST as JSON. The ``query`` method will take the string query as the
payload which it will then lex and parse before sending to the TaskList
implementation.

The specification for each method is described in detail below.

All methods which return something return a message with the form:

.. code::

   {
       "status": "success",
       "payload": $OBJECT // Task as JSON: {}, or Array of Tasks as JSON [{}]
                          // depending on method as described below.
   }

For methods that return nothing they will simply return a message indicating
success or failure:

.. code::

   {
       "status": "success"
   }

Any time a server method fails the payload will have ``"status": "failure"`` and
will have a key ``"message"`` which contains an error message:

.. code::

   {
       "status": "failure",
       "message": "Why this method failed"
   }

This message is not guaranteed to be human readable but will often be.

``add``
^^^^^^^

Add is used for adding tasks. A minimal add message looks like the following:

.. code::

   {
       "method": "add",
       "payload": {"title": "write server design document"}
   }

All other task metadata can be provided as usual with the exception of
the "id" field. A more complete example looks like:

.. code::

   {
       "method": "add",
       "payload": {
           "title": "write server design document",
           "body": "it should be complete",
           "priority": 2.5,
           "context": "designs"
       }
   }


``add_multiple``
^^^^^^^^^^^^^^^^

Add multiple works identically to add above however it's payload is an array of
Task objects instead of a single Task.

.. code::

   {
       "method": "add",
       "payload": [{"title": "write server design document"}]
   }


``list``
^^^^^^^^

``list`` returns all of the tasks in the TaskList implementation. It only requires
the method name in the message.

.. code::

   {
       "method": "list"
   }

``find_by_id``
^^^^^^^^^^^^^^

``find_by_id`` returns the task with the given ID. The payload for this message
is an object with a single key ``id`` which is the string of the ID you want to
find.

.. code::

   {
       "method": "find_by_id",
       "payload": {"id": "$TASK_ID}
   }

``current``
^^^^^^^^^^^

``current`` returns the current task. It only requires the method name in the
message.

.. code::

   {
       "method": "current"
   }


``complete``
^^^^^^^^^^^^

``complete`` completes the task with the given ID. The payload for this message is
an object with a single key ``id`` which is the string of the ID you want to
find.

.. code::

   {
       "method": "complete",
       "payload": {"id": "$TASK_ID}
   }


``update``
^^^^^^^^^^

``update`` updates the task with the ID ``"id"``. The payload for this message
is a full task object with all the fields and values you would like set on the
Task. ``"id"`` and ``title`` are required and if not provided the operation will
fail.

.. code::

   {
       "method": "update",
       "payload": {
           "id": "$TASK_ID,
           "title": "updated task",
           // ... other fields as required
       }
   }




``add_note``
^^^^^^^^^^^^

``add_note`` will add a note to the task with ``"task_id"``. The message
required looks like:

.. code::

   {
       "method": "add_note",
       "payload": {
           "task_id": "ID_OF_TASK_TO_ADD_TO",
           "note": {"body": "This is a note"}
       }
   }

``search``
^^^^^^^^^^

``search`` takes a JSON representation of the Taskfoge Query Language AST and
uses it to search the TaskList implementation. The payload looks like:

.. code::

   {
       "method": "search",
       "payload": {
           "expression": {
               "left": {
                   "token": {
                       "token_type": "STRING",
                       "literal": "completed"
                   },
                   "value": "completed"
               },
               "right": {
                   "token": {
                       "token_type": "BOOLEAN",
                       "literal": "false"
                   },
                   "value": false
               },
               "operator": {
                   "token_type": "EQ",
                   "literal": "="
               }
            }
       }
   }



``query``
^^^^^^^^^

``query`` takes a JSON object with a single key ``query`` which has a string
value of a Taskfoge Query Language query. The server will then do Parsing of the
query returning any parsing errors or a payload of all the matching tasks.

.. code::

   {
       "method": "query",
       "payload": {"query": "completed = false"}
   }


