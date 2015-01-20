import SocketServer,os
# coding: utf-8

# Copyright 2013 Abram Hindle, Eddie Antonio Santos,Lin Tong, Bowen qi
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


class MyWebServer(SocketServer.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        newReq= self.data.split()
        url= newReq[1]
        path=os.getcwd()+"/www"+url
        indexHtml=path+"index.html"
        baseCss=path+"base.css"
        deepCss=path+"deep.css"
        responseG=""
#return true if path refers to an existing path
        if not (os.path.lexists(path)):
            responseG=self.NoResponse()
            self.request.sendall(responseG)
            self.request.sendall("\r\n")
	    Error_message=("<html><body>Error 404, please go back<body><html>")
	    self.request.sendall(Error_message)
#else check is it home directory, if its w, we are in www folder, otherwise its deep folder
        elif path[-1]=="/":
            if path[-2]=="w":
                fp=open(indexHtml).read()
                fp2=open(baseCss).read()
                responseG=self.response_is_good(indexHtml,"html")
                open_web=self.open_page(responseG,fp,fp2)
            elif path[-2] =="p":
                fp=open(indexHtml).read()
                fp2=open(deepCss).read()
                responseG=self.response_is_good(indexHtml,"html")
                open_web=self.open_page(responseG,fp,fp2)
	elif path[-4:]=="deep"and path[-1] is not "/":
		print(path)
                fp=open(path+"/index.html").read()
                fp2=open(path+"/deep.css").read()
                responseG=self.response_is_good(indexHtml,"html")
                open_web=self.open_page(responseG,fp,fp2)
#check /.. 404      
        elif "/.." in path:
            responseG=self.NoResponse()
            self.request.sendall(responseG)
            self.request.sendall("\r\n")
	    Error_message=("<html><body>Error 404, please go back<body><html>")
	    self.request.sendall(Error_message)
#check  is it a directory
        elif not(os.path.isdir(path)):
            name,extension =os.path.splitext(path)
#check is it html file or css file
            if extension ==".html":
                fp=open(path).read()
                get_css=os.path.dirname(path)
                responseG=self.response_is_good(path,"html")
                if get_css[-1] == "w":
                    fp2= open(get_css+"/base.css").read()
                    open_web=self.open_page(responseG,fp,fp2)  
                else:
                    fp2= open(get_css+"/deep.css").read()
                    open_web=self.open_page(responseG,fp,fp2)  
            elif  extension ==".css":
                fp=open(path,"r+")
                fp=fp.read()
                responseG=self.response_is_good(path,"css")
                self.request.sendall(responseG)
#open webpage
    def open_page(self,response,file1,file2):
            self.request.sendall(response)
            self.request.sendall("\r\n")
            self.request.sendall(file1)
            self.request.sendall("<style> "+file2+"<style>")
#send http header
    def response_is_good(self,path,content_type):
        http_header = "HTTP/1.1 200 OK\r\n" + "Content-Type: text/" + content_type + ""
        return http_header
#send 404 error
    def NoResponse(self):
        Notfind_header = "HTTP/1.1 404 Not Found\r\n" + "Content-Type:\n"
        return Notfind_header

	

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    SocketServer.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = SocketServer.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()

