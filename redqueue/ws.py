from tornado.httpserver import HTTPServer
from tornado.web import Application, StaticFileHandler
from tornado.websocket import WebSocketHandler

from redqueue import task

class WSTask(task.Task):
    key = 'task:ws'
    connections = []
    def on_data(self, data):
        print 'task data', data
        for c in self.connections:
            c.write_message(data)

task.runnable_tasks.append(WSTask)

class Handler(WebSocketHandler):
    def open(self):
        print "New connection opened."
        WSTask.connections.append(self)

    def on_message(self, message):
        print message
        self.write_message(u"You said: " + message)


    def on_close(self):
        print "Connection closed."


class Server(HTTPServer):
    def __init__(self):
        app = Application([
            ("/_ws", Handler),
            (r'/static/(.*)', StaticFileHandler, {'path': 'static'}),
        ])

        HTTPServer.__init__(self, app)
