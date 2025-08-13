import cv2
import mediapipe as mp
import pyautogui
import numpy as np
import time

# Initialize MediaPipe and webcam
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.8,
    min_tracking_confidence=0.7
)
mp_draw = mp.solutions.drawing_utils

# Get screen resolution
screen_w, screen_h = pyautogui.size()
cap = cv2.VideoCapture(0)

# Last action time (click debounce)
last_left_click = 0
last_right_click = 0
click_delay = 1  # seconds

# Define camera range (adjust if pointer doesn’t reach the full screen)
cam_x_min, cam_x_max = 100, 540
cam_y_min, cam_y_max = 100, 380

def fingers_up(hand_landmarks):
    tips = [4, 8, 12, 16, 20]
    fingers = []
    # Thumb
    fingers.append(hand_landmarks.landmark[tips[0]].x < hand_landmarks.landmark[tips[0] - 1].x)
    # Other fingers
    for tip in tips[1:]:
        fingers.append(
            hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip - 2].y)
    return fingers  # [thumb, index, middle, ring, pinky]

print("\n[🎮 GESTURE MOUSE STARTED]")
print("🖐  All Fingers Open  --> Move Mouse")
print("☝🏼  Index Finger Only --> Left Click")
print("✌🏼  Index + Middle    --> Right Click")
print("❌  Press ESC or close window to exit\n")

while True:
    success, frame = cap.read()
    if not success:
        print("[WARNING] Camera frame not captured.")
        continue

    # Flip and convert to RGB
    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    result = hands.process(rgb)

    if result.multi_hand_landmarks:
        hand_landmark = result.multi_hand_landmarks[0]
        lm_list = []

        for id, lm in enumerate(hand_landmark.landmark):
            cx, cy = int(lm.x * w), int(lm.y * h)
            lm_list.append((cx, cy))

        mp_draw.draw_landmarks(frame, hand_landmark, mp_hands.HAND_CONNECTIONS)

        if lm_list:
            x, y = lm_list[8]  # Index tip

            # Map to screen coordinates (adjusted for calibration)
            screen_x = np.interp(x, [cam_x_min, cam_x_max], [0, screen_w])
            screen_y = np.interp(y, [cam_y_min, cam_y_max], [0, screen_h])

            # Move cursor with all fingers up
            finger_state = fingers_up(hand_landmark)
            current_time = time.time()

            if all(finger_state):  # All fingers open → Move
                pyautogui.moveTo(screen_x, screen_y, duration=0.05)

            # Only index finger → Left click
            elif finger_state[1] and not any(finger_state[2:]):
                if current_time - last_left_click > click_delay:
                    pyautogui.click()
                    print("[ACTION] Left Click")
                    last_left_click = current_time
                    time.sleep(0.3)

            # Index + middle fingers → Right click
            elif finger_state[1] and finger_state[2] and not any(finger_state[3:]):
                if current_time - last_right_click > click_delay:
                    pyautogui.click(button='right')
                    print("[ACTION] Right Click")
                    last_right_click = current_time
                    time.sleep(0.3)

    # Show the webcam feed
    cv2.imshow("🖱 Hand Gesture Mouse Control", frame)

    # ✅ Window closure detection
    if cv2.getWindowProperty("🖱 Hand Gesture Mouse Control", cv2.WND_PROP_VISIBLE) < 1:
        print("[INFO] Window closed. Exiting.")
        break

    # Exit on ESC key
    if cv2.waitKey(1) & 0xFF == 27:
        print("[INFO] ESC pressed. Exiting.")
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()
print("[✅] Program ended. Resources released.")
