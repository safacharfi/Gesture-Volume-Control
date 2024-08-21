import cv2
import time
import numpy as np
import math
import handTrackingModule as htm
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# Set camera resolution
wCam, hCam = 640, 480

# Initialize the camera
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

pTime = 0
detector = htm.HandDetector(detectionConf=0.7)  # Make sure it's a hand !!

# Initialize audio control
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))  # Corrected line

volRange = volume.GetVolumeRange()
minVol = volRange[0]
maxVol = volRange[1]

if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

while True:
    success, img = cap.read()
    if not success:
        print("Error: Could not read frame.")
        break

    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)

    if len(lmList) >= 9:  # Ensure there are enough landmarks
        # We need the 4 and 8 landmarks: thumb and index
        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]

        cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 15, (255, 0, 255), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)

        # Calculate the center of the line
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
        cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)

        # Calculate the length between the two points to change the volume
        length = math.hypot(x2 - x1, y2 - y1)

        # Convert hand range (50-300) to volume range (-65 to 0)
        vol = np.interp(length, [50, 120], [minVol, maxVol])
        volume.SetMasterVolumeLevel(vol, None)  # Corrected line

        if length < 50:
            cv2.circle(img, (cx, cy), 15, (0, 255, 0), cv2.FILLED)

    # Calculate FPS
    cTime = time.time()
    fps = 1 / (cTime - pTime) if (cTime - pTime) > 0 else 0
    pTime = cTime

    # Display FPS on the frame
    cv2.putText(img, f'FPS: {int(fps)}', (40, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)

    # Display the captured frame
    cv2.imshow("Img", img)

    # Exit if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close windows
cap.release()
cv2.destroyAllWindows()
