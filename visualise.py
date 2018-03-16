#!/usr/bin/python3

import tornado.web

class Hello(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self):

        text = ""

        self.render("consumer1.html", title = "plot", text = text)

class NoCacheStaticFileHandler(tornado.web.StaticFileHandler):
    def set_extra_headers(self, path):
        self.set_header("Cache-control", "no-cache")

application = tornado.web.Application([
    (r"/", Hello),
    (r"/static/(.*)", NoCacheStaticFileHandler, {
        "path": "admin/img/"
    }),
])

if __name__ == "__main__":
    application.listen(8080)
    tornado.ioloop.IOLoop.instance().start()

