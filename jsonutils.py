import json
import sys
import pickle


class createJSONFrame():

    def __init__(self, source, destination, rawData):
        super(createJSONFrame, self).__init__()

        self.source = source
        self.destination = destination

        self.rawData = rawData
        self.data = pickle.dumps(self.rawData)

        self.type = type(self.rawData)

        self.size = sys.getsizeof(self.data)

        self.frame = {
            "source": f"{self.source}",
            "destination": f"{self.destination}",
            "data": f"{self.data}",
            "type": f"{self.type}",
            "size": f"{self.size}"
        }

        self.rawJSON = json.dumps(self.frame, indent=2)

    def getJSONFrame(self): return self.rawJSON
