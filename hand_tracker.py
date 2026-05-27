import cv2
import mediapipe as mp

class HandTracker:
    def __init__(self, detectionCon=0.8, trackCon=0.5):
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(
            max_num_hands=1,
            min_detection_confidence=self.detectionCon,
            min_tracking_confidence=self.trackCon
        )
        self.mpDraw = mp.solutions.drawing_utils
        self.tipIds = [4, 8, 12, 16, 20]

    def findHands(self, img):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img

    def findPosition(self, img, draw=False):
        lmList = []
        if self.results.multi_hand_landmarks:
            hand = self.results.multi_hand_landmarks[0]
            h, w, _ = img.shape

            for id, lm in enumerate(hand.landmark):
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([id, cx, cy])

                if draw:
                    cv2.circle(img, (cx, cy), 5, (255, 0, 0), cv2.FILLED)

        return lmList

    def fingersUp(self):
        fingers = []

        if not self.results.multi_hand_landmarks:
            return []

        hand = self.results.multi_hand_landmarks[0]
        if hand.landmark[self.tipIds[0]].x < hand.landmark[self.tipIds[0] - 1].x:
            fingers.append(1)
        else:
            fingers.append(0)
        for id in range(1, 5):
            if hand.landmark[self.tipIds[id]].y < hand.landmark[self.tipIds[id] - 2].y:
                fingers.append(1)
            else:
                fingers.append(0)

        return fingers