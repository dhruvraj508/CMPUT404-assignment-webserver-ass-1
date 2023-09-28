#  coding: utf-8 
import socketserver
import os

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):
    
    def read_file(self, path_requested):
        with open('./www'+path_requested, 'r') as file:
            contents = file.read().encode()
        return contents

    def handle(self):
        self.data = self.request.recv(1024).strip().decode('utf-8')
        # print ("Got a request of: %s\n" % self.data)
        # self.request.sendall(bytearray("OK",'utf-8'))
        
        path  = self.data.split()[1]
        if path[-1] == '/':
            path += 'index.html'

        # check if the requested method is GET, send 405 otherwise. 
        if self.data.split()[0] == "GET":
            # checking if the directory path is valid
            if os.path.exists('./www'+path):
                # if the file is html
                if path.endswith('.html'):
                    self.request.sendall("HTTP/1.1 200 OK\r\n".encode())
                    content = self.read_file(path)
                    self.request.sendall(b'Content-Type: text/html\r\n\r\n')
                    self.request.sendall(content)
                # if the file is css
                elif path.endswith('.css'):
                    self.request.sendall("HTTP/1.1 200 OK\r\n".encode())
                    content = self.read_file(path)
                    self.request.sendall(b'Content-Type: text/css\r\n\r\n')
                    self.request.sendall(content)
                # if not both, send 301 moved perm request. 
                else:
                    self.request.sendall("HTTP/1.1 301 Moved Permanently\r\n".encode())
                    path += '/'
                    self.request.sendall(('Location: http://127.0.0.1:8080' + self.data.split()[1] + '\n' ).encode())  
            # if the path does not exist, send 404 file not found error.
            else:
                self.request.sendall("HTTP/1.1 404 File Not Found\r\n".encode())
        # if the requested method is not GET, we send 405 not allowed
        else:
            self.request.sendall('HTTP/1.1 405 Method Not Allowed\r\n\r\n'.encode())


if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
