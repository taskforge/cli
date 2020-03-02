"""Module containing the implementation of the Taskforge API server."""

from sanic import Sanic
from sanic.views import HTTPMethodView

app = Sanic()


class TaskView(HTTPMethodView):

    async def 
