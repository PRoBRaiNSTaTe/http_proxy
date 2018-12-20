import socket
import sys
import threading
import os

def usage():
	print("usage : python http_proxy.py <port>")
	print("Sample: python http_proxy.py 8080")

def quit(sock):
	if sys.stdin.readline():
		sock.close()
		os._exit(0)

def RunProxy(browser):
	size=8192
	data=browser.recv(size)

	if not data:
		return

	h=data.split('\r\n')[1]
	host=h[h.index(" ")+1:]
	
	try:
		webserver=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		webserver.connect((host,80))
		webserver.send(data)
	except:	
		return

	while True:
		data=webserver.recv(size)

		if not data:
			webserver.close()
			browser.close()
			return
		else:
			browser.send(data)

if __name__ == "__main__":
	if len(sys.argv)!=2:
		usage()
		sys.exit()

	ip='localhost'
	port=int(sys.argv[1])

	proxy=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	proxy.bind((ip,port))
	proxy.listen(1)
	t=threading.Thread(target=quit,args=(proxy,))
	t.start()

	while True:
		(browser,(host,port))=proxy.accept()
		t=threading.Thread(target=RunProxy,args=(browser,))
		t.start()
