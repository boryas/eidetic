import BaseHTTPServer

import lib.recall.project

class EideticHTTPHandler(BaseHTTPServer.BaseHTTPRequestHandler):

    def _send_headers(self):
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def _send_html(self, title, html):
        self.wfile.write("<html>")
        self.wfile.write("<head><title>{}</title></head>".format(title))
        self.wfile.write("<body>{}</body>".format(html))
        self.wfile.write("</html>")

    def do_HEAD(self):
        self.send_response(200)
        self._send_headers()

    def do_GET(self):
        chunks = self.path.split('/')[1:]
        if len(chunks) == 0:
            self.send_response(404)
        if len(chunks) == 1:
            command = chunks[0]
            self.send_response(200)
            self._send_headers()
        elif len(chunks) == 2:
            command, project = chunks
            self.send_response(200)
            self._send_headers()
            title = '{}:{}'.format(command, project)
            html = lib.recall.project.recall_project(project, format='html')
            self._send_html(title, html)
