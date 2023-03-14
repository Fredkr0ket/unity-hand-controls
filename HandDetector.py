import cv2
from cvzone.HandTrackingModule import HandDetector


# TODO: add comments for confData dataTypes

class handTracker:
    def __init__ (self, maxHands: int = 2, detectionConfidence: float = 0.8, minTrackingConfidence: float = 0.5 , resolution: tuple[int, int] = (1280, 720), showVideo: bool = False):
        self.maxHands = maxHands
        self.detectionConfidence = detectionConfidence
        self.minTrackingConfidence = minTrackingConfidence
        self.resolution = resolution
        self.showVideo = showVideo

    def __confData(rightHand, leftHand, dataType: str | list[str]):
        # configures the data to the actualy data you wane recieve
        pass
        

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

                    print(rightHand['bbox'])
                    print(leftHand['bbox'])

            if self.showVideo != True:
                continue

            cv2.imshow('hack tracker', cv2.flip(image, 1))
            cv2.waitKey(1)





if __name__ == "__main__":
    handTrack = handTracker()
    handTrack.handtracker()