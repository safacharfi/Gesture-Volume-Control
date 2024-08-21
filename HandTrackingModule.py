import cv2
import mediapipe as mp
import time

class HandDetector:

    # Initialization
    def __init__(self, mode=False, maxHands=2, detectionConf=0.5, trackConf=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionConf = detectionConf
        self.trackConf = trackConf

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(
            static_image_mode=self.mode,
            max_num_hands=self.maxHands,
            min_detection_confidence=self.detectionConf,
            min_tracking_confidence=self.trackConf
        )
        self.mpDraw = mp.solutions.drawing_utils
        self.results = None

    # Detection part
    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img

    # Finding the position of the hands
    def findPosition(self, img, handNb=0, draw=True):
        lmList = []
        if self.results.multi_hand_landmarks:
            handLms = self.results.multi_hand_landmarks[handNb]  # first hand
            for id, lm in enumerate(handLms.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
        return lmList


def main():
    PTime = 0  # Previous time

    # Initialize video capture
    cap = cv2.VideoCapture(0)

    detector = HandDetector()

    while True:
        success, img = cap.read()  # Capture frame-by-frame
        if not success:
            break

        img = detector.findHands(img)
        lmList = detector.findPosition(img)
        if lmList:
            print(lmList[0])  # Print the position of the first landmark

        # Calculate FPS
        cTime = time.time()
        fps = 1 / (cTime - PTime) if (cTime - PTime) != 0 else 0
        PTime = cTime

        # Display FPS on the image
        cv2.putText(img, f'FPS: {int(fps)}', (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 2)

        # Display the resulting frame
        cv2.imshow("img", img)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
