from typing import Literal
import cv2
from cvzone.HandTrackingModule import HandDetector
import socket

udpIp = "127.0.0.1"
udpPort = 5005
udpMessage = "kaas"



class handTracker:
    def __init__ (
            self,
            maxHands: int = 2,
            detectionConfidence: float = 0.8,
            minTrackingConfidence: float = 0.5 ,
            resolution: tuple[int, int] = (1280, 720),
            showVideo: bool = True,
            dataType: Literal['bbox', 'lmList', 'center'] | list[str] | None = ['bbox', 'center', 'lmList'],
            getHands: Literal['right', 'left', 'both'] = 'left',
            udp: dict[str, int] = {'ip': '127.0.0.1', 'port': 5005}):
        self.maxHands = maxHands
        self.detectionConfidence = detectionConfidence
        self.minTrackingConfidence = minTrackingConfidence
        self.resolution = resolution
        self.showVideo = showVideo
        self.dataType = dataType
        self.getHands = getHands
        self.udp = udp
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


    def __confData(self, rightHand, leftHand):
        if type(self.dataType) == str:
            output = {'righthand': rightHand[self.dataType], 'lefthand': leftHand[self.dataType]}
        elif type(self.dataType) == list:
            output = {'righthand': {}, 'lefthand': {}}
            for dataType in self.dataType:
                output["righthand"][dataType] = rightHand[dataType]
                output["lefthand"][dataType] = leftHand[dataType]
        match self.getHands:
            case 'right':
                return output['righthand']
            case 'left':
                return output['lefthand']
            case _:
                return output


    def handtracker(self):
        detector = HandDetector(maxHands=self.maxHands, detectionCon=self.detectionConfidence, minTrackCon=self.minTrackingConfidence)
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.resolution[0])
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.resolution[1])

        # width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        # height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        # print(width, height)

        while True:
            success, image = cap.read()
            hands, img = detector.findHands(img=image)

            rightHandL = list()
            leftHandL = list()
            if len(hands) == 2:
                for hand in hands:
                    if hand['type'] ==  'Right':
                        rightHandL.append(hand)
                    elif hand['type'] == 'Left':
                        leftHandL.append(hand)

                rightHand = {k: v for d in rightHandL for k, v in d.items()}
                leftHand = {k: v for d in leftHandL for k, v in d.items()}

                if len(rightHand) != 0 and len(leftHand) != 0:

                    data = self.__confData(rightHand, leftHand)
                    self.sock.sendto(str(data).encode(), (self.udp['ip'], self.udp['port']))
            if self.showVideo != True:
                continue

            cv2.imshow('hack tracker', cv2.flip(image, 1))
            cv2.waitKey(1)





if __name__ == "__main__":
    print("UDP target IP: %s" % udpIp)
    print("UDP target port: %s" % udpPort)
    print("message: %s" % udpMessage)
    handTrack = handTracker()
    handTrack.handtracker()