taskforged
==========

SYNOPSIS
--------

Run a taskforge server daemon. Most taskforge commands will automatically
start this server if not running. You can override this behavior by adding:

    [general]
    automatic_server = false

To your Taskforge config file.

OPTIONS
-------

.. program:: taskforged

.. option::  --verbose

             Turn on verbose logging

.. option:: --unix=<socket_path>

            Provide a unix socket address to run the server on.

.. option:: --host=<ip_addr>

            Provide a listen interface to listen on. [default:
            127.0.0.1]

.. option:: --port=<port>

            Provide the port to listen on for TCP
            connections. [default: 8000]

.. option:: --mock

            If provided run the server with a mock task list. This is
                         useful for developing and testing clients.


.. option:: --secret=<secret>

            Provide the shared secret clients must provide when
                         connecting.

.. option:: --secret-file=<secret_file_path>

            Path to a file containing the shared secret clients must
                                     provide when connecting.

.. option:: --config-file=<config_file_path>

            Path to a config file to use.

