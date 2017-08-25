#!/usr/bin/env python

# Derived from dummy-web-server.py in https://gist.github.com/bradmontgomery/2219997

# Portions Copyright (C) 2017 Hin-Tak Leung <htl10@users.sourceforge.net>

"""
Very simple HTTP server in python.

Usage::
    ./wc-mini-web-server.py [<port>]

    point your web browser to http://localhost:[<port>]

Send a GET request::
    curl http://localhost

Send a HEAD request::
    curl -I http://localhost

Send a POST request::
    curl -d "foo=bar&bin=baz" http://localhost

"""
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import SocketServer
import cgi
import wc
from cStringIO import StringIO

class S(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        self.wfile.write("<html><body>")
        self.wfile.write("<h1>hi!</h1>")
        self.wfile.write("<form enctype='multipart/form-data' method='POST'>Choose a file to upload: ")
        self.wfile.write("<input name='inputfile' type='file'/>")
        self.wfile.write("<input type='submit' value='Upload File'/>")
        self.wfile.write("</form>")
        self.wfile.write("</body></html>")

    def do_HEAD(self):
        self._set_headers()
        
    def do_POST(self):
        self._set_headers()
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD':'POST',
                     'CONTENT_TYPE':self.headers['Content-Type'],
            })
        self.wfile.write("<html><body>")
        for field in form.keys():
            field_item = form[field]
            if field_item.filename:
                # The field contains an uploaded file
                file_data = field_item.file.read()
                file_len = len(file_data)
                self.wfile.write('\tUploaded %s as "%s" (%d bytes)<br>\n' % \
                        (field, field_item.filename, file_len))
                opts=['-l','-w','-m']
                results=[wc.count_words_lines_bytes_stdin(file_data,opts)]
                all_output = StringIO(wc.report_str(results,3))
                while True:
                    nl = all_output.readline()
                    if nl == '': break
                    self.wfile.write(nl + "<br>")
            else:
                # Regular form value
                self.wfile.write('\t%s=%s\n' % (field, form[field].value))
        self.wfile.write("</body></html>")
        return

        
def run(server_class=HTTPServer, handler_class=S, port=80):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print 'Starting httpd...'
    httpd.serve_forever()

if __name__ == "__main__":
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
