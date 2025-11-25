# Hand Gesture Mouse Controller (OpenCV + MediaPipe + Python)

This project turns a regular webcam into a **virtual mouse controller** using **hand gestures**.  
By detecting hand landmarks in real time, the system lets the user **move the cursor and perform mouse clicks without touching a physical mouse**.


## Demo (What the Project Does)

✔ Moves the mouse pointer when all fingers are open  
✔ Performs **left click** using **only the index finger**  
✔ Performs **right click** using **index + middle fingers**  
✔ Exits safely when **ESC** is pressed or when the window is closed  

The program uses **computer vision + gesture classification** to map the index fingertip to the screen coordinates and execute PyAutoGUI mouse events.



## Technologies Used

| Library | Purpose |
|--------|---------|
| Python | Main programming language |
| OpenCV | Webcam capture & image processing |
| MediaPipe | Hand landmark detection (21 key points) |
| PyAutoGUI | System mouse control and click events |
| NumPy | Screen coordinate mapping |



## How to Run

Install the required modules:bash
pip install opencv-python mediapipe pyautogui numpy
python tra.py
