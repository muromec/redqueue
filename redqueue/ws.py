from uuid import uuid4 as uuid
import json

from tornado.httpserver import HTTPServer
from tornado.web import Application, StaticFileHandler
from tornado.websocket import WebSocketHandler

from redqueue import task

class WSTask(task.Task):
    key = 'task:ws'
    connections = {}
    def on_data(self, data):
        c = self.connections.get(data['_id'])
        if not c:
            return

        c.write_message(json.dumps(data['payload']))

task.runnable_tasks.append(WSTask)

class Handler(WebSocketHandler):
    def open(self):
        print "New connection opened."
        self._id = str(uuid())
        self.write_message(self._id)

        WSTask.connections[self._id] = self
        print WSTask.connections

    def on_message(self, message):
        print message
        #self.write_message(u"You said: " + message)

    def on_close(self):
        print "Connection closed."
        WSTask.connections.pop(self._id, None)


class Server(HTTPServer):
    def __init__(self):
        app = Application([
            ("/_ws", Handler),
            (r'/static/(.*)', StaticFileHandler, {'path': 'static'}),
        ])

        HTTPServer.__init__(self, app)
