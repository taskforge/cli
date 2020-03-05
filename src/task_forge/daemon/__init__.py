# Ignore types because aiohttp does not support them
# type: ignore
"""
Usage: taskforged [options]

Taskforge daemon.

Options:
   -c <file>, --config-file <file> path to the config file to use
"""

from docopt import docopt
from aiohttp import web
from typing import Any

from task_forge import __version__
from task_forge.lists import NotFoundError, TaskList
from task_forge.cli.config import Config
from task_forge.models import Note, Task
from task_forge.ql import Parser, ParseError


class Daemon:
    def __init__(
        self,
        task_list: TaskList,
        loop: Any = None,
        host: str = "localhost",
        port: int = 8000,
    ):
        self.task_list = task_list
        self.host = host
        self.port = port
        self.loop = loop

    async def status(self, request):
        return web.json_response({"message": "available"})

    async def complete_task(self, request):
        task_id = request.match_info.get("id")
        self.task_list.complete(task_id)
        return web.json_response({"message": "success"})

    async def update_task(self, request):
        jsn = await request.json()
        task = Task.from_dict(jsn)
        self.task_list.update(task)
        return web.json_response(task.to_json())

    async def add_note(self, request):
        task_id = request.match_info.get("id", None)
        if task_id is None:
            return web.json_response({"message": "must provide a task id"}, status=400)

        jsn = await request.json()
        note = Note.from_dict(jsn)
        self.task_list.add_note(task_id, note)
        return web.json_response({"message": "success"})

    async def create_tasks(self, request):
        jsn = await request.json()
        if isinstance(jsn, task_list):
            tasks = [Task.from_dict(j) for j in jsn]
            self.task_list.add_multiple(tasks)
        else:
            task = Task.from_dict(jsn)
            self.task_list.add(task)

        return web.json_response({"message": "success"})

    async def get_tasks(self, request):
        task_id = request.match_info.get("id", None)
        if task_id is not None:
            if task_id == "current":
                try:
                    task = self.task_list.current()
                except NotFoundError:
                    return web.json_response(
                        {"message": "no current task found"}, status=404
                    )
            else:
                try:
                    task = self.task_list.find_by_id(task_id)
                except NotFoundError:
                    return web.json_response(
                        {"message": f"no task with {task_id} exists"}, status=404
                    )

            return web.json_response(task.to_json())

        query = request.query.get("query", None)
        if query is not None:
            try:
                if not query:
                    raise ParseError("can not parse an empty query")

                parser = Parser(query)
                tasks = self.task_list.search(parser.parse())
            except ParseError as e:
                return web.json_response(
                    {"message": str(e), "position": e.pos}, status=400
                )
        else:
            tasks = self.task_list.task_list()

        return web.json_response([t.to_json() for t in tasks])

    def run(self):
        app = web.Application(loop=self.loop)
        app.add_routes(
            [
                web.get("/status", self.status),
                web.get("/tasks", self.get_tasks),
                web.post("/tasks", self.create_tasks),
                web.get("/tasks/{id}", self.get_tasks),
                web.put("/tasks", self.update_task),
                web.post("/tasks/{id}/note", self.add_note),
                web.put("/tasks/{id}/complete", self.complete_task),
            ]
        )

        print("Running on: {}:{}".format(self.host, self.port))
        web.run_app(
            app, host=self.host, port=self.port,
        )


def main():
    args = docopt(__doc__, version="taskforged version {}".format(__version__))
    cfgfile = args.get("--config-file")
    config = Config.load(cfgfile)
    task_list_impl = config.load_task_list()
    daemon = Daemon(
        task_list_impl,
        host=config.server.get("host", "localhost"),
        port=config.server.get("port", 8000),
    )
    daemon.run()


if __name__ == "__main__":
    main()
