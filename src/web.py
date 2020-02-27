import tornado.web
import tornado.ioloop


class ProblemHandler(tornado.web.RequestHandler):
    def get(self):
        pass


class WebServer:
    def __init__(self):
        self._app = tornado.web.Application([
            (r"/api/v1/problem/namespace/key", ProblemHandler),
        ])

    def start(self, port: int = 8081):
        self._app.listen(port)
        tornado.ioloop.IOLoop.current().start()
