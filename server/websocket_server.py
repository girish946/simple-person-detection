#!python3
import tornado.ioloop
import tornado.web
import tornado.websocket
    
clients = []

# Handle http response for '/'
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("This is a websocket-server for person detection demo")


# Handle socket connections from device.
# Receive the messages (bounding boxes) fromthe device
# and pass it on to the client for rendering.
class InputWebSocket(tornado.websocket.WebSocketHandler):
    def open(self):
        print("WebSocket opened")

    # Forward the incoming message to all of the clients.
    def on_message(self, message):
        for i in clients:
            i.write_message(message)

    def on_close(self):
        print("WebSocket closed")

# Handle incoming connections from the clinets
class OutWebSocket(tornado.websocket.WebSocketHandler):
    def open(self):
        # Add incoming connection to the client list.
        print("OutWebSocket opened")
        clients.append(self)

    def on_message(self, message):
        pass

    def on_close(self):
        print("WebSocket closed")
        clients.remove(self)


def make_app():
    return tornado.web.Application(
        [
            (r"/", MainHandler),
            (r"/in", InputWebSocket),
            (r"/out", OutWebSocket),
        ]
    )


if __name__ == "__main__":
    app = make_app()
    app.listen(8005)
    tornado.ioloop.IOLoop.current().start()
