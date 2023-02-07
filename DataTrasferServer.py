from PyQt5 import QtCore, QtWebSockets, QtNetwork, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QAction
from PyQt5.QtCore import QUrl

import sys
import pickle
import json
import time


class DataTrasferServer(QtWidgets.QMainWindow):

    def __init__(self):
        super(DataTrasferServer, self).__init__()

        self.IP = "127.0.0.1"
        self.PORT = 1302
        self.SERVER_NAME = "DataTrasferServer"
        self.clients = []

        self.setWindowTitle(self.SERVER_NAME)

        self.server = QtWebSockets.QWebSocketServer(
            self.SERVER_NAME,  QtWebSockets.QWebSocketServer.NonSecureMode)

        if self.server.listen(QtNetwork.QHostAddress.LocalHost, self.PORT):
            print(
                f"{self.getCurrentTime()} {self.server.serverName()} on IP {self.server.serverAddress().toString()} PORT {str(self.server.serverPort())}")
        else:
            print(
                "Error has occurred... Maybe another server is already running on this PORT?")

        self.server.newConnection.connect(self.onNewConnection)
        self.clientConnection = None

        self.server.acceptError.connect(self.onAcceptError)

        if self.server.isListening():
            print(f"{self.getCurrentTime()} Server is listening... \n")

    def getCurrentTime(self):
        localTime = time.localtime()
        currentTime = time.strftime("%H:%M:%S", localTime)

        return currentTime

    def onNewConnection(self):
        self.clientConnection = self.server.nextPendingConnection()
        self.clients.append(self.clientConnection)

        self.clientConnection.textMessageReceived.connect(
            self.processJSONMessage)
        self.clientConnection.disconnected.connect(self.onDisconnected)

        print(
            f"{self.getCurrentTime()} New client connected: {self.clientConnection.origin()}\n")

    def onDisconnected(self):
        sender = self.sender()
        self.clientConnection = sender
        self.clients.remove(self.clientConnection)
        print(
            f"{self.getCurrentTime()} Client disconnected: {self.clientConnection.origin()}\n")

    def processJSONMessage(self, message):
        self.jsonMessage = json.loads(message)

        self.messageSource = self.jsonMessage["source"]
        self.messageDestination = self.jsonMessage["destination"]

        for client in self.clients:
            if client.origin() == self.messageDestination:
                client.sendTextMessage(message)
                print(
                    f"{self.getCurrentTime()} A message was passed from {self.messageSource} to {self.messageDestination}\n")

    def onAcceptError(accept_error):
        print(f"{self.getCurrentTime()} Accept Error: {accept_error}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    server = DataTrasferServer()
    app.exec_()
