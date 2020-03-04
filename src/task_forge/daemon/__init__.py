"""Module containing the implementation of the Taskforge API server."""

from aiohttp import web

from task_forge.lists import NotFoundError
from task_forge.cli.config import Config
from task_forge.models import Note, Task
from task_forge.ql import Parser, ParseError


class Daemon(web.Application):
    def __init__(self, list, loop=None):
        self.list = list
        super().__init__(loop=loop)

        self.add_routes(
            [
                web.get("/status", self.status),
                web.get("/tasks", self.get_tasks),
                web.post("/tasks", self.create_tasks),
                web.get("/tasks/{id}", self.get_tasks),
                web.put("/tasks/{id}", self.update_task),
                web.post("/tasks/{id}/note", self.add_note),
                web.put("/tasks/{id}/complete", self.complete_task),
            ]
        )

    async def status(self, request):
        return web.json_response({"message": "available"})

    async def complete_task(self, request):
        task_id = request.match_info.get("id")
        self.list.complete(task_id)
        return web.json_response({"message": "success"})

    async def update_task(self, request):
        jsn = await request.json()
        task = Task.from_dict(jsn)
        self.list.update(task)
        return web.json_response(task.to_json())

    async def add_note(self, request):
        task_id = request.match_info.get("id", None)
        if task_id is None:
            return web.json_response({"message": "must provide a task id"}, status=400)

        jsn = await request.json()
        note = Note.from_dict(jsn)
        self.list.add_note(task_id, jsn)
        return web.json_response({"message": "success"})

    async def create_tasks(self, request):
        jsn = await request.json()
        if isinstance(jsn, list):
            tasks = [Task.from_dict(j) for j in jsn]
            self.list.add_multiple(tasks)
        else:
            task = Task.from_dict(jsn)
            self.list.add(task)

        return web.json_response({"message": "success"})

    async def get_tasks(self, request):
        task_id = request.match_info.get("id", None)
        if task_id is not None:
            if task_id == "current":
                try:
                    task = self.list.current()
                except NotFoundError:
                    return web.json_response(
                        {"message": "no current task found"}, status=404
                    )
            else:
                try:
                    task = self.list.find_by_id(task_id)
                except NotFoundError:
                    return web.json_response(
                        {"message": f"no task with {task_id} exists"}, status=404
                    )

            return web.json_response(task.to_json())

        query = request.query.get("query", None)
        if query is not None:
            try:
                parser = Parser(query)
                tasks = self.list.search(parser.parse())
            except ParseError as e:
                return web.json_response(
                    {"message": str(e), "position": e.pos}, status=400
                )
        else:
            tasks = self.list.list()

        return web.json_response([t.to_json() for t in tasks])

    def run(self, host=None, port=None, sock=None):
        web.run_app(
            self, sock=sock, host=host, port=port,
        )


def main():
    config = Config.load()
    list_impl = config.load_list()
    daemon = Daemon(list_impl)
    daemon.run(host="localhost", port=8000)


if __name__ == "__main__":
    main()
