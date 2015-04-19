import osc_server_test as osc
from autobahn.twisted.websocket import WebSocketServerProtocol, \
    WebSocketServerFactory
class MyServerProtocol(WebSocketServerProtocol):

    def onConnect(self, request):
        global x
        x = self
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

class ThreadingExample(object):
    """ Threading example class

    The run() method will be started and it will run in the background
    until the application exits.
    """
 
    def __init__(self, interval=1):
        """ Constructor

        :type interval: int
        :param interval: Check interval, in seconds
        """
        self.interval = interval
        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True                            # Daemonize thread
        thread.start()                                  # Start the execution
 
    def run(self):
        """ Method that runs forever """
        # Do something
        global x
        print('Doing something imporant in the background')
        while (x is None):
            time.sleep(1)
            print ("sleeping")
            print ("here")
        osc.init_test(x)

        #x.sendMessage(str(12).encode('utf8'), False)
        time.sleep(self.interval)

if __name__ == '__main__':

    import sys
    import time, threading
    from twisted.python import log
    from twisted.internet import reactor
    x = None
    example = ThreadingExample()
    log.startLogging(sys.stdout)
    factory = WebSocketServerFactory("ws://localhost:9000", debug=False)
    factory.protocol = MyServerProtocol
    # factory.setProtocolOptions(maxConnections=2)

    print "before listen"
    reactor.listenTCP(9000, factory)
    reactor.run()
    print "after run"
            

def onDisconnect(self):
    reactor.stop()

