import cv2
import numpy as np
import os
import time
import hand_tracker as htm
base_path = os.path.dirname(os.path.abspath(__file__))
def load_image(path):
    img = cv2.imread(path)
    if img is None:
        print("Error loading:", path)
    return img
normal_header = load_image(
    os.path.join(base_path, "header", "normal.jpeg")
)
white_header = load_image(
    os.path.join(base_path, "header", "white.jpeg")
)

red_header = load_image(
    os.path.join(base_path, "header", "pink.jpeg")
)

yellow_header = load_image(
    os.path.join(base_path, "header", "yellow.jpeg")
)
green_header = load_image(
    os.path.join(base_path, "header", "green.jpeg")
)

eraser_header = load_image(
    os.path.join(base_path, "header", "eraser.jpeg")
)

if normal_header is None:
    print("Header images not found.")
    exit()

header = normal_header
cap = cv2.VideoCapture(0)
# window size
cap.set(3, 1020)
cap.set(4, 720)
detector = htm.HandTracker(detectionCon=0.85)
drawColor = (0, 0, 0)
brushThickness = 8
eraserThickness = 40
xp, yp = 0, 0
canvas = None
last_switch = 0
delay = 0.3
eraserMode = False
#open camera 
while True:
    success, img = cap.read()
    if not success:
        print("Camera error")
        break
    img = cv2.flip(img, 1)
    h, w, _ = img.shape
    if canvas is None:
        canvas = np.zeros((h, w, 3), np.uint8)
    header_height = 100
    header_resized = cv2.resize(
        header,
        (w, header_height)
    )
    img[0:header_height, 0:w] = header_resized

    img = detector.findHands(img)

    lmList = detector.findPosition(
        img,
        draw=False
    )
    if len(lmList) > 12:
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]
        fingers = detector.fingersUp()
        if fingers[1] and fingers[2]:
            xp, yp = 0, 0
            if y1 < header_height and time.time() - last_switch > delay:
                section_width = w // 6

                # normal
                if 0 * section_width < x1 < 1 * section_width:
                    header = normal_header
                    eraserMode = False

                # white 
                elif 1 * section_width < x1 < 2 * section_width:
                    drawColor = (255, 255, 255)
                    header = white_header
                    eraserMode = False

                # pink
                elif 2 * section_width < x1 < 3 * section_width:
                    drawColor = (203,190, 255)
                    header = red_header
                    eraserMode = False

                # Yellow
                elif 3 * section_width < x1 < 4 * section_width:
                    drawColor = (153, 255, 255)
                    header = yellow_header
                    eraserMode = False
                #green
                elif 4 * section_width < x1 < 5 * section_width:
                    drawColor = (0, 255, 0)
                    header = green_header
                    eraserMode = False

                # eraser
                elif 5 * section_width < x1 < 6 * section_width:
                    header = eraser_header
                    eraserMode = True
                last_switch = time.time()
        elif fingers[1] and not fingers[2]:
            # dot color
            if eraserMode:
                pointerColor = (0, 0, 0)   # black
            else:
                pointerColor = drawColor
            cv2.circle(
                img,
                (x1, y1),
                10,
                pointerColor,
                cv2.FILLED
            )
            if xp == 0 and yp == 0:
                xp, yp = x1, y1
            if eraserMode:
                color_to_use = (0, 0, 0)
                thickness = eraserThickness
            else:
                color_to_use = drawColor
                thickness = brushThickness
            cv2.line(
                canvas,
                (xp, yp),
                (x1, y1),
                color_to_use,
                thickness
            )
            xp, yp = x1, y1
        else:
            xp, yp = 0, 0
    else:
        xp, yp = 0, 0
    imgGray = cv2.cvtColor(
        canvas,
        cv2.COLOR_BGR2GRAY
    )
    _, imgInv = cv2.threshold(
        imgGray,
        50,
        255,
        cv2.THRESH_BINARY_INV
    )
    imgInv = cv2.cvtColor(
        imgInv,
        cv2.COLOR_GRAY2BGR
    )
    img = cv2.bitwise_and(
        img,
        imgInv
    )
    img = cv2.bitwise_or(
        img,
        canvas
    )
    cv2.namedWindow(
        "Virtual Painter",
        cv2.WINDOW_NORMAL
    )
    cv2.resizeWindow(
        "Virtual Painter",
        1200,
        800
    )
    cv2.imshow(
        "Virtual Painter",
        img
    )
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()