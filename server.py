from http.server import HTTPServer, SimpleHTTPRequestHandler
import os

class RewritingHTTPRequestHandler(SimpleHTTPRequestHandler):
    """
    Serve responses but from /output/<filename> instead of /roadmap-to-html/<filename>
    """
    def translate_path(self, path):
        path = super(self.__class__, self).translate_path(path)

        # remove the filesystem path up to this file
        path = path.replace(os.path.dirname(os.path.realpath(__file__)), "")

        # then replace the beginning /roadmap-to-html/<filename> with
        # /output/<filename>
        path = path.replace("/roadmap-to-html/", "/output/")

        # reappend the OS path since it's needed by the server
        path = os.path.dirname(os.path.realpath(__file__)) + path
        return path

def run(server_class=HTTPServer, handler_class=RewritingHTTPRequestHandler):
    server_address = ('', 8000)
    httpd = server_class(server_address, handler_class)
    print("Listening on 0.0.0.0 Port 8000")
    httpd.serve_forever()

run()
