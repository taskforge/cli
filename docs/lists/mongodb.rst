MongoDB List
============

Why use the MongoDB list
------------------------

MongoDB is a fast document database that's easy to setup. The benefits
of the MongoDB list are ease of use and synchronization of data
between machines that come with using a remote data store.

The downsides of the MongoDB list are:

- Requires setup, securing, and configuration of a MongoDB database
- If a remote data source is desired requires running a server
  accessible from the internet

Configuration
-------------

The MongoDB list takes the following configuration keys:

host
++++

The host where MongoDB is running. By default this is
``localhost``. If using a remote MongoDB instance use the Public IP
address of the server where this is running.

port
++++

The port that MongoDB is listening on. The default value is ``27017``
which is the default port for a MongoDB server.

username
++++++++

The username to use when authenticating to the MongoDB database. This
is only required if auth is configured on the MongoDB
server. Configuring auth for a remote server is recommended.

password
++++++++

The password to use when authenticating to the MongoDB database. This
is only required if auth is configured on the MongoDB
server. Configuring auth for a remote server is recommended.

db
++

This is the database that taskforge will use for storing
tasks. Default value is ``task_forge``. Most users will not need to
set this configuration.

collection
++++++++++

This is the collection that taskforge will use for storing
tasks. Default value is ``tasks``. Most users will not need to set
this configuration.


Example Configuration
---------------------

An example configuration would look like:

.. code::

   [list.config]
   host = 'localhost'
   port = 27017
   username = taskforge
   password = redacted
