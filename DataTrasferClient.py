from PyQt5 import QtCore, QtWebSockets, QtNetwork
from PyQt5.QtCore import QUrl, QCoreApplication, QTimer
from PyQt5.QtWidgets import QApplication
from PyQt5 import QtWidgets
from PyQt5.uic import loadUi

import numpy as np

import sys
import time
import pickle
import copy
import cv2
import json

from jsonutils import createJSONFrame


class DataTrasferClient(QtWidgets.QMainWindow):

    def __init__(self, data):
        super(DataTrasferClient, self).__init__()
        # loadUi("P:\\DataTransferApp\\ui\\DataTrasferClient.ui", self)
        self.setWindowTitle("DataTrasferClient")

        self.IP = "127.0.0.1"
        self.PORT = 1302
        self.CLIENT_NAME = "Detection"
        self.DESTINATION_CLIENT_NAME = "Recognition"

        self.dataToSend = data

        self.client = QtWebSockets.QWebSocket(
            self.CLIENT_NAME, QtWebSockets.QWebSocketProtocol.Version13, None)
        self.client.error.connect(self.error)

        self.url = f"ws://{self.IP}:{str(self.PORT)}"
        self.client.open(QUrl(self.url))
        self.client.pong.connect(self.onPong)

        self.client.textMessageReceived.connect(
            self.processJSONMessage)

    def processJSONMessage(self, message):
        self.receivedMessage = message

        self.jsonMessage = json.loads(message)
        self.data = self.jsonMessage["data"]
        self.type = self.jsonMessage["type"]
        self.size = self.jsonMessage["size"]

        self.rawData = eval(self.data)

        self.finalData = pickle.loads(self.rawData)

        print(
            f"{self.currentTime()} Received message from {self.jsonMessage['source']}")
        print(f"Data type: {self.type}")
        print(f"Data Size: {self.size} B\n")

    def currentTime(self):
        localtime = time.localtime()
        current_time = time.strftime("%H:%M:%S", localtime)

        return current_time

    def doPing(self):
        self.client.ping()

    def onPong(self, elapsedTime, payload):
        print(
            f"{self.currentTime()} DataTrasferClient {self.CLIENT_NAME} is connected to server\n")

    def sendMessage(self):
        data = self.dataToSend

        JSONFrame = createJSONFrame(
            self.CLIENT_NAME, self.DESTINATION_CLIENT_NAME, data)
        JSONFrame = JSONFrame.getJSONFrame()

        self.client.sendTextMessage(JSONFrame)

        jsonMessage = json.loads(JSONFrame)
        destination = jsonMessage["destination"]

        print(f"{self.currentTime()} Sended message to {destination}")

        self.dataType = type(data)
        print(f"Data type: {self.dataType}")

        self.dataSize = json.loads(JSONFrame)["size"]
        print(f"Size: {self.dataSize} B\n")

    def error(self, error_code):
        print(f"Error excepted! Error code: {error_code}")
        print(self.client.errorString())
        # TODO: Uwaga!
        quit_app()

    def close(self):
        self.client.close()


def quit_app():
    print("Exiting...")
    QCoreApplication.quit()


def ping():
    client.doPing()


def sendMessage():
    client.sendMessage()


if __name__ == "__main__":
    global client

    data = ['Test', [324, 5234, 436, 44], 98, 'Test']

    app = QApplication(sys.argv)
    client = DataTrasferClient(data)
    # client.show()

    QTimer.singleShot(100, ping)

# --------------------------------------------------------------
    timer = QTimer()
    timer.timeout.connect(sendMessage)
    timer.setInterval(2000)
    timer.start()
# --------------------------------------------------------------

    app.exec_()
