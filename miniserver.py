#!/usr/bin/env python3
import http.server
import socketserver
import cgitb
import os

cgitb.enable()

web_dir = os.path.join(os.path.dirname(__file__), 'web')
os.chdir(web_dir)

PORT = 8091
HOST = "localhost"

handler = http.server.CGIHTTPRequestHandler

httpd = socketserver.TCPServer((HOST, PORT), handler)
httpd.server_name = "pyWebPrint"
httpd.server_port = PORT
print("serving at host ", HOST, ":", PORT)

httpd.serve_forever()

