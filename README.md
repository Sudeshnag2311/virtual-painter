# 🎨 Virtual Painter using Python

A virtual painting application built using Python, OpenCV, and mediapipe.  
This project allows users to draw on the screen using hand gestures without touching the mouse or keyboard.

---

## 🚀 Features

- ✋ Hand gesture detection
- 🎨 Draw using finger movement
- 🖌️ Multiple color options
- 🧽 Eraser functionality
- 📷 Real-time webcam tracking
- ⚡ Smooth virtual drawing experience

---

## 🛠️ Technologies Used

- Python
- OpenCV
- MediaPipe
- NumPy

## 🧠 How It Works

- The project uses the **Index Finger** and **Middle Finger** for gesture detection.

### ✌️ Selection Mode
When both the **Index Finger** and **Middle Finger** are raised:
- User can select:
  - Brush colors
  - Eraser
  - Drawing tools

### ☝️ Drawing Mode
When only the **Index Finger** is raised:
- User can draw freely on the virtual canvas.

## 📂 Project Structure

virtual-painter/
│── drawing.py
│── hand_tracker.py
│── pink.jpeg
│── yellow.jpeg
│── green.jpeg
│── white.jpeg
│── normal.jpeg
│── eraser.jpeg

The webcam tracks hand movement in real-time using **MediaPipe Hand Tracking**.
