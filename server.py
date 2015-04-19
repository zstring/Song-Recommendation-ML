from autobahn.twisted.websocket import WebSocketServerProtocol, \
    WebSocketServerFactory


class MyServerProtocol(WebSocketServerProtocol):

    def onConnect(self, request):
        print("Client connecting: {0}".format(request.peer))	

    def onOpen(self):
        print("WebSocket connection open.")

    def onMessage(self, payload, isBinary):
	print("Client Called me..."+payload)
        if isBinary:
            print("Binary message received: {0} bytes".format(len(payload)))
        else:
            print("Text message received: {0}".format(payload.decode('utf8')))

        # echo back message verbatim
	count = 1
	while 1==1:
	    #str = ""+count	     
	    self.sendMessage(str(count).encode('utf8'), isBinary)
	    count = count + 1
	    if count == 5:
	    	break;	 

    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {0}".format(reason))


if __name__ == '__main__':

    import sys

    from twisted.python import log
    from twisted.internet import reactor

    log.startLogging(sys.stdout)

    factory = WebSocketServerFactory("ws://localhost:9000", debug=False)
    factory.protocol = MyServerProtocol
    # factory.setProtocolOptions(maxConnections=2)

    reactor.listenTCP(9000, factory)
    reactor.run()

def onDisconnect(self):
    reactor.stop()

