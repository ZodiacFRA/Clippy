import select
import socket

from CONFIG import SERVER_ADDRESS, BUFFER_SIZE, GREEN, RED, CYAN, YELLOW
from utils import ClientObject


class NetworkManager(object):
    def __init__(self, clients, logger):
        self.clients = clients
        self.logger = logger
        self.inputs = []
        self.outputs = []
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setblocking(False)
        self.server.bind(SERVER_ADDRESS)
        self.server.listen(5)
        self.logger.log('Listening on: {}'.format(SERVER_ADDRESS), GREEN)
        self.inputs.append(self.server)
        self.clients_nbr = 0
        self.prev_clients_nbr = 0

    def do_turn(self):
        """First check if max number of connections is reached (1024, imposed by select())
        if so, don't listen for new connections
        When conns number returns below the threshold, start listening again
        Then perform the socket handling (read, write, exceptions)"""
        # print('-> waiting for network event')
        self.clients_nbr = len(self.clients)
        if self.clients_nbr != self.prev_clients_nbr:
            if self.clients_nbr % 100 == 0:
                self.logger.log("{} connections".format(self.clients_nbr), CYAN)
            if 990 < self.clients_nbr < 1000:
                self.logger.log("{} clients, approaching max connections number".format(self.clients_nbr), YELLOW)
        if self.inputs or self.outputs:
            readable, writable, exceptional = select.select(self.inputs, self.outputs, self.inputs)
            self.handle_readable(readable)
            self.handle_writable(writable)
            self.handle_exceptional(exceptional)
        self.prev_clients_nbr = self.clients_nbr

    def handle_readable(self, readable):
        for s in readable:
            if s is self.server:
                # A "readable" server socket is ready to accept a connection
                conn, client_address = s.accept()
                if self.clients_nbr >= 1000:
                    self.logger.log(
                        "{} Connection refused: Max connections reached ({})".format(client_address, len(self.clients)),
                        RED
                    )
                    self.delete_client(conn)
                else:
                    conn.setblocking(0)
                    self.inputs.append(conn)
                    self.clients[conn] = ClientObject(conn)
                    self.logger.log("New connection from {}".format(client_address), GREEN, True)
            else:
                try:
                    msg = s.recv(BUFFER_SIZE).decode('utf-8')
                except ConnectionResetError:
                    self.logger.log(
                        "Unexpected client disconnection (happens when clients disconnect too fast after connection)",
                        RED
                    )
                    self.delete_client(s)
                else:
                    if msg:
                        # A readable client socket has data
                        self.logger.log('received "{}" from {}'.format(msg, s.getpeername()), CYAN, True)
                        self.clients[s].todo = msg
                        # Add output channel for response
                        if s not in self.outputs:
                            self.outputs.append(s)
                    else:
                        # Interpret empty result as closed connection, try / except for brutal client disconnection
                        self.delete_client(s)
                        try:
                            self.logger.log("closing {} after reading no data".format(s.getpeername()), GREEN, True)
                        except OSError:
                            self.logger.log("closing socket after reading no data", GREEN, True)
                        # Stop listening for input on the connection

    def handle_writable(self, writable):
        """Handle writable sockets, send message if there is one
        remove the socket from writable select list if there is nothing more to send
        socket will be added back in handle_readable if the client sends another message
        """
        for s in writable:
            client = self.clients.get(s, None)
            if not client:
                return
            response = client.result
            if response:
                self.logger.log('sending "{}" to {}'.format(response, s.getpeername()), CYAN, True)
                s.send(response.serialize().encode())
                self.clients[s].result = None
            else:  # No messages waiting so stop checking for writability.
                self.outputs.remove(s)

    def handle_exceptional(self, exceptional):
        """Handle exceptional conditions"""
        for s in exceptional:
            self.logger.log('Exceptional condition for {}'.format(s.getpeername()), YELLOW)
            # Stop listening for input on the connection
            self.delete_client(s)

    def delete_client(self, s):
        """Used to safely delete a client Object, remove it from the NM lists and close its connection"""
        if s in self.outputs:
            self.outputs.remove(s)
        if s in self.inputs:
            self.inputs.remove(s)
        if s in self.clients:
            client_obj = self.clients.pop(s)
            del client_obj
        try:
            s.shutdown(socket.SHUT_RDWR)
        except OSError:
            pass
        s.close()


