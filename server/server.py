import BaseHTTPServer

import handler

SERVER_CLS = BaseHTTPServer.HTTPServer
HANDLER_CLS = handler.EideticHTTPHandler
ADDR = ('', 8000)

def serve():
    httpd = SERVER_CLS(ADDR, HANDLER_CLS)
    httpd.serve_forever()
