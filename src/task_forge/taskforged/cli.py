"""
Usage: taskforged [options]

Run a taskforge server daemon. Most taskforge commands will automatically
start this server if not running. You can override this behavior by adding:

    [general]
    automatic_server = false

To your Taskforge config file.

Options:
   --unix=<socket_path>  Provide a unix socket address to run the server on.
   --host=<ip_addr>      Provide a listen interface to listen on. [default: 127.0.0.1]
   --port=<port>         Provide the port to listen on for TCP connections. [default: 8000]

   --mock                If provided run the server with a mock task list. This is
                         useful for developing and testing clients.


   --secret=<secret>     Provide the shared secret clients must provide
                         when connecting.

   --secret_file=<secret_file_path>  Path to a file containing the
                                     shared secret clients must
                                     provide when connecting.
"""

from docopt import docopt

from task_forge.cli.utils import config, load_list
from task_forge.server.server import Server


# We can't use inject_list here since it would be circular with this
# command. inject_list tries to start the server if it's not running.
#
# Additionally we need the server config to set up the server anyway.
@config
def run(cfg=None):
    """Add the server command to the parser."""
    args = docopt(__doc__, version='taskforged version 0.3.0')
    task_list = load_list(cfg)
    srv_cfg = cfg.get('server')
    server = Server(
        task_list,
        unix_socket=args.get('unix', srv_cfg.get('unix_socket')),
        host=args.get('host', srv_cfg.get('host')),
        port=args.get('port', srv_cfg.get('port')),
        secret=args.get('secret', srv_cfg.get('secret')),
        secret_file=args.get('secret_file', srv_cfg.get('secret_file')))
    server.run()
