"""
Usage: task server [options]

Run a taskforge server. Most taskforge commands will automatically
start this server if not running. You can override this behavior by adding:

    [general]
    automatic_server = false

To your Taskforge config file.

Options:
   --unix    Provide a unix socket address to run the server on.
   --listen  Provide a listen interface to listen on. [default: 127.0.0.1]
   --port    Provide the port to listen on for TCP connections. [default: 8000]
   --mock    If provided run the server with a mock task list. This is
             useful for developing and testing clients.
"""

from task_forge.cli.utils import config, load_list
from task_forge.server.server import Server


# We can't use inject_list here since it would be circular with this
# command. inject_list tries to start the server if it's not running.
#
# Additionally we need the server config to set up the server anyway.
@config
def run(_args, cfg=None):
    task_list = load_list(cfg)
    srv_cfg = cfg.get('server')
    server = Server(
        task_list,
        unix_socket=srv_cfg.get('unix_socket'),
        host=srv_cfg.get('host'),
        port=srv_cfg.get('port'),
        secret_file=srv_cfg.get('secret_file'))
    server.run()
